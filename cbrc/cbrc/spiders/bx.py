# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class BxSpider(CrawlSpider):
    name = 'bx'
    allowed_domains = ['cbrc.gov.cn']
    start_urls = ['http://www.cbrc.gov.cn/chinese/newListDoc/111002/1.html']
    print("start")
    # 定义提取url地址规则
    rules = (
        # LinkExtractor:链接提取器，提取url地址
        # callback:处理提取出来的url地址的response
        # follow:当前url地址的响应是否能重新进入rules提取url地址（exp：下一页的url
        Rule(LinkExtractor(allow=r'/chinese/newShouDoc/.+\.html'), callback='parse_item'),
        )
    print("end")

    def parse_item(self, response):
        print("-"*50)
        item = {}
        item["title"] = response.xpath("//div[@class='Section0']//h2//text()").extract_first()
        item["date"] = re.findall("发布时间:(20\d{2}-\d{2}-\d{2})", response.body.decode())[0]
        print(item)
