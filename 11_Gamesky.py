import requests
import re
import json


class GamerSpider(object):
	"""docstring for Weibo"""
	def __init__(self):
		self.start_url = "https://www.gamersky.com/news/"
		self.headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}

	def parse_url(self, url):
		"""发送请求"""
		response = requests.get(url, headers=self.headers)
		return response.content.decode()

	def get_first_page_content_list(self, html_str):
		"""提取第一页"""
		content_list = re.findall(r"<div class=\"txt\">(.*)</div>", html_str)
		return content_list

	def save_content_list(self, content_list):
		"""保存"""
		with open("gamer.txt", "a", encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False))
				f.write("\n\n")
		print("SUCCESS")

	def run(self):
		"""实现主要逻辑"""
		# 1.start_url
		# 2.发送请求，获取响应
		html_str = self.parse_url(self.start_url)
		# 3.提取数据
		content_list = self.get_first_page_content_list(html_str)
		# 4.保存
		self.save_content_list(content_list)

if __name__ == '__main__':
	gamer = GamerSpider()
	gamer.run()
		