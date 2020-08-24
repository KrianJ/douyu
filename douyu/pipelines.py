import pymongo


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_port):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 更新并去重
        if item.collection == 'live_rooms':
            self.db[item.collection].update_one({'roomSrc': item['roomSrc']}, {'$set': item}, upsert=True)
        elif item.collection == 'channel':
            self.db[item.collection].insert_one(dict(item))
            pass
        elif item.collection == 'room_info':
            self.db[item.collection].update_one({'room_id': item['room_id']}, {'$set': item}, upsert=True)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )
