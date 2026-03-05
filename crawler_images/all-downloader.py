import time

import random
import requests
import os
import threading

from crawler_images import constants
from crawler_images.common import fixed_length, get_image_format, format_number, save_image
from crawler_images.deskbabes import Deskbabes
from crawler_images.istripper import Istripper
from crawler_images.penthouse import Penthouse
from crawler_images.penthouse_2 import Penthouse2
from crawler_images.virtuagirls import Virtuagirls


def create_website_info(website_title):
    website_dir = os.path.join(constants.base_dir, website_title)
    os.makedirs(website_dir, exist_ok=True)

    website_info_filename = f"{website_dir}/website_info.txt"
    if not os.path.exists(website_info_filename):
        with open(website_info_filename, 'w') as file:
            file.write("0")


def download_website_image(download_info):
    website_info = download_info["website_info"]
    download_min_page = website_info["download_min_page"]
    download_max_page = website_info["download_max_page"]
    if download_max_page < 0:
        download_max_page = website_info["max_page"]

    for page_index in range(download_min_page, download_max_page + 1):  # 遍历页码
        current_download_info = {
            "page_index": page_index
        }
        download_info["current_download_info"] = current_download_info

        try:
            download_page_image(download_info)
        except Exception as e:
            print(
                f"{"error - in page":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{page_index:>3}, exception:{e}")


def download_page_image(download_info):
    page_index = download_info["current_download_info"]["page_index"]
    print(
        f"{"current page":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{page_index:>3}")

    page_url = get_page_url(download_info, page=page_index)  # 获取当前页码的URL地址，如果没有该页码就返回空
    if not page_url:
        return
    download_info["current_download_info"]["page_url"] = page_url

    models = download_info["website_downloader"].get_models_in_page(download_info)  # 获取当前页的所有model
    model_count = len(models)
    if model_count < 1:
        return

    current_download_info = download_info["current_download_info"]
    current_download_info["model_count_in_page"] = model_count

    for model_index in range(model_count):  # 遍历当前页面的所有model
        current_download_info["model_index_in_page"] = model_index + 1
        current_download_info["model_info"] = models[model_index]

        try:
            download_model_image(download_info)
        except Exception as e:
            print(
                f"{"error - in model":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({(model_index + 1):>3}/{model_count:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, exception:{e}")


def download_model_image(download_info):
    current_download_info = download_info["current_download_info"]
    model_urls = current_download_info["model_info"]["urls"]
    model_url_count = len(model_urls)
    for model_url_index, model_url in enumerate(model_urls):
        current_download_info["model_url_index"] = model_url_index + 1
        current_download_info["model_url_count"] = model_url_count
        current_download_info["model_url"] = model_url

        try:
            download_model_sub_page_image(download_info)
        except Exception as e:
            print(
                f"{"error - in sub page":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{(model_url_index + 1):>3}/{model_url_count:>3},  exception:{e}")


def download_model_sub_page_image(download_info):
    current_download_info = download_info["current_download_info"]
    if if_model_downloaded(download_info["website_info"]["title"], download_info["current_download_info"]["model_url"]):
        print(
            f"{"page downloaded":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, model_url:{current_download_info["model_url"]}")
        return

    for second in range(1, 11):  # 每个页码，等待10秒
        print(
            f"{"sub page wait":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, model_url:{current_download_info["model_url"]}, {second}秒")
        time.sleep(1)

    download_model_sub_page_image2(download_info)


def download_model_sub_page_image2(download_info):
    model_images = download_info["website_downloader"].get_model_images(
        download_info)  # 获取当前model的所有图片地址, {"image_url": "image_url"}
    if not model_images:
        return

    current_download_info = download_info["current_download_info"]
    model_image_dir = create_model_dir(download_info["website_info"]["title"], current_download_info["page_index"],
                                       current_download_info["model_info"]["name"],
                                       current_download_info["model_info"]["dir_name"])
    current_download_info["model_info"]["dir"] = model_image_dir
    current_download_info["model_images"] = model_images

    print()
    print(
        f"{"current sub page":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, model_url:{current_download_info["model_url"]}, 图片数量:{len(model_images)}")
    save_model_sub_page_images(download_info)  # 下载当前model子页的所有图片


def save_model_sub_page_images(download_info):
    current_download_info = download_info["current_download_info"]
    image_count = len(current_download_info["model_images"])
    if download_info["website_info"]["independent_download_image"]:
        success_count = download_info["website_downloader"].save_images(download_info)
    else:
        success_count = save_images(download_info)
    if success_count < 0.9 * image_count:  # 下载成功率小于0.9
        save_statis(image_count, success_count, current_download_info["model_info"], current_download_info["model_url"])
    else:
        save_model_url_to_file(download_info["website_info"]["title"], current_download_info["model_info"],
                               current_download_info["model_url"])


