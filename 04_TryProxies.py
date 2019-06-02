import requests


proxies = {"http":"http://39.137.77.67:8080"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}

r = requests.get("http://www.baidu.com", proxies=proxies, headers=headers)

print(r.status_code)

