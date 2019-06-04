# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class Sun0769Pipeline(object):
    def process_item(self, item, spider):
    	item["content"] = self.process_content(item["content"])
    	print(item)
    	return item

    def process_content(self, content):
    	content = [re.sub(r"\xa0|\s", "", i) for i in content]

    	# 去除列表中的空字符串
    	content = [i for i in content if len(i)>0]
    	return content
