# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cnblogs.items import CnblogsItem
import pymongo


class CnblogsPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        dbName = client['cnblogs']
        self.table = dbName['articles']

    def process_item(self, item, spider):
        if isinstance(item, CnblogsItem):
            self.table.insert(dict(item))
            return item
