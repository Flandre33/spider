from selenium import webdriver
import time


# 实例化一个浏览器
driver = webdriver.Chrome()
# driver = webdriver.PhantonJS()

# 发送请求
driver.get("http://www.baidu.com")

# 设置窗口大小
# driver.set_window_size(1920, 1080)
# 最大化窗口
driver.maximize_window()

# 进行页面截屏
driver.save_screenshot("./baidu.png")

# 元素定位的方法
# driver.find_element_by_id("kw").send_keys("python") # 输入数据
# driver.find_element_by_id("su").click() # 点击

# 获取html字符串
print(driver.page_source) # elements的内容

# 获取当前url地址
print(driver.current_url)

# 获取cookies
cookies = driver.get_cookies()
# 字典推导式
cookies = {i["name"]:i["value"] for i in cookies}

# 退出浏览器
time.sleep(3)
driver.quit()
