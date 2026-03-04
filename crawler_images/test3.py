from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import random
import requests
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # 启用无头模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 启动Selenium浏览器
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://deskbabesgirls.com/galleries/0724_lucy_li.html")
# https://deskbabesgirls.com/images/data/f0106/full/VGI1088P040019.jpg
# 等待特定元素加载完成
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "h2"))
)

# 等待页面完全加载
time.sleep(3)

print(driver.page_source)

# 获取当前页面的所有Cookie
cookies = driver.get_cookies()

# 将Selenium Cookie转换为requests格式
requests_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

# 从Selenium获取User-Agent
user_agent = driver.execute_script("return navigator.userAgent;")

# 获取图片元素
elements = driver.find_elements(By.CLASS_NAME, "photo-thumb")
print(elements)
img_url = elements[10].get_attribute("href")
print(img_url)

# 使用requests下载，复用Selenium的会话信息
headers = {
    "User-Agent": user_agent,
    "Referer": driver.current_url,  # 关键：使用当前页面URL作为Referer
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

response = requests.get(img_url, headers=headers, cookies=requests_cookies)
print(response)

driver.quit()
