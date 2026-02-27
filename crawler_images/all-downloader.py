import time
from operator import truediv

import requests
import os
import threading

from crawler_images import constants
from crawler_images.girl_atlas import GirlAtlas
from crawler_images.girl_atlas_Japanese import GirlAtlasJapanese
from crawler_images.girl_atlas_artgravia import GirlAtlasArtGravia
from crawler_images.girl_atlas_bimilstory import GirlAtlasBimilstory
from crawler_images.girl_atlas_bomb import GirlAtlasBomb
from crawler_images.girl_atlas_chinese import GirlAtlasChinese
from crawler_images.girl_atlas_cosplay import GirlAtlasCosplay
from crawler_images.girl_atlas_denudeart import GirlAtlasDeNudeArt
from crawler_images.girl_atlas_eroticbeauty import GirlAtlasEroticBeauty
from crawler_images.girl_atlas_eternaldesire import GirlAtlasEternalDesire
from crawler_images.girl_atlas_famegirls import GirlAtlasFameGirls
from crawler_images.girl_atlas_fantia import GirlAtlasFantia
from crawler_images.girl_atlas_femjoy import GirlAtlasFemjoy
from crawler_images.girl_atlas_graphis import GirlAtlasGraphis
from crawler_images.girl_atlas_hegreart import GirlAtlasHegreArt
from crawler_images.girl_atlas_jvid import GirlAtlasJvid
from crawler_images.girl_atlas_korean import GirlAtlasKorean
from crawler_images.girl_atlas_leehee import GirlAtlasLeehee
from crawler_images.girl_atlas_ligui import GirlAtlasLigui
from crawler_images.girl_atlas_maycontaingirl import GirlAtlasMayContainGirl
from crawler_images.girl_atlas_metart import GirlAtlasMetArt
from crawler_images.girl_atlas_metartx import GirlAtlasMetArtX
from crawler_images.girl_atlas_mplstudios import GirlAtlasMPLStudios
from crawler_images.girl_atlas_nudeinrussia import GirlAtlasNudeInRussia
from crawler_images.girl_atlas_patreon import GirlAtlasPatreon
from crawler_images.girl_atlas_pbplus import GirlAtlasPbplus
from crawler_images.girl_atlas_perfect18 import GirlAtlasPerfect18
from crawler_images.girl_atlas_photodromm import GirlAtlasPhotoDromm
from crawler_images.girl_atlas_rylskyart import GirlAtlasRylskyArt
from crawler_images.girl_atlas_sabra import GirlAtlasSabra
from crawler_images.girl_atlas_sexart import GirlAtlasSexArt
from crawler_images.girl_atlas_showybeauty import GirlAtlasShowyBeauty
from crawler_images.girl_atlas_strapLez import GirlAtlasStrapLez
from crawler_images.girl_atlas_stunning18 import GirlAtlasStunning18
from crawler_images.girl_atlas_teendreams import GirlAtlasTeenDreams
from crawler_images.girl_atlas_ugirls import GirlAtlasUgirls
from crawler_images.girl_atlas_w4b import GirlAtlasW4b
from crawler_images.girl_atlas_wanibooks import GirlAtlasWanibooks
from crawler_images.girl_atlas_wpb_net import GirlAtlasWpbNet
from crawler_images.girl_atlas_xingyan import GirlAtlasXingyan
from crawler_images.girl_atlas_xiuren import GirlAtlasXiuren
from crawler_images.girl_atlas_xrwang import GirlAtlasXrwang
from crawler_images.girl_atlas_ysvw import GirlAtlasYsvw
from crawler_images.girl_atlas_zishy import GirlAtlasZishy


# 线程1
def download_thread1():
    download(GirlAtlasChinese(), 1)
    download(GirlAtlasJvid(), 1)
    download(GirlAtlasWanibooks(), 1)
    download(GirlAtlasLeehee(), 1)


