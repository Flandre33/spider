# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import urllib


class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://dangdang.com/']
    redis_key = "dangdang"

    def parse(self, response):
        div_list = response.xpath("//div[@class='con flq_body']/div")
        # 大分类分组
        for div in div_list:
        	item = {}
        	item["b_cate"] = div.xpath("./dl/dt//text()").extract()
        	item["b_cate"] = [i.strip() for i in item["b_cate"] if len(i.strip())>0]
        	# 中间分类分组
        	dl_list = div.xpath(".//dl[@class='inner_dl']")
        	for dl in dl_list:
        		item["m_cate"] = dl.xpath("./dt//text()").extract()
        		item["m_cate"] = [i.strip() for i in item["m_cate"] if len(i.strip())>0]
        		# 小分类分组
        		a_list = dl.xpath("./dd/a")
        		for a in a_list:
        			item["href"] = a.xpath("./@href").extract_first()
        			item["s_cate"] = a.xpath("./text()").extract_first()
        			if item["href"]:
        				yield scrapy.Request(
        					item["href"],
        					callback=self.parse_book_list,
        					meta = {"item":deepcopy(item)}
        				)

    def parse_book_list(self, response):
    	item = response.meta["item"]
    	li_list = response.xpath("//ul[@class='bigimg']/li")
    	for li in li_list:
    		item["book_name"] = li.xpath("./p[@class='name']/a/@title").extract_first()
    		item["book_detail"] = li.xpath("./p[@class='detail']/text()").extract_first()
    		item["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").extract_first()
    		item["book_author"] = li.xpath("./p[@class='search_book_author']/span[1]/a/text()").extract()
    		print(item)
    	# 下一页
    	next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
    	if next_url:
    		next_url = urllib.parse.urljoin(response.url, next_url)
    		yield scrapy.Request(
    			next_url,
    			callback=self.parse_book_list,
    			meta={"item":item}
    		)
