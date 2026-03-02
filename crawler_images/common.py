import requests
from bs4 import BeautifulSoup

from crawler_images import constants


def get_page_html(thread_id, page, page_url):
    try:
        response = requests.get(page_url, timeout=constants.http_timeout, headers=constants.http_headers)
    except Exception as e:
        print(f"EXCEPT-获取Page页面异常, thread:{thread_id}, page:{page}, page_url:{page_url}, exception:{e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def is_selected_model(model_name, model_names):
    selected = False
    mnl = model_name.lower()
    for mn in model_names:
        if mn in mnl:
            selected = True
            break
    return selected