# 线程2
def download_thread2():
    download(GirlAtlasXiuren(), 2)
    download(GirlAtlasJapanese(), 2)
    download(GirlAtlasYsvw(), 2)
    download(GirlAtlasArtGravia(), 2)
    download(GirlAtlasUgirls(), 2)
    download(GirlAtlasGraphis(), 2)
    download(GirlAtlasBomb(), 2)


# 线程3
def download_thread3():
    download(GirlAtlasXingyan(), 3)
    download(GirlAtlas(), 3)
    download(GirlAtlasSabra(), 3)
    download(GirlAtlasBimilstory(), 3)
    download(GirlAtlasLigui(), 3)
    download(GirlAtlasWpbNet(), 3)
    download(GirlAtlasKorean(), 3)


# 线程4
def download_thread4():
    download(GirlAtlasMetArt(), 4)
    download(GirlAtlasStunning18(), 4)
    download(GirlAtlasDeNudeArt(), 4)
    download(GirlAtlasPhotoDromm(), 4)
    download(GirlAtlasMPLStudios(), 4)
    download(GirlAtlasFameGirls(), 4)
    download(GirlAtlasNudeInRussia(), 4)
    download(GirlAtlasTeenDreams(), 4)


# 线程5
def download_thread5():
    download(GirlAtlasMetArtX(), 5)
    download(GirlAtlasFemjoy(), 5)
    download(GirlAtlasZishy(), 5)
    download(GirlAtlasPerfect18(), 5)
    download(GirlAtlasRylskyArt(), 5)
    download(GirlAtlasMayContainGirl(), 5)
    download(GirlAtlasShowyBeauty(), 5)
    download(GirlAtlasEternalDesire(), 5)


# 线程6
def download_thread6():
    download(GirlAtlasStrapLez(), 6)
    download(GirlAtlasSexArt(), 6)
    download(GirlAtlasPbplus(), 6)
    download(GirlAtlasW4b(), 6)
    download(GirlAtlasHegreArt(), 6)
    download(GirlAtlasEroticBeauty(), 6)


# 线程7
def download_thread7():
    download(GirlAtlasPatreon(), 7)
    download(GirlAtlasFantia(), 7)
    download(GirlAtlasCosplay(), 7)

# 线程8
def download_thread8():
    download(GirlAtlasXrwang(), 8)



def create_website_info(website_title):
    website_dir = os.path.join(constants.base_dir, website_title)
    os.makedirs(website_dir, exist_ok=True)

    website_info_filename = f"{website_dir}/website_info.txt"
    if not os.path.exists(website_info_filename):
        with open(website_info_filename, 'w') as file:
            file.write("0")


def download_image(website_downloader, website_info, thread_id):
    for page in range(1, constants.largest_page):  # 遍历页码
        try:
            page_url = get_page_url(website_downloader, website_info["url_template"],
                                    page=page)  # 获取当前页码的URL地址，如果没有该页码就返回空
            if not page_url:
                continue

            time.sleep(10)  # 每个页码，等待10秒
            download_page_image(website_downloader, website_info, page, page_url, thread_id)
        except Exception as e:
            print(
                f"EXCEPT-Page遍历下载异常, thread:{thread_id}, website_title:{website_info["title"]}, page:{page}, url_template:{website_info["url_template"]}, exception:{e}")


def download_page_image(website_downloader, website_info, page, page_url, thread_id):
    models = website_downloader.get_models(page_url)  # 获取当前页的所有model, {"name": "name", "url": "url"}
    model_count = len(models)
    if model_count < 1:
        return
    for model_index in range(model_count):  # 遍历当前页面的所有model
        try:
            model = models[model_index]
            model_downloaded = if_model_downloaded(website_info["title"], model["url"])
            if model_downloaded:
                print(
                    f"Model已下载, thread:{thread_id}, website_title:{website_info["title"]}, model_name:{model["name"]}, model_url:{model["url"]}")
                continue

            time.sleep(10)  # 每个model页面，等待10秒
            download_model_images(website_info["title"], website_downloader, page, model_index, model_count, model,
                                  thread_id)
        except Exception as e:
            print(
                f"EXCEPT-Model遍历下载异常, thread:{thread_id}, website_title:{website_info["title"]}, page:{page}, model_index:{model_index}, model_url:{models[model_index]["url"]}, exception:{e}")


