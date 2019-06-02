import requests
from lxml import etree
import json
import threading
from queue import Queue


class DuanSpider():
	def __init__(self):
		self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
		self.url_queue = Queue()
		self.html_queue = Queue()
		self.content_queue = Queue()

	def get_url_list(self):
		# return [self.url_temp.format(i) for i in range(1,11)]
		for i in range(1,11):
			self.url_queue.put(self.url_temp.format(i))

	def parse_url(self):
		while True:
			url = self.url_queue.get()
			print(url)
			response = requests.get(url, headers=self.headers)
			self.html_queue.put(response.content.decode())
			self.url_queue.task_done()

	def get_content_list(self):
		while True:
			html_str = self.html_queue.get()
			html = etree.HTML(html_str)
			div_list = html.xpath("//div[@id='content-left']/div") # 分组
			content_list = []
			for div in div_list:
				item = {}
				item["content"] = div.xpath(".//div[@class='content']/span/text()")
				item["content"] = [i.replace("\n", "") for i in item["content"]]
				content_list.append(item)
			self.content_queue.put(content_list)
			self.html_queue.task_done()
		
	def save_content_list(self):
		while True:
			content = self.content_queue.get()
			with open("段子.txt","w",encoding="utf-8") as f:
				for cont in content:
					f.write(json.dumps(cont, ensure_ascii=False, indent=2))
					f.write("\n\n")
			self.content_queue.task_done()

	def run(self):
		thread_list = []
		# 1.url_list
		t_url = threading.Thread(target=self.get_url_list)
		thread_list.append(t_url)
		# 2.遍历，发送请求，获取响应
		for i in range(5):
			t_parse = threading.Thread(target=self.parse_url)
			thread_list.append(t_parse)
		# 3.提取数据
		for i in range(5):
			t_html = threading.Thread(target=self.get_content_list)
			thread_list.append(t_html)
		# 4.保存
		t_save = threading.Thread(target=self.save_content_list)
		thread_list.append(t_save)

		for t in thread_list:
			t.setDaemon(True) # 把子进程设置为守护线程，主线程结束子进程也结束
			t.start()
		for q in [self.url_queue, self.html_queue, self.content_queue]:
			q.join() # 让主线程等待堵塞，等待队列的任务完成之后再完成

if __name__ == '__main__':
	duanzi = DuanSpider()
	duanzi.run()