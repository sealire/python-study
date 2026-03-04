import random
import re
from urllib.parse import urljoin

from crawler_images.common import is_selected_model, get_page_html, get_model_image_html


class Ysvw:

    def get_website_info(self):
        return {
            "title": "ysvw",
            "url_template": "https://girl-atlas.xyz/tag?id=57653d1458e03930fbb7e344&p={page}",
            "max_page": 8,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        html_text = get_page_html(download_info)
        if not html_text:
            return model_list
        container = html_text.find('div', id='div-tag')
        model_cards = container.find_all("div", class_='card-body')
        for index, model_card in enumerate(model_cards):
            model_card_h4 = model_card.find("h4").find("a")
            model_name = model_card_h4.string
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_url = model_card_h4.get("href")
                model_url = urljoin(download_info["current_download_info"]["page_url"], model_url)
                model_dir_name = model_name + "-" + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, download_info):
        image_urls = []
        html_text = get_model_image_html(download_info)
        if not html_text:
            return image_urls
        container = html_text.find('div', class_='gallery')
        image_tags = container.find_all("a")

        for i, image in enumerate(image_tags):
            image_url = image.get("src") or image.get("data-src")
            if not image_url:
                continue
            image_full_url = urljoin(download_info["current_download_info"]["model_url"], image_url)
            if image_full_url and image_full_url.startswith('http'):
                image_urls.append({
                    "image_url": image_full_url.strip()
                })

        return image_urls
