# -*- coding: utf-8 -*-
import scrapy
from sun0769.items import Sun0769Item


class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4']

    def parse(self, response):
        # 分组
        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for tr in tr_list:
        	item = Sun0769Item()
        	item["title"] = tr.xpath("./td[2]/a[@class='news14']/@title").extract_first()
        	item["href"] = tr.xpath("./td[2]/a[@class='news14']/@href").extract_first()
        	item["publish_date"] = tr.xpath("./td[last()]/text()").extract_first()
        	
        	# 请求详情页
        	yield scrapy.Request(
        		item["href"],
        		callback = self.parse_detail,
        		meta = {"item":item}
        	)
          
        	# 翻页
        	next_url = response.xpath("//a[text()='>']/@href").extract_first()
        	i = 0
        	while i<2:
	        	if next_url:
	        		yield scrapy.Request(
	        			next_url,
	        			callback=self.parse
	        		)
	        	i+=1

    def parse_detail(self, response):
      	"""处理详情页"""
      	item = response.meta["item"]
      	item["content"] = response.xpath("//td[@class='txt16_3']//text()").extract()
      	item["content_img"] = response.xpath("//td[@class='txt16_3']//img/@src").extract()
      	item["content_img"] = ["http://wz.sun0769.com" + i for i in item["content_img"]]
      	# print(item)
      	yield item
