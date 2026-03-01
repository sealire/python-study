import time

import requests
import os
import threading

from crawler_images import constants
from crawler_images.common import is_selected_model
from crawler_images.istrippergirls import Istrippergirls
from crawler_images.sgirlsweb import Sgirlsweb
from crawler_images.virtuagirlgirls import Virtuagirlgirls


def create_website_info(website_title):
    website_dir = os.path.join(constants.base_dir, website_title)
    os.makedirs(website_dir, exist_ok=True)

    website_info_filename = f"{website_dir}/website_info.txt"
    if not os.path.exists(website_info_filename):
        with open(website_info_filename, 'w') as file:
            file.write("0")


def download_image(website_downloader, website_info, thread_id, model_names, min_page, max_page):
    for page in range(min_page, max_page):  # 遍历页码
        try:
            page_url = get_page_url(website_downloader, website_info["url_template"],
                                    page=page)  # 获取当前页码的URL地址，如果没有该页码就返回空
            if not page_url:
                continue

            download_page_image(website_downloader, website_info, page, page_url, thread_id, model_names)
        except Exception as e:
            print(
                f"EXCEPT-Page遍历下载异常, thread:{thread_id}, website_title:{website_info["title"]}, page:{page}, url_template:{website_info["url_template"]}, exception:{e}")


def download_page_image(website_downloader, website_info, page, page_url, thread_id, model_names):
    models = website_downloader.get_models(page_url, model_names)  # 获取当前页的所有model, {"name": "name", "url": "url"}
    model_count = len(models)
    if model_count < 1:
        return

    for model_index in range(model_count):  # 遍历当前页面的所有model
        model = models[model_index]
        model_urls = model["urls"]
        for model_url_index, model_url in enumerate(model_urls):
            try:
                model_downloaded = if_model_downloaded(website_info["title"], model_url)
                if model_downloaded:
                    print(
                        f"Model已下载, thread:{thread_id}, website_title:{website_info["title"]}, page:{page}, model_index:{model_index}, model_name:{model["name"]}, model_url_index:{model_url_index + 1}, model_url:{model_url}")
                    continue

                for second in range(1, 11):  # 每个页码，等待10秒
                    print(
                        f"Model遍历等待, thread:{thread_id}, website_title:{website_info["title"]}, page:{page}, model_index:{model_index}, model_url_index:{model_url_index + 1}, model_url:{model_url}, {second}秒")
                    time.sleep(1)
                download_model_images(website_info["title"], website_downloader, page, model_index, model_count, model,
                                      model_url_index, model_url, thread_id)
            except Exception as e:
                print(
                    f"EXCEPT-Model遍历下载异常, thread:{thread_id}, website_title:{website_info["title"]}, page:{page}, model_index:{model_index}, model_url:{model_url}, exception:{e}")


def download_model_images(website_title, website_downloader, page, model_index, model_count, model, model_url_index,
                          model_url, thread_id):
    image_urls = website_downloader.get_model_image_urls(model_url)  # 获取当前model的所有图片地址, {"image_url": "image_url"}
    if not image_urls:
        return

    model_image_dir = create_model_dir(website_title, page, model["name"])
    model["dir"] = model_image_dir

    print()
    print(
        f"当前下载Model, thread:{thread_id}, website_title:{website_title}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, model_url_index:{model_url_index + 1}, model_url:{model_url}, 图片数量:{len(image_urls)}")
    save_model_images(website_title, page, model_index, model_count, model, model_url_index, model_url, image_urls,
                      thread_id)  # 下载当前model的所有图片


def save_model_images(website_title, page, model_index, model_count, model, model_url_index, model_url, image_urls,
                      thread_id):
    success_count = 0
    total = len(image_urls)
    for index in range(total):
        try:
            img_data = requests.get(image_urls[index]["image_url"], timeout=constants.http_timeout,
                                    headers=constants.http_headers).content
            with open(f"{model["dir"]}/image_{model_url_index + 1}_{index + 1}.jpg", "wb") as f:
                f.write(img_data)
            success_count = success_count + 1
            print(
                f"下载完成, thread:{thread_id}, website_title:{website_title}, {index + 1}/{total}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, model_url_index:{model_url_index}, image_url:{image_urls[index]["image_url"]}")
        except Exception as e:
            print(
                f"EXCEPT-Image下载失败, thread:{thread_id}, website_title:{website_title}, {index + 1}/{total}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, model_url_index:{model_url_index}, image_url:{image_urls[index]["image_url"]}, exception:{e}")

    if success_count < 0.9 * total:  # 下载成功率小于0.6
        save_statis(total, success_count, model, model_url)
    else:
        save_model_url_to_file(website_title, model, model_url)


def get_page_url(website_downloader, url_template, **kwargs):
    url = url_template.format(**kwargs)
    if website_downloader.check_page_exist(url):
        return url
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


def download(thread_id, website_downloader, model_names, min_page, max_page):
    website_title = ""
    try:
        website_info = website_downloader.get_website_info()  # 获取网站信息
        website_title = website_info["title"]
        create_website_info(website_title)  # 创建目录和网站信息文件
        download_image(website_downloader, website_info, thread_id, model_names, min_page, max_page)  # 下载网站下所有页码的图片
        print(f"下载线程完成，退出, thread:{thread_id}, website_title:{website_title}")
    except Exception as e:
        print(f"下载线程异常, thread:{thread_id}, website_title:{website_title}, exception:{e}")


def single_thread_download_website(website_downloaders, model_names, min_page=1, max_page=constants.largest_page):
    for index, website_downloader in enumerate(website_downloaders):
        download(index + 1, website_downloader, model_names, min_page, max_page)


def multi_thread_download_website(website_downloaders, model_names, min_page=1, max_page=constants.largest_page):
    for index, website_downloader in enumerate(website_downloaders):
        thread = threading.Thread(target=download,
                                  args=(index + 1, website_downloader, model_names, min_page, max_page))
        thread.start()


if __name__ == "__main__":
    multi_thread = True
    downloaders = [Sgirlsweb()]
    names = ["stacy cruz", "natasha nice", "lucy li", "jia lissa"]
    if multi_thread:
        multi_thread_download_website(downloaders, names)
    else:
        single_thread_download_website(downloaders, names)
