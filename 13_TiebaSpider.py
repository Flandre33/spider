import requests
from lxml import etree
import json


class TiebaSpider():
	def __init__(self, tieba_name):
		self.tieba_name = tieba_name
		self.start_url = "https://m.tieba.com/mo/q---A7D058AE8445A71C7C092EF60711A6F9%3AFG%3D1--1-3-0--2--wapp_1558537494603_423/m?kw="+tieba_name+"&pn=0"
		self.part_url = "https://m.tieba.com/mo/q---A7D058AE8445A71C7C092EF60711A6F9%3AFG%3D1--1-3-0--2--wapp_1558537494603_423/"
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

	def parse_url(self, url):
		"""发送请求，获取响应"""
		response = requests.get(url, headers=self.headers, verify=False)
		return response.content

	def get_content_list(self, html_str):
		"""提取数据"""
		html = etree.HTML(html_str)
		div_list = html.xpath("//div[contains(@class,'i')]") # 根据div分组
		content_list = []
		for div in div_list:
			item={}
			item["title"] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()"))>0 else None
			item["href"] = self.part_url + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href"))>0 else None
			item["img_list"] = self.get_img_list(item["href"], [])
			content_list.append(item)
		# 提取下一页的url地址
		next_url = html.xpath("//a[text()='下一页']/@href")[0] if len(html.xpath("//a[text()='下一页']/@href"))>0 else None
		return content_list, next_url

	def get_img_list(self, detail_url, total_img_list):
	 	"""获取帖子中的所有图片"""
	 	# 3.2请求列表页的url地址，获取详情页的第一页
	 	detail_html_str = self.parse_url(detail_url)
	 	detail_html = etree.HTML(detail_html_str)
	 	# 3.3提取详情页第一页的图片，提取下一页的地址
	 	img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
	 	total_img_list.extend(img_list)
	 	# 3.4请求详情页下一个的地址，进入循环
	 	detail_next_url = detail_html.xpath("//a[text()='下一页']/@href")
	 	if len(detail_next_url)>0:
	 		detail_next_url = self.part_url + detail_next_url[0]
	 		return self.get_img_list(detail_next_url, total_img_list)
	 	
	 	return total_img_list

	def save_content_list(self, content_list):
		file_path = self.tieba_name+".txt"
		with open(file_path,"w",encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n\n")

	def run(self):
		"""实现主要逻辑"""
		next_url = self.start_url
		while next_url is not None:
			# 1.start_url
			# 2.发送请求，获取响应
			html_str = self.parse_url(next_url)
			# 3.提取数据，提取下一页的url地址
				# 3.1提取列表页的url地址和标题
				# 3.2请求列表页的url地址，获取详情页的第一页
				# 3.3提取详情页第一页的图片，提取下一页的地址
				# 3.4请求详情页下一个的地址，进入循环
			content_list, next_url = self.get_content_list(html_str)
			# 4.保存数据
			self.save_content_list(content_list)
			# 5.请求下一页的url地址，进入循环

if __name__ == '__main__':
	blhx = TiebaSpider("碧蓝航线")
	blhx.run()
