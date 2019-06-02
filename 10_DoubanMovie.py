import requests
import json


class DoubanSpider(object):
	"""docstring for DoubanSpider"""
	def __init__(self):
		self.url_temp = "https://movie.douban.com/j/new_search_subjects?"
		self.headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}

	def parse_url(self, url):
		print(url)
		response = requests.get(url, headers=self.headers)
		return response.content.decode()

	def get_content_list(self, json_str):
		dict_ret = json.loads(json_str)
		content_list = dict_ret["data"]
		return content_list

	def save_content_list(self, content_list):
		with open("DoubanMovie.txt", "a", encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False))
				f.write("\n") # 写入换行符进行换行
		print("保存成功")

	def run(self):
		"""实现主要逻辑"""
		while True:
			# 1.start_url
			url = self.url_temp
			# 2.发送请求，获取响应
			json_str = self.parse_url(url)
			# 3.提取数据
			content_list = self.get_content_list(json_str)
			# 4.保存
			self.save_content_list(content_list)

if __name__ == '__main__':
	doubanspider = DoubanSpider()
	doubanspider.run()
		