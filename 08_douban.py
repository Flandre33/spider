import json
import requests
from parse_url import parse_url


url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0"
html_str = parse_url(url)

# json.loads把json字符串转化为python类型
ret = json.loads(html_str)

# json.dumps能够把python类型转化为json字符串
with open("douban.json", "w") as f:
	f.write(json.dumps(ret, ensure_ascii=False, indent=4))