def download_model_images(website_title, website_downloader, page, model_index, model_count, model, thread_id):
    image_urls = website_downloader.get_model_image_urls(model["url"])  # 获取当前model的所有图片地址, {"image_url": "image_url"}
    if not image_urls:
        return

    model_image_dir = create_model_dir(website_title, page, model["name"])
    model["dir"] = model_image_dir

    print()
    print(
        f"当前下载Model, thread:{thread_id}, website_title:{website_title}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, model_url:{model["url"]}, 图片数量:{len(image_urls)}")
    save_model_images(website_title, page, model_index, model_count, model, image_urls, thread_id)  # 下载当前model的所有图片


def save_model_images(website_title, page, model_index, model_count, model, image_urls, thread_id):
    success_count = 0
    total = len(image_urls)
    for index in range(total):
        try:
            img_data = requests.get(image_urls[index]["image_url"], timeout=constants.http_timeout,
                                    headers=constants.http_headers).content
            with open(f"{model["dir"]}/image_{index + 1}.jpg", "wb") as f:
                f.write(img_data)
            success_count = success_count + 1
            print(
                f"下载完成, thread:{thread_id}, website_title:{website_title}, {index + 1}/{total}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, image_url:{image_urls[index]["image_url"]}")
        except Exception as e:
            print(
                f"EXCEPT-Image下载失败, thread:{thread_id}, website_title:{website_title}, {index + 1}/{total}, page:{page}, model:{model_index + 1}/{model_count}, model_name:{model["name"]}, image_url:{image_urls[index]["image_url"]}, exception:{e}")

    if success_count < 0.9 * total:  # 下载成功率小于0.6
        save_statis(total, success_count, model)
    else:
        save_model_url_to_file(website_title, model)


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


def save_statis(total, success_count, model):
    ratio = success_count / total * 100
    with open(f"{model["dir"]}/statis.txt", "w", encoding='utf-8') as file:
        file.write(model["name"] + "[" + model["url"] + "]\r\n")
        file.write(f"下载结果, 总数:{total}, 成功:{success_count}, 成功率:{ratio}\r\n")


def save_model_url_to_file(website_title, model):
    website_dir = os.path.join(constants.base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "a", encoding='utf-8') as file:
        file.write(model["name"] + " [" + model["url"] + "]\r\n")


def if_model_downloaded(website_title, model_url):
    website_dir = os.path.join(constants.base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "r", encoding='utf-8') as file:
        content = file.read()
        if model_url in content:
            return True
        else:
            return False


def download(website_downloader, thread_id):
    website_info = website_downloader.get_website_info()  # 获取网站信息
    create_website_info(website_info["title"])  # 创建目录和网站信息文件
    download_image(website_downloader, website_info, thread_id)  # 下载网站下所有页码的图片


def multi_thread_download():
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

    thread6 = threading.Thread(target=download_thread6)
    thread6.start()

    thread7 = threading.Thread(target=download_thread7)
    thread7.start()

    thread8 = threading.Thread(target=download_thread8)
    thread8.start()


def single_thread_download():
    download_thread1()  # 东方
    download_thread2()  # 东方
    download_thread3()  # 东方
    download_thread4()  # 西方
    download_thread5()  # 西方
    download_thread6()  # 西方
    download_thread7()  # Cosplay
    download_thread8()  # 秀人网


if __name__ == "__main__":
    multi_thread = True
    if multi_thread:
        multi_thread_download()
    else:
        single_thread_download()
