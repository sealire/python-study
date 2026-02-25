import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

headers = {"User-Agent": "Mozilla/5.0"}


def download_images(url, file_dir="images"):
    os.makedirs(file_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    for i, img in enumerate(img_tags):
        img_url = img.get("src") or img.get("data-src")
        if not img_url:
            continue
        img_full_url = urljoin(url, img_url)
        try:
            img_data = requests.get(img_full_url, headers=headers).content
            with open(f"{file_dir}/image_{i}.jpg", "wb") as f:
                f.write(img_data)
            print(f"下载成功: image_{i}.jpg")
        except Exception as e:
            print(f"下载失败: {e}")


def save_txt(content, file_dir, mode):
    with open(f"{file_dir}/url.txt", mode, encoding='utf-8') as file:
        file.write(content)


def format_number(number, width=4):
    return f"{number:0{width}d}"


def get_url(template, **kwargs):
    return template.format(**kwargs)


def get_models(page_url):
    model_list = []

    model_list.append({"name": "张三1", "url": "https://www.doewe.com/{page}.html"})
    # model_list.append({"name": "张三2", "url": "https://www.doewe.com/{page}.html"})
    # model_list.append({"name": "张三3", "url": "https://www.doewe.com/{page}.html"})

    return model_list


def get_model_img_urls(model_url):
    img_urls = []

    img_urls.append({
        "img_url": "https://gips0.baidu.com/it/u=1690853528,2506870245&fm=3028&app=3028&f=JPEG&fmt=auto?w=1024&h=1024"
    })

    # img_urls.append({
    #     "img_url": "https://gips3.baidu.com/it/u=1022347589,1106887837&fm=3028&app=3028&f=JPEG&fmt=auto?w=960&h=1280"
    # })

    return img_urls


def save_statis(total, success_count, file_dir, model_info):
    ratio = success_count / total * 100
    with open(f"{file_dir}/statis.txt", "w", encoding='utf-8') as file:
        file.write(model_info["name"] + "\r\n")
        file.write(model_info["url"] + "\r\n")
        file.write(f"下载结果, 总数:{total}, 成功:{success_count}, 成功率:{ratio}")


def download_model_imgs(page, model_info, img_urls, file_dir):
    success_count = 0
    for index in range(len(img_urls)):
        try:
            img_data = requests.get(img_urls[index]["img_url"], timeout=5, headers=headers).content
            with open(f"{file_dir}/image_{index + 1}.jpg", "wb") as f:
                f.write(img_data)
            success_count = success_count + 1
            print(f"下载完成, page:{page}, model_url:{model_info["url"]}, img_url:{img_urls[index]["img_url"]}")
        except Exception as e:
            print(f"下载失败, page:{page}, model_url:{model_info["url"]}, exception:{e}")

    total = len(img_urls)
    if success_count < 0.6 * total:  # 下载成功率小于0.6
        save_statis(total, success_count, file_dir, model_info)


def save_images(template, base_dir="images", min_page=1, max_page=3000):
    for page in range(min_page, max_page + 1):  # 遍历页码
        sub_dir = format_number(page // 100)
        page_url = get_url(template, page=page)  # 获取当前页码的URL地址
        models = get_models(page_url)  # 获取当前页的所有model, {"name": "name", "url": "url"}
        for model in models:  # 遍历当前页面的所有model
            file_dir = os.path.join(base_dir, sub_dir, format_number(page), model["name"])
            os.makedirs(file_dir, exist_ok=True)

            img_urls = get_model_img_urls(model["url"])  # 获取当前model的所有图片地址, {"img_url": "img_url"}
            print()
            print("当前下载, page:", page, ", model:", model["name"], ", 图片数量:", len(img_urls))
            download_model_imgs(page, model, img_urls, file_dir)  # 下载当前model的所有图片


url_template = "https://www.doewe.com/{page}.html"
save_images(url_template, min_page=1, max_page=120)
