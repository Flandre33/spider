# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from pymongo import MongoClient

#client = MongoClient()
#collention = client["tencent"]["hr"]


class TencentPipeline(object):
    def process_item(self, item, spider):
    	print(item)
    	#collention.insert(item)
    	return item
