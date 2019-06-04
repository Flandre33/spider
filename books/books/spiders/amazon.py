# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    # allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b?ie=UTF8&node=658390051']
    redis_key = "amazon"
    print("- "*50)
    rules = (
        # 匹配大分类和小分类的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='left_nav browseBox']/ul/li")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='a-row a-expander-container a-expander-extend-container']/li")), follow=True),
        # 匹配图书的url地址
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='mainResults']/ul/li//h2/..")), callback="parse_book_detail"),
        # 匹配翻页的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']")), follow=True),

    )
    print("- "*50)

    def parse_book_detail(self, response):
        print("start")
        item = {}
        item["book_title"] = response.xpath("//span[@id='productTitle']/text()").extract_first()
        item["book_publish_date"] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first()
        item["book_author"] = response.xpath("//div[@id='bylineInfo']/span/a/text()").extract()
        item["book_price"] = response.xpath("//div[@id='soldByThirdParty']/span[2]/text()").extract_first()
        item["book_cate"] = response.xpath("//span[@class='a-list-item']/a/text()").extract()
        item["book_press"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()
        item["book_detail"] = response.xpath("//div[@id='iframeContent']/text()").extract_first()
        print(item)
