from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://deskbabesgirls.com/galleries/0724_lucy_li.html")
# 等待特定元素加载完成
wait = WebDriverWait(driver, 30)
element = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "h2"))
)

print(driver.page_source)
