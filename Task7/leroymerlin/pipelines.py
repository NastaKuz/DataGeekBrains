# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.mongo_base = client.leroymerlin

    def make_dict(self, params):
        specs_dict = {params[i]: params[i + 1] for i in range(0, (len(params) - 1), 2)}
        return specs_dict

    def process_item(self, item, spider):
        if item["params"]:
            item["params"] = self.make_dict(item["params"])

        print(item)

        item["_id"] = hashlib.sha1(str(item).encode()).hexdigest()

        collection = self.mongo_base[spider.name]

        collection.insert_one(item)

        return item


class LeroymerlinPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
