# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class DoubanPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'))

    def process_item(self, item, spider):
        item = dict(item)
        self.db['MovieTop250'].update({
            'title': item.get('title')
        }, {'#set': item}, True)
        return item

    def close_spider(self, spider):
        self.client.close()