# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class LiveRoomItem(Item):
    """索引页直播间信息"""
    collection = 'live_rooms'
    r_type = Field()    # 房间类型
    user = Field()      # 主播
    zoom = Field()      # 版块
    intro = Field()     # 介绍
    roomId = Field()    # 房间号
    hot = Field()       # 热度
    # remark = Field()    # 备注
    roomSrc = Field()   # 房间链接
    fans = Field()      # 粉丝数
    status = Field()    # 在播状态


class ChannelItem(Item):
    collection = 'channel'
    # 共享
    cate_id = Field()       # 主板块id/子版块对应的主板块id
    short_name = Field()    # 主板块简称/子板块简称
    # 父频道
    cate_name = Field()
    # 子频道
    tag_id = Field()
    tag_name = Field()
    tag_intro = Field()


class RoomInfo(Item):
    collection = 'room_info'
    room_id = Field()       # 房间号
    cate_id = Field()       # 所属主版块
    room_name = Field()     # 房间名
    status = Field()        # 在播状态
    owner_uid = Field()     # 主播id
    owner_name = Field()    # 主播名
    hot = Field()           # 房间热度
    game_name = Field()     # 子版块名称
    fans = Field()          # 粉丝数
    url = Field()           # 房间链接
