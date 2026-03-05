import random
import re
import time
from urllib.parse import urljoin

import requests

from crawler_images.common import is_selected_model, get_image_format, format_number, fixed_length, save_image, \
    get_page_html_by_selenium, get_model_image_html_by_selenium, save_image_by_chunk


class Deskbabes:

    def __init__(self, download_min_page=1, download_max_page=-1):
        self.download_min_page = download_min_page
        self.download_max_page = download_max_page

    def get_website_info(self):
        return {
            "title": "deskbabes",
            "url_template": "https://deskbabesgirls.com/?page={page}",
            "max_page": 14,
            "download_min_page": self.download_min_page,
            "download_max_page": self.download_max_page,
            "independent_download_image": True,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        html_text = get_page_html_by_selenium(download_info)
        if not html_text:
            return model_list
        container = html_text.find('div', class_='grid-cols-2')
        model_cards = container.find_all("a", class_='gallery-card')
        for index, model_card in enumerate(model_cards):
            model_name = model_card.find("img").get("alt")
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_url = model_card.get("href")
                model_url = urljoin(download_info["current_download_info"]["page_url"], model_url)
                model_dir_name = model_name + " - " + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": [model_url]})

        return model_list

    def get_model_images(self, download_info):
        model_images = []
        html_text = get_model_image_html_by_selenium(download_info)
        if not html_text:
            return model_images
        container = html_text.find('div', class_='content-section')
        image_tags = container.find_all("a", class_='photo-thumb')
        for i, image in enumerate(image_tags):
            image_url = image.get("href")
            if image_url and image_url.startswith('http'):
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

                if "https://deskbabesgirls.com" in image_url:
                    self.save_image2(image_url, image_format, current_download_info["model_index_in_page"],
                                     current_download_info["model_url_index"], image_index, image_count,
                                     current_download_info["model_info"]["dir"], download_info)
                else:
                    save_image(image_url, image_format, current_download_info["model_index_in_page"],
                               current_download_info["model_url_index"], image_index,
                               current_download_info["model_info"]["dir"])

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
            'Referer': 'https://deskbabesgirls.com',
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
