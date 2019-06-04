# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class BookSpider(scrapy.Spider):
    name = 'book'
    # allowed_domains = ['list.suning.com']
    start_urls = ['https://list.suning.com/0-502282-0.html#search-path']

    def parse(self, response):
        # 图书类型分组
        div_list = response.xpath("//div[@class='all-class clearfix']")
        for a in div_list:
        	item = {}
        	item["b_cate"] = a.xpath("./a/@title").extract_first()
        	item["b_href"] = a.xpath("./a/@href").extract_first()
        	item["b_href"] = "https:" + item["b_href"]
        	if item["b_href"]:
        		yield scrapy.Request(
        			item["b_href"],
        			callback=self.parse_book_list,
        			meta = {"item":deepcopy(item)} # 避免字典内容被替换
        			)

    def parse_book_list(self, response):
    	item = response.meta["item"]
    	# 图书列表分组
    	li_list = response.xpath("//ul[@class='general clearfix']/li")
    	for li in li_list:
    		item["book_name"] = li.xpath(".//div[@class='title-selling-point']/a/text()").extract_first()
    		item["book_price"] = li.xpath(".//div[@class='price-box']//text()").extract_first()
    		item["store_name"] = li.xpath(".//a[@class='store-name']/text()").extract_first()
    		item["book_href"] = li.xpath(".//div[@class='title-selling-point']/a/@href").extract_first()
    		item["book_href"] = "https:" + item["book_href"]
    		yield scrapy.Request(
    			item["book_href"],
    			callback=self.parse_book_detail,
    			meta = {"item":deepcopy(item)}
    			)
    	# 翻页
    	next_url = "https://list.suning.com/0-502282-" + '{}'.format(i for i in range(10)) +'.html'
    	if next_url:
    		yield scrapy.Request(
    			next_url,
    			callback=self.parse_book_list,
    			meta = {"item":item}
    			)

    def parse_book_detail(self, response):
    	item = response.meta["item"]
    	item["content"] = response.xpath("//h2[@id='promotionDesc']/text()").extract_first()
    	print(item)

