import requests
import os
import threading

from crawler_images.girl_atlas import GirlAtlas
from crawler_images.girl_atlas_Japanese import GirlAtlasJapanese
from crawler_images.girl_atlas_chinese import GirlAtlasChinese
from crawler_images.girl_atlas_graphis import GirlAtlasGraphis
from crawler_images.girl_atlas_jvid import GirlAtlasJvid
from crawler_images.girl_atlas_ligui import GirlAtlasLigui
from crawler_images.girl_atlas_ugirls import GirlAtlasUgirls
from crawler_images.girl_atlas_wanibooks import GirlAtlasWanibooks
from crawler_images.girl_atlas_wpb_net import GirlAtlasWpbNet
from crawler_images.girl_atlas_xingyan import GirlAtlasXingyan
from crawler_images.girl_atlas_xiuren import GirlAtlasXiuren
from crawler_images.girl_atlas_ysvw import GirlAtlasYsvw

base_dir = "images"  # 基本目录
largest_page = 10000  # 最大页码
headers = {"User-Agent": "Mozilla/5.0"}


# 线程1
def download_thread1():
    download(GirlAtlasChinese(), 1)
    download(GirlAtlasJvid(), 1)
    download(GirlAtlasWanibooks(), 1)


# 线程2
def download_thread2():
    download(GirlAtlasXiuren(), 2)
    download(GirlAtlasJapanese(), 2)
    download(GirlAtlasYsvw(), 2)


# 线程3
def download_thread3():
    download(GirlAtlasXingyan(), 3)
    download(GirlAtlas(), 3)


# 线程4
def download_thread4():
    download(GirlAtlasUgirls(), 4)
    download(GirlAtlasGraphis(), 4)


# 线程5
def download_thread5():
    download(GirlAtlasLigui(), 5)
    download(GirlAtlasWpbNet(), 5)


def create_website_info(website_title):
    website_dir = os.path.join(base_dir, website_title)
    os.makedirs(website_dir, exist_ok=True)

    website_info_filename = f"{website_dir}/website_info.txt"
    if not os.path.exists(website_info_filename):
        with open(website_info_filename, 'w') as file:
            file.write("0")


def download_image(website_downloader, website_info, thread_id):
    for page in range(1, largest_page):  # 遍历页码
        page_url = get_page_url(website_info["url_template"], page=page)  # 获取当前页码的URL地址，如果没有该页码就返回空
        if not page_url:
            continue
        download_page_image(website_downloader, website_info, page, page_url, thread_id)


def download_page_image(website_downloader, website_info, page, page_url, thread_id):
    models = website_downloader.get_models(page_url)  # 获取当前页的所有model, {"name": "name", "url": "url"}
    model_count = len(models)
    if model_count < 1:
        return
    for model_index in range(model_count):  # 遍历当前页面的所有model
        model = models[model_index]
        model_downloaded = if_model_downloaded(website_info["title"], model["url"])
        if model_downloaded:
            continue

        model_image_dir = create_model_dir(website_info["title"], page, model["name"])
        model["dir"] = model_image_dir
        download_model_images(website_info["title"], website_downloader, page, model_index, model_count, model,
                              thread_id)


def download_model_images(website_title, website_downloader, page, model_index, model_count, model, thread_id):
    image_urls = website_downloader.get_model_image_urls(model["url"])  # 获取当前model的所有图片地址, {"image_url": "image_url"}
    if not image_urls:
        return

    print()
    print(
        f"当前下载, thread:{thread_id}, website_title:{website_title}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, model_url:{model["url"]}, 图片数量:{len(image_urls)}")
    save_model_images(website_title, page, model_index, model_count, model, image_urls, thread_id)  # 下载当前model的所有图片


def save_model_images(website_title, page, model_index, model_count, model, image_urls, thread_id):
    success_count = 0
    total = len(image_urls)
    for index in range(total):
        try:
            img_data = requests.get(image_urls[index]["image_url"], timeout=5, headers=headers).content
            with open(f"{model["dir"]}/image_{index + 1}.jpg", "wb") as f:
                f.write(img_data)
            success_count = success_count + 1
            print(
                f"下载完成, thread:{thread_id}, website_title:{website_title}, {index + 1}/{total}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, image_url:{image_urls[index]["image_url"]}")
        except Exception as e:
            print(
                f"下载失败, thread:{thread_id}, website_title:{website_title}, {index + 1}/{total}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, exception:{e}")

    if success_count < 0.6 * total:  # 下载成功率小于0.6
        save_statis(total, success_count, model)
    else:
        save_model_url_to_file(website_title, model)


def get_page_url(url_template, **kwargs):
    url = url_template.format(**kwargs)
    if check_page_exist(url):
        return url
    else:
        return ""


def check_page_exist(url):
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


def create_model_dir(website_title, page, model_name):
    seg_lower_limit = page - (page % 100)
    seg_upper_limit = seg_lower_limit + 100
    page_segment = "page" + format_number(seg_lower_limit) + "--page" + format_number(seg_upper_limit)

    model_image_dir = os.path.join(base_dir, website_title, page_segment, format_number(page), model_name)
    os.makedirs(model_image_dir, exist_ok=True)
    return model_image_dir


def format_number(number, width=4):
    return f"{number:0{width}d}"


def save_statis(total, success_count, model):
    ratio = success_count / total * 100
    with open(f"{model["dir"]}/statis.txt", "w", encoding='utf-8') as file:
        file.write(model["name"] + "[" + model["url"] + "]\r\n")
        file.write(f"下载结果, 总数:{total}, 成功:{success_count}, 成功率:{ratio}\r\n")


def save_model_url_to_file(website_title, model):
    website_dir = os.path.join(base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "a", encoding='utf-8') as file:
        file.write(model["name"] + " [" + model["url"] + "]\r\n")


def if_model_downloaded(website_title, model_url):
    website_dir = os.path.join(base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "r", encoding='utf-8') as file:
        content = file.read()
        if model_url in content:
            return True
        else:
            return False


def download(website_downloader: object, thread_id: object) -> None:
    website_info = website_downloader.get_website_info()  # 获取网站信息
    create_website_info(website_info["title"])  # 创建目录和网站信息文件
    download_image(website_downloader, website_info, thread_id)  # 下载网站下所有页码的图片


if __name__ == "__main__":
    thread1 = threading.Thread(target=download_thread1)
    thread1.start()

    thread2 = threading.Thread(target=download_thread2)
    thread2.start()

    thread3 = threading.Thread(target=download_thread3)
    thread3.start()

    thread4 = threading.Thread(target=download_thread4)
    thread4.start()

    thread5 = threading.Thread(target=download_thread5)
    thread5.start()
