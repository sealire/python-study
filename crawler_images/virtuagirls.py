import random
import re

from crawler_images.common import is_selected_model, get_page_html, get_model_image_html


class Virtuagirls:

    def __init__(self, download_min_page=1, download_max_page=-1):
        self.download_min_page = download_min_page
        self.download_max_page = download_max_page

    def get_website_info(self):
        return {
            "title": "virtuagirls",
            "url_template": "https://virtuagirlgirls.com/?page={page}",
            "max_page": 40,
            "download_min_page": self.download_min_page,
            "download_max_page": self.download_max_page,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        html_text = get_page_html(download_info)
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
                model_dir_name = model_name + " - " + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": [model_url]})

        return model_list

    def get_model_images(self, download_info):
        model_images = []
        html_text = get_model_image_html(download_info)
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
