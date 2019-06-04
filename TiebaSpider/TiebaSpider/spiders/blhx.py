# -*- coding: utf-8 -*-
import scrapy
from TiebaSpider.items import TiebaspiderItem
import urllib
import requests


class BlhxSpider(scrapy.Spider):
    name = 'blhx'
    allowed_domains = ['m.tieba.com']
    start_urls = ['http://m.tieba.com/mo/q---DF69575A6D913C2DF3799BE7DD8FE336%3AFG%3D1--1-3-0--2--wapp_1559096070619_304/m?kw=%E7%A2%A7%E8%93%9D%E8%88%AA%E7%BA%BF&lp=5011&lm=&pn=0']

    def parse(self, response):
        # 分组
        div_list = response.xpath("//div[@class='i']")
        for div in div_list:
            item = {}
            item["href"] = div.xpath("./a/@href").extract_first()
            item["title"] = div.xpath("./a/text()").extract_first()
            item["img_list"] = []
            print( item["href"])
            print(item["title"])
            if item["href"]:
                item["href"] = urllib.parse.urljoin(response.url, item["href"])
                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta = {"item":item}
                )
            # 列表页的翻页
            next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
            if next_url:
                next_url = urllib.parse.urljoin(response.url, next_url)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["img_list"].extend(response.xpath("//a[text()='图']/@href").extract())
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_detail,
                meta = {"item":item}
            )
        else:
            #print(item)
            yield item
