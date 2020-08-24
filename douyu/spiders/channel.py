import scrapy
import json
from douyu.items import ChannelItem, RoomInfo
from scrapy import Request
from urllib.parse import urlencode


class ChannelSpider(scrapy.Spider):
    """爬取各大版块以及其下小版块所有直播列表"""
    name = 'channel'
    allowed_domains = ['douyu.com']
    start_urls = ['http://capi.douyucdn.cn/api/v1/getColumnList']

    def parse(self, response):
        mc_item = ChannelItem()          # main channel Item
        channels = json.loads(response.text).get('data')
        for channel in channels:
            # 生成主板块item
            mc_item['cate_id'] = channel.get('cate_id')
            mc_item['cate_name'] = channel.get('cate_name')
            mc_item['short_name'] = channel.get('short_name')
            yield mc_item
            # 生成子板块Request
            sub_channel_base = 'http://capi.douyucdn.cn/api/v1/getColumnDetail?shortName={0}'
            sub_channel_url = sub_channel_base.format(mc_item['short_name'])
            yield Request(url=sub_channel_url, callback=self.sub_channel_parse, dont_filter=True)

    def sub_channel_parse(self, response):
        sc_item = ChannelItem()          # sub channel item
        channels = json.loads(response.text).get('data')
        for channel in channels:
            # 生成子版块item
            sc_item['cate_id'] = channel.get('cate_id')
            sc_item['tag_id'] = channel.get('tag_id')
            sc_item['tag_name'] = channel.get('tag_name')
            sc_item['short_name'] = channel.get('short_name')
            sc_item['tag_intro'] = channel.get('tag_introduce')
            yield sc_item
            # 生成子版块下的直播列表Request
            rooms_base = 'http://capi.douyucdn.cn/api/v1/live/{0}?'.format(sc_item['tag_id'])
            for i in range(20):
                if not i:
                    data = {'limit': 20, 'offset': 0}
                else:
                    data = {'limit': 20, 'offset': i*20}
                data = urlencode(data)
                rooms_url = rooms_base + data
                yield Request(url=rooms_url, callback=self.rooms_parse, dont_filter=True)

    def rooms_parse(self, response):
        r_item = RoomInfo()
        rooms = json.loads(response.text).get('data')
        for room in rooms:
            r_item['room_id'] = room.get('room_id')
            r_item['cate_id'] = room.get('cate_id')
            r_item['room_name'] = room.get('room_name')
            r_item['status'] = room.get('show_status')
            r_item['owner_uid'] = room.get('owner_uid')
            r_item['owner_name'] = room.get('nickname')
            r_item['hot'] = room.get('hn')
            r_item['game_name'] = room.get('game_name')
            r_item['fans'] = room.get('fans')
            r_item['url'] = 'www.douyu.com/'+r_item['room_id']
            yield r_item



