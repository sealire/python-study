import random
import requests
from bs4 import BeautifulSoup

from crawler_images import constants

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_page_html(download_info):
    current_download_info = download_info["current_download_info"]
    try:
        response = requests.get(current_download_info["page_url"], timeout=constants.http_timeout,
                                headers=constants.http_headers)
    except Exception as e:
        print(
            f"{"error - page html":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}, page_url:{current_download_info["page_url"]}, exception:{e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_page_html_by_selenium(download_info):
    current_download_info = download_info["current_download_info"]
    retry_count = 3
    success = False
    driver = get_webdriver()
    while retry_count > 0:
        try:
            driver.get(current_download_info["page_url"])
            wait = WebDriverWait(driver, 30)
            element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "div"))
            )
            success = True
        except Exception as e:
            print(
                f"{"error - page html":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}, page_url:{current_download_info["page_url"]}, retry:{4 - retry_count} exception:{e}")
            success = False
        if success:
            break
        retry_count = retry_count - 1

    if success:
        return BeautifulSoup(driver.page_source, "html.parser")
    else:
        return None


def get_model_image_html(download_info):
    current_download_info = download_info["current_download_info"]
    try:
        response = requests.get(current_download_info["model_url"], timeout=constants.http_timeout,
                                headers=constants.http_headers)
    except Exception as e:
        print(
            f"{"error - image html":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, model_url:{current_download_info["model_url"]}, exception:{e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_model_image_html_by_selenium(download_info):
    current_download_info = download_info["current_download_info"]
    retry_count = 3
    success = False
    driver = get_webdriver()
    while retry_count > 0:
        try:
            driver.get(current_download_info["model_url"])
            wait = WebDriverWait(driver, 30)
            element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "div"))
            )
            success = True
        except Exception as e:
            print(
                f"{"error - image html":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, model_url:{current_download_info["model_url"]}, retry:{4 - retry_count}, exception:{e}")
            success = False
        if success:
            break
        retry_count = retry_count - 1

    if success:
        return BeautifulSoup(driver.page_source, "html.parser")
    else:
        return None


def is_selected_model(model_name, download_info):
    selected_model_names = download_info["selected_model_names"]
    if not selected_model_names:
        return True
    model_name_lower = model_name.lower()
    selected = False
    for name in selected_model_names:
        if name in model_name_lower:
            selected = True
            break
    if not selected:
        print(
            f"{"unselected":<15}, thread_id:{download_info["thread_id"]:>2}, page:{download_info["current_download_info"]["page_index"]:<15}, model_name:{fixed_length(model_name, width=30)}")
    return selected


def fixed_length(s, width=25, fill_char=' '):
    if len(s) >= width:
        return s[:width]
    else:
        return s.ljust(width, fill_char)


def get_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)
