from selenium import webdriver


class DouyuSpider():
	def __init__(self):
		self.start_url = "https://www.douyu.com/directory/all"
		self.driver = webdriver.Chrome()

	def get_content_list(self):
		li_list = self.driver.find_elements_by_xpath("//ul[@class='layout-Cover_list']/li")
		# 分组
		content_list = []
		for li in li_list:
			item = {}
			item["room_img"] = li.find_element_by_xpath(".//div[@class='DyListCover-superscript']/img").get_attribute("src") # 获取元素
			item["room_title"] = li.find_element_by_xpath(".//h3[@class='DyListCover-intro']").get_attribute("title")
			item["anchor_name"] = li.find_element_by_xpath(".//h2[@class='DyListCover-user']").text
			item["watch_num"] = li.find_element_by_xpath(".//span[@class='DyListCover-hot']").text
			print(item)
			content_list.append(item)
		# 获取下一页的元素
		next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")
		next_url = next_url[0] if len(next_url)>0 else None
		return content_list, next_url

	def save_content_list(self, content_list):
		with open("douyu.txt","w",encoding="utf-8") as f:
			for content in content_list:
				f.write(json.dumps(content, ensure_ascii=False, indent=2))
				f.write("\n\n")

	def run(self):
		"""实现主要逻辑"""
		# 1.start_url
		# 2.发送请求，获取响应
		self.driver.get(self.start_url)
		# 3.提取数据，提取下一页的按钮
		content_list, next_url = self.get_content_list()
		# 4.保存数据
		self.save_content_list(content_list)
		# 5.点击下一页元素，循环
		while next_url:
			next_url.click()
			content_list, next_url = self.get_content_list()
			self.save_content_list(content_list)

if __name__ == '__main__':
	douyu = DouyuSpider()
	douyu.run()