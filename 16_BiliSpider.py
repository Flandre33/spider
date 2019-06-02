import requests
from lxml import etree
import json
import re


class BiliSpider():
	def __init__(self):
		#self.url = url
		self.url_danmu = "http://comment.bilibili.com/93048148.xml"
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

	def parse_url(self, url):
		"""获取响应"""
		response = requests.get(url, headers=self.headers)
		return response.content

	def get_html(self, html_str):
		"""提取数据"""
		html = etree.HTML(html_str)
		danmu_list = html.xpath("//d/text()")
		content_list = []
		for danmu in danmu_list:
			content_list.append(danmu)
		return content_list

	def save_danmu(self, content_list):
		with open("弹幕.txt","w",encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n")

	def run(self):
		# 1.url
		# 2.发送请求，获取响应
		html_str = self.parse_url(self.url_danmu)
		# 3.提取数据
		content_list = self.get_html(html_str)
		# 4.保存
		self.save_danmu(content_list)

if __name__ == '__main__':
	danmu = BiliSpider()
	danmu.run()