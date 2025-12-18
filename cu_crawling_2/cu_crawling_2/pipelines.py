# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CuCrawling2PipelineMongoDB:
    def __init__(self):
        self.mongo_db = "items"
        self.mongo_uri = f"mongodb://admin:admin@localhost:27017/{self.mongo_db}?authSource=admin"
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection_name = "collection"

    def close_spider(self, spider, reason):
        self.client.close()

    def process_item(self, item, spider):
        if item:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
