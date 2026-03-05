import random
import re
import time

import requests
from bs4 import BeautifulSoup

from crawler_images import constants
from crawler_images.common import is_selected_model, get_page_html, get_model_image_html, get_image_format, \
    save_image_by_chunk, fixed_length


class Sgirlsweb:

    def __init__(self, download_min_page=1, download_max_page=-1):
        self.download_min_page = download_min_page
        self.download_max_page = download_max_page

    def get_website_info(self):
        return {
            "title": "sgirlsweb",
            "url_template": "https://www.sgirlsweb.com/all-sexy-girls/{page}/",
            "max_page": 9,
            "download_min_page": self.download_min_page,
            "download_max_page": self.download_max_page,
            "independent_download_image": True,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        html_text = get_page_html(download_info)
        if not html_text:
            return model_list
        container = html_text.find('ul', id='iids')
        model_cards = container.find_all("li", class_='item')
        model_count = len(model_cards)
        for model_index, model_card in enumerate(model_cards):
            model_h2 = model_card.find("div", class_="item-pdat-text").find("h2")
            model_name = model_h2.get_text(strip=True)
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_name_split = model_name.replace(' ', "-").lower()
                model_urls = self.get_model_urls(download_info, model_index, model_count, model_name, model_name_split)
                model_dir_name = model_name + " - " + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": model_urls})

        return model_list

    def get_model_urls(self, download_info, model_index, model_count, model_name, model_name_split):
        model_urls = []
        max_image_page_index = 1
        base_url = "https://www.sgirlsweb.com/girl/" + model_name_split + "/photo-gallery/"
        while True:
            max_image_page = self.get_model_max_image_page(download_info, model_index, model_count, model_name,
                                                           base_url, max_image_page_index)
            if max_image_page <= max_image_page_index:
                break
            max_image_page_index = max_image_page
            print(
                f"{"get max image page":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{download_info["current_download_info"]["page_index"]:>3}, model_index: {model_index:<3}/{model_count:<3}, {model_name:<30}, max_image_page_index:{max_image_page_index}")

        for page in range(1, max_image_page_index + 1):  # 遍历页码
            model_url = base_url + str(page) + "/"
            model_urls.append(model_url)

        return model_urls

    def get_model_max_image_page(self, download_info, model_index, model_count, model_name, base_url,
                                 max_image_page_index):
        model_url = base_url + str(max_image_page_index) + "/"
        html_text = self.get_model_image_html(download_info, model_index, model_count, model_name, model_url,
                                              max_image_page_index)
        container = html_text.find('div', class_='pages')
        if not container:
            return max_image_page_index
        lis = container.find_all("li")
        count = len(lis)
        last = lis[count - 3]
        pa = last.find("a")
        if pa:
            return int(pa.string)
        else:
            return max_image_page_index

    def get_model_image_html(self, download_info, model_index, model_count, model_name, model_url,
                             max_image_page_index):
        try:
            response = requests.get(model_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except Exception as e:
            print(
                f"{"get image page error":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{download_info["current_download_info"]["page_index"]:>3}, model_index: {model_index:<3}/{model_count:<3}, {model_name:<30}, max_image_page_index:{max_image_page_index}, exception:{e}")
            return None
        return BeautifulSoup(response.text, "html.parser")

    def get_model_images(self, download_info):
        model_images = []
        html_text = get_model_image_html(download_info)
        if not html_text:
            return model_images
        container = html_text.find('ul', id='iids')
        image_tags = container.find_all("li", class_='fl-photo-item')
        for i, image in enumerate(image_tags):
            img = image.find("a", class_="athumb").find("img")
            image_url = img.get("src")
            if image_url and image_url.startswith('http'):
                # image_url = image_url.replace("thumbs-photos/480/", "thumbs-photos/1080/")

                image_url = image_url.replace("static3", "static1")
                image_url = image_url.replace("thumbs-photos/480", "")
                index = image_url.rfind("/") + 1
                image_url = image_url[:index] + "mibogirl-" + image_url[index:]

                model_images.append({
                    "image_url": image_url.strip()
                })

        return model_images

    def save_images(self, download_info):
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

                self.save_image2(image_url, image_format, current_download_info["model_index_in_page"],
                                 current_download_info["model_url_index"], image_index, image_count,
                                 current_download_info["model_info"]["dir"], download_info)

                success_count = success_count + 1
                print(
                    f"{"success":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), image: {image_index + 1}/{image_count}, model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, image_url:{image_url}")
            except Exception as e:
                print(
                    f"{"error - download":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), image: {image_index + 1}/{image_count}, model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, image_url:{image_url}, exception:{e}")

        return success_count

    def save_image2(self, image_url, image_format, model_index, sub_page_index, image_index, image_count, model_dir,
                    download_info):
        current_download_info = download_info["current_download_info"]
        headers = {
            'Referer': 'https://www.sgirlsweb.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
        }
        retry_count = 4
        ex = None
        success = False
        while retry_count > 0:
            try:
                save_image_by_chunk(image_url, image_format, model_index, sub_page_index, image_index, model_dir, headers)
                success = True
            except Exception as e:
                success = False
                ex = e

            if success:
                break

            retry_count = retry_count - 1
            if retry_count > 0:
                sec = 3 * retry_count
                print(
                    f"{"download retry":<25}, thread:{download_info["thread_id"]:>2}, website:{download_info["website_info"]["title"]:<15}, page:{current_download_info["page_index"]:>3}({current_download_info["model_index_in_page"]:>3}/{current_download_info["model_count_in_page"]:>3}), image: {image_index + 1}/{image_count}, model_name:{fixed_length(current_download_info["model_info"]["name"], width=30)}, sub_page:{current_download_info["model_url_index"]:>3}/{current_download_info["model_url_count"]:>3}, image_url:{image_url}, sleep: {sec}秒")
                time.sleep(sec)

        if not success:
            raise ex
