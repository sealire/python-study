import time

import requests
import os
import threading

from crawler_images import constants
from crawler_images.common import is_selected_model
from crawler_images.deskbabesgirls import Deskbabesgirls
from crawler_images.istrippergirls import Istrippergirls
from crawler_images.penthouse_pets import PenthousePets
from crawler_images.sgirlsweb import Sgirlsweb
from crawler_images.virtuagirlgirls import Virtuagirlgirls


def create_website_info(website_title):
    website_dir = os.path.join(constants.base_dir, website_title)
    os.makedirs(website_dir, exist_ok=True)

    website_info_filename = f"{website_dir}/website_info.txt"
    if not os.path.exists(website_info_filename):
        with open(website_info_filename, 'w') as file:
            file.write("0")


def download_website_image(download_info):
    for page_index in range(download_info["min_page"], download_info["max_page"]):  # 遍历页码
        current_download_info = {
            "page_index": page_index
        }
        download_info["current_download_info"] = current_download_info

        try:
            download_page_image(download_info)
        except Exception as e:
            print(
                f"EXCEPT-Page下载异常, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{page_index}, exception:{e}")


def download_page_image(download_info):
    page_index = download_info["current_download_info"]["page_index"]
    print(
        f"遍历Page, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{page_index}")

    page_url = get_page_url(download_info, page=page_index)  # 获取当前页码的URL地址，如果没有该页码就返回空
    if not page_url:
        return

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
                f"EXCEPT-Model下载异常, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{current_download_info["page_index"]}({model_index + 1}/{model_count}), model_name:{current_download_info["model_info"]["name"]}, exception:{e}")


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
                f"EXCEPT-Model子页下载异常, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{current_download_info["page_index"]}, model_name:{current_download_info["model_info"]["name"]}, sub_page:{model_url_index + 1}/{model_url_count},  exception:{e}")


def download_model_sub_page_image(download_info):
    current_download_info = download_info["current_download_info"]
    if if_model_downloaded(download_info["website_info"]["title"], download_info["current_download_info"]["model_url"]):
        print(
            f"Model子页已下载, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, model_url:{current_download_info["model_url"]}")
        return

    for second in range(1, 11):  # 每个页码，等待10秒
        print(
            f"下载等待, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, model_url:{current_download_info["model_url"]}, {second}秒")
        time.sleep(1)

    download_model_sub_page_image2(download_info)


def download_model_sub_page_image2(download_info):
    image_urls = download_info["website_downloader"].get_model_image_urls(
        download_info)  # 获取当前model的所有图片地址, {"image_url": "image_url"}
    if not image_urls:
        return

    current_download_info = download_info["current_download_info"]
    model_image_dir = create_model_dir(download_info["website_info"]["title"], current_download_info["page_index"],
                                       current_download_info["model_info"]["name"])
    current_download_info["model_info"]["dir"] = model_image_dir
    current_download_info["model_image_urls"] = image_urls

    print()
    print(
        f"当前下载Model, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, model_url:{current_download_info["model_url"]}, 图片数量:{len(image_urls)}")
    save_model_sub_page_images(download_info)  # 下载当前model子页的所有图片


def save_model_sub_page_images(download_info):
    current_download_info = download_info["current_download_info"]
    model_image_urls = current_download_info["model_image_urls"]

    success_count = 0
    image_count = len(model_image_urls)
    for image_index in range(image_count):
        try:
            image_url = model_image_urls[image_index]["image_url"]
            image_format = get_image_format(image_url)
            if not image_format:
                print(
                    f"EXCEPT-Image下载失败, 图片格式错误, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, image: {image_index + 1}/{image_count}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, image_url:{model_image_urls[image_index]["image_url"]}")
                continue

            img_data = requests.get(model_image_urls[image_index]["image_url"], timeout=constants.http_timeout,
                                    headers=constants.http_headers).content
            with open(
                    f"{current_download_info["model_info"]["dir"]}/image_{format_number(current_download_info["model_url_index"] + 1)}_{format_number(image_index + 1)}.{image_format}",
                    "wb") as f:
                f.write(img_data)
            success_count = success_count + 1
            print(
                f"下载完成, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, image: {image_index + 1}/{image_count}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, image_url:{model_image_urls[image_index]["image_url"]}")
        except Exception as e:
            print(
                f"EXCEPT-Image下载失败, thread:{download_info["thread_id"]}, website:{download_info["website_info"]["title"]}, image: {image_index + 1}/{image_count}, page:{current_download_info["page_index"]}({current_download_info["model_index_in_page"]}/{current_download_info["model_count_in_page"]}), model_name:{current_download_info["model_info"]["name"]}, sub_page:{current_download_info["model_url_index"]}/{current_download_info["model_url_count"]}, image_url:{model_image_urls[image_index]["image_url"]}, exception:{e}")

    if success_count < 0.9 * image_count:  # 下载成功率小于0.9
        save_statis(image_count, success_count, current_download_info["model_info"], current_download_info["model_url"])
    else:
        save_model_url_to_file(download_info["website_info"]["title"], current_download_info["model_info"],
                               current_download_info["model_url"])


def get_image_format(image_url):
    index = image_url.rfind(".")
    if index > 0:
        image_format = image_url[index + 1:]
        if image_format in ["jpg", "jpeg", "png"]:
            return image_format
        return ""
    else:
        return ""


def get_page_url(download_info, **kwargs):
    page_url = download_info["website_info"]["url_template"].format(**kwargs)
    download_info["current_download_info"]["page_url"] = page_url
    if download_info["website_downloader"].check_page_exist(download_info):
        return page_url
    else:
        return ""


def create_model_dir(website_title, page, model_name):
    seg_lower_limit = page - (page % 100)
    seg_upper_limit = seg_lower_limit + 100
    page_segment = "page" + format_number(seg_lower_limit) + "--page" + format_number(seg_upper_limit)

    model_image_dir = os.path.join(constants.base_dir, website_title, page_segment, format_number(page), model_name)
    os.makedirs(model_image_dir, exist_ok=True)
    return model_image_dir


def format_number(number, width=4):
    return f"{number:0{width}d}"


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


def download(thread_id, website_downloader, selected_model_names, min_page, max_page):
    website_title = ""
    download_info = {
        "thread_id": thread_id,
        "website_downloader": website_downloader,
        "selected_model_names": selected_model_names,
        "min_page": min_page,
        "max_page": max_page,
    }
    try:
        website_info = website_downloader.get_website_info()  # 获取网站信息
        download_info["website_info"] = website_info
        website_title = website_info["title"]
        create_website_info(website_title)  # 创建目录和网站信息文件
        download_website_image(download_info)  # 下载网站下所有页码的图片
        print(f"线程下载完成，退出, thread:{thread_id}, website:{website_title}")
    except Exception as e:
        print(f"下载线程异常, thread:{thread_id}, website:{website_title}, exception:{e}")


def single_thread_download_website(website_downloaders, selected_model_names, min_page=1,
                                   max_page=constants.largest_page):
    for index, website_downloader in enumerate(website_downloaders):
        download(1, website_downloader, selected_model_names, min_page, max_page)


def multi_thread_download_website(website_downloaders, selected_model_names, min_page=1,
                                  max_page=constants.largest_page):
    for index, website_downloader in enumerate(website_downloaders):
        thread = threading.Thread(target=download,
                                  args=(index + 1, website_downloader, selected_model_names, min_page, max_page))
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

    website_downloaders.append(Istrippergirls())
    website_downloaders.append(Virtuagirlgirls())
    website_downloaders.append(PenthousePets())

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
