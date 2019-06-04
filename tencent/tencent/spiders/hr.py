# -*- coding: utf-8 -*-
import scrapy
import json


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['careers.tencent.com']
    start_urls = ['https://careers.tencent.com/search.html']

    def parse(self, response):
        li_list = response.xpath("//div[@class='search-content']")
        print(li_list)
        for li in li_list:
        	item = {}
        	item["title"] = li.xpath(".//h4/text()").extract_first()
        	item["place"] = li.xpath(".//span[2]/text()").extract_first()
        	item["intro"] = li.xpath(".//p[2]/text()").extract_first()
        	yield item


