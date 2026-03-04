import random
import re
from urllib.parse import urljoin

from crawler_images.common import is_selected_model, get_page_html_by_selenium, get_model_image_html_by_selenium


class Penthouse2:

    def __init__(self, download_min_page=1, download_max_page=-1):
        self.download_min_page = download_min_page
        self.download_max_page = download_max_page

    def get_website_info(self):
        return {
            "title": "penthouse",
            "url_template": "https://penthouse-galleries.net/penthouse_galleries_{page}.html",
            "max_page": 26,
            "download_min_page": self.download_min_page,
            "download_max_page": self.download_max_page,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        html_text = get_page_html_by_selenium(download_info)
        if not html_text:
            return model_list
        container = html_text.find('div', class_='gallery-grid')
        model_cards = container.find_all("div", class_='gallery-item')
        for index, model_card in enumerate(model_cards):
            model_card_a = model_card.find("a")
            model_name = model_card_a.find("span").string
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_url = model_card_a.get("href")
                model_url = urljoin(download_info["current_download_info"]["page_url"], model_url)
                model_dir_name = model_name + " - " + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, download_info):
        image_urls = []
        html_text = get_model_image_html_by_selenium(download_info)
        if not html_text:
            return image_urls

        container = html_text.find('div', class_='space-y-6')
        grids = container.find_all('div', class_='grid')
        for index, grid in enumerate(grids):
            image_tags = grid.find_all("a")
            for i, image in enumerate(image_tags):
                image_url = image.get("href")
                if image_url and image_url.startswith('http'):
                    image_urls.append({
                        "image_url": image_url.strip()
                    })

        return image_urls
