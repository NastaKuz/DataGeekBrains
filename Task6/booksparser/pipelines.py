# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class BooksparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        item['title'] = item['title'].replace("\n", "").strip()
        item['author'] = item['author'].replace("\n", "").strip()
        if item['main_price'] is not None:  # если нет в наличии, то цены нет
            item['main_price'] = float(re.findall(r'\d+', item['main_price'])[0])
        if item['discount_price'] is not None:
            item['discount_price'] = float(re.findall(r'\d+', item['discount_price'])[0])
            item['main_price'], item['discount_price'] = item['discount_price'], item['main_price']
        item['rating'] = float(item['rating'].replace("\n", "").replace(',', '.').strip())

        item['_id'] = hashlib.sha1(str(item).encode()).hexdigest()

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