def save_images(download_info):
    current_download_info = download_info["current_download_info"]
    model_images = current_download_info["model_images"]
    success_count = 0
    image_count = len(model_images)
    for image_index, image in enumerate(model_images):
        image_url = image["image_url"]
        try:
            image_format = get_image_format(image_url)
            if not image_format:
                print(
                    f"{"error - image format":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), image: {image_index + 1}/{image_count}, model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, image_url:{image_url}")
                continue

            save_image(image_url, image_format, current_download_info["model_url_index"], image_index,
                       current_download_info["model_info"]["dir"])
            success_count = success_count + 1
            print(
                f"{"success":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), image: {image_index + 1}/{image_count}, model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, image_url:{image_url}")
        except Exception as e:
            print(
                f"{"error - download":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), image: {image_index + 1}/{image_count}, model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, image_url:{image_url}, exception:{e}")

    return success_count


def get_page_url(download_info, **kwargs):
    website_info = download_info["website_info"]
    download_max_page = website_info["download_max_page"]
    if download_max_page < 0:
        download_max_page = website_info["max_page"]

    if download_info["current_download_info"]["page_index"] <= download_max_page:
        return download_info["website_info"]["url_template"].format(**kwargs)
    else:
        return ""


def create_model_dir(website_title, page, model_name, model_dir_name):
    seg_lower_limit = page - (page % 100)
    seg_upper_limit = seg_lower_limit + 100
    page_segment = "page" + format_number(seg_lower_limit) + "--page" + format_number(seg_upper_limit)

    model_image_dir = os.path.join(constants.base_dir, website_title, page_segment, format_number(page), model_name)
    if os.path.exists(model_image_dir):
        model_image_dir = os.path.join(constants.base_dir, website_title, page_segment, format_number(page), model_dir_name)
    os.makedirs(model_image_dir, exist_ok=True)
    return model_image_dir


def save_statis(total, success_count, model, model_url):
    ratio = success_count / total * 100
    with open(f"{model["dir"]}/statis.txt", "w", encoding='utf-8') as file:
        file.write(model["name"] + "[" + model_url + "]\r\n")
        file.write(f"下载结果, 总数:{total}, 成功:{success_count}, 成功率:{ratio}\r\n")


def save_model_url_to_file(website_title, model, model_url):
    website_dir = os.path.join(constants.base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "a", encoding='utf-8') as file:
        file.write(model["name"] + " [" + model_url + "]\r\n")


def if_model_downloaded(website_title, model_url):
    website_dir = os.path.join(constants.base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "r", encoding='utf-8') as file:
        content = file.read()
        if model_url in content:
            return True
        else:
            return False


def download(thread_id, website_downloader, selected_model_names):
    website_title = ""
    download_info = {
        "thread_id": thread_id,
        "website_downloader": website_downloader,
        "selected_model_names": selected_model_names,
    }
    try:
        website_info = website_downloader.get_website_info()  # 获取网站信息
        download_info["website_info"] = website_info
        website_title = website_info["title"]
        create_website_info(website_title)  # 创建目录和网站信息文件
        download_website_image(download_info)  # 下载网站下所有页码的图片
        print(f"{"thread finished":<25}, thread:{thread_id:>2}, website:{website_title:<15}")
    except Exception as e:
        print(
            f"{"thread error":<25}, thread:{thread_id:>2}, website:{website_title:<15}, exception:{e}")


def single_thread_download_website(website_downloaders, selected_model_names):
    for index, website_downloader in enumerate(website_downloaders):
        download(1, website_downloader, selected_model_names)


def multi_thread_download_website(website_downloaders, selected_model_names):
    for index, website_downloader in enumerate(website_downloaders):
        thread = threading.Thread(target=download,
                                  args=(index + 1, website_downloader, selected_model_names))
        thread.start()


def get_selected_model_names():
    selected_model_names = []
    # selected_model_names.append("stacy cruz")
    # selected_model_names.append("natasha nice")
    # selected_model_names.append("lucy li")
    # selected_model_names.append("jia lissa")
    # selected_model_names.append("alexis crystal")
    # selected_model_names.append("cabiria")
    # selected_model_names.append("lana rhoades")
    # selected_model_names.append("helga lovekaty")
    # selected_model_names.append("sybil")
    # selected_model_names.append("cindy shine")

    return selected_model_names


def get_website_downloaders():
    website_downloaders = []

    # website_downloaders.append(Istripper())
    # website_downloaders.append(Virtuagirls())
    website_downloaders.append(Penthouse2())
    # website_downloaders.append(Deskbabes())

    return website_downloaders


def main_download():
    multi_thread = True
    website_downloaders = get_website_downloaders()
    selected_model_names = get_selected_model_names()
    if multi_thread:
        multi_thread_download_website(website_downloaders, selected_model_names)
    else:
        single_thread_download_website(website_downloaders, selected_model_names)


if __name__ == "__main__":
    main_download()
