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
            f"{fixed_length("error - page html")}, thread:{download_info["thread_id"]}, page:{current_download_info["page_index"]}, page_url:{current_download_info["page_url"]}, exception:{e}")
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_model_image_html(download_info):
    current_download_info = download_info["current_download_info"]
    try:
        response = requests.get(download_info["current_download_info"]["model_url"], timeout=constants.http_timeout,
                                headers=constants.http_headers)
    except Exception as e:
        print(
            f"{fixed_length("error - image html")}, thread:{download_info["thread_id"]}, website:{fixed_length(download_info["website_info"]["title"], width=15)}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, model_url:{current_download_info["model_url"]}, exception:{e}")
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
            f"{fixed_length("unselected")}, thread_id:{download_info["thread_id"]}, page:{download_info["current_download_info"]["page_index"]}, model_name:{fixed_length(model_name, width=30)}")
    return selected


def fixed_length(s, width=25, fill_char=' '):
    if len(s) >= width:
        return s[:width]
    else:
        return s.ljust(width, fill_char)
