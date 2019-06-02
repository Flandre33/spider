import requests


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
p = {"wd":"python"}
url_temp = "https://www.baidu.com/s?"

r = requests.get(url_temp, headers=headers, params=p)

print(r.status_code)
print(r.request.url)

url = "https://www.baidu.com/s?wd={}".format("python")
r2 = requests.get(url, headers=headers, params=p)
print(r2.request.url)