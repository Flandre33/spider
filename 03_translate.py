import requests
import json


search = input("请输入你要翻译的内容:")
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
post_data = {
	"query":search,
	"from":"en",
	"to":"zh",
}
post_url = "https://fanyi.baidu.com/basetrans"

r = requests.post(post_url, data=post_data, headers=headers)
# print(r.content.decode())
if r.content:
	dict_ret = json.loads(r.content.decode())
	ret = dict_ret["trans"][0]["dst"]
print("result is :")
