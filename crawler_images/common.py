import requests
from bs4 import BeautifulSoup

from crawler_images import constants


def get_page_html(download_info):
    current_download_info = download_info["current_download_info"]
    try:
        response = requests.get(current_download_info["page_url"], timeout=constants.http_timeout,
                                headers=constants.http_headers)
    except Exception as e:
        print(
            f"EXCEPT-获取Page页面异常, thread:{download_info["thread_id"]}, page:{current_download_info["page_index"]}, page_url:{current_download_info["page_url"]}, exception:{e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_model_image_html(download_info):
    current_download_info = download_info["current_download_info"]
    try:
        response = requests.get(download_info["current_download_info"]["model_url"], timeout=constants.http_timeout, headers=constants.http_headers)
    except Exception as e:
        print(
            f"EXCEPT-获取Model页面异常, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, model_url:{current_download_info["model_url"]}, exception:{e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


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
            f"model未选择, thread_id:{download_info["thread_id"]}, page:{download_info["current_download_info"]["page_index"]}, model_name:{model_name}")
    return selected
