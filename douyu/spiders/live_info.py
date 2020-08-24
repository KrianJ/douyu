import scrapy
from scrapy import Request
from douyu.items import *
from urllib.parse import urlencode
import json


class LiveInfoSpider(scrapy.Spider):
    """获取斗鱼直播首页的所有直播信息(斗鱼推荐+在线直播)"""
    name = 'live_info'
    allowed_domains = ['douyu.com']
    start_urls = ['http://www.douyu.com/directory/all']

    def start_requests(self):
        # 首页推荐直播
        data = {'num': 10}
        data = urlencode(data)
        base_url = 'https://www.douyu.com/japi/weblist/apinc/rec/list?'
        rec_url = base_url + data
        yield Request(url=rec_url, callback=self.index_parse)
        # 首页在线直播
        for i in range(100):
            if not i:
                ol_data = {'limit': 20, 'offset': 0}
            else:
                ol_data = ol_data = {'limit': 20, 'offset': i*20}
            ol_data = urlencode(ol_data)
            ol_base = 'http://capi.douyucdn.cn/api/v1/live?'
            ol_url = ol_base + ol_data
            yield Request(url=ol_url, callback=self.index_parse)

    def index_parse(self, response):
        """解析首页"""
        rooms = json.loads(response.text).get('data')
        if 'rec' in response.url:
            rec = LiveRoomItem()           # recommend_rooms
            for room in rooms:
                rec['r_type'] = 'recommend'
                rec['user'] = room.get('nickname')
                rec['zoom'] = room.get('cate2Name')
                rec['intro'] = room.get('roomName')
                rec['roomId'] = room.get('roomId')
                rec['hot'] = room.get('hot')
                rec['roomSrc'] = 'www.douyu.com/'+str(rec['roomId'])
                yield rec
        elif 'capi' in response.url:
            ol = LiveRoomItem()  # online_rooms
            for room in rooms:
                ol['r_type'] = 'online'
                ol['user'] = room.get('nickname')
                ol['zoom'] = room.get('game_name')
                ol['intro'] = room.get('room_name')
                ol['roomId'] = room.get('room_id')
                ol['hot'] = room.get('hn')
                ol['roomSrc'] = 'www.douyu.com/'+ol['roomId']
                ol['fans'] = room.get('fans')
                ol['status'] = room.get('show_status')
                yield ol
