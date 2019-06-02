import requests


session = requests.session()
post_url = "https://dotcounter.douyucdn.cn/deliver/fish2"
post_data = {"phoneNum":"18666887778", "password":"ldcrs1123"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}

# 使用session发送post请求，cookie保存其中
session.post(post_url, data=post_data, headers=headers)

# 在使用session进行请求登陆之后才能访问的地址
r = session.get("https://www.douyu.com/member/cp", headers=headers)
print(r.status_code)
