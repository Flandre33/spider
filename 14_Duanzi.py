import requests
from lxml import etree
import json


class DuanSpider():
	def __init__(self):
		self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

	def get_url_list(self):
		return [self.url_temp.format(i) for i in range(1,11)]

	def parse_url(self, url):
		response = requests.get(url, headers=self.headers)
		return response.content.decode()

	def get_content_list(self, html_str):
		html = etree.HTML(html_str)
		div_list = html.xpath("//div[@id='content-left']/div") # 分组
		content_list = []
		for div in div_list:
			item = {}
			item["content"] = div.xpath(".//div[@class='content']/span/text()")
			item["content"] = [i.replace("\n", "") for i in item["content"]]
			content_list.append(item)
		return content_list

	def save_content_list(self, content_list):
		with open("段子.txt","w",encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n\n")

	def run(self):
		# 1.url_list
		url_list = self.get_url_list()
		# 2.遍历，发送请求，获取响应
		for url in url_list:
			html_str = self.parse_url(url)
		# 3.提取数据
		content_list = self.get_content_list(html_str)
		# 4.保存
		self.save_content_list(content_list)

if __name__ == '__main__':
	duanzi = DuanSpider()
	duanzi.run()