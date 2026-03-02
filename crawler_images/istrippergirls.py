import re

import requests
from bs4 import BeautifulSoup

from crawler_images import constants
from crawler_images.common import is_selected_model, get_page_html


class Istrippergirls:

    def get_website_info(self):
        return {
            "title": "Istrippergirls",
            "url_template": "https://istrippergirls.net/?page={page}",
        }

    def check_page_exist(self, thread_id, page, page_url):
        html_text = get_page_html(thread_id, page, page_url)
        container = html_text.find('div', class_='grid-cols-2')
        if not container:
            return False
        model_cards = container.find_all("a", class_='gallery-card')
        if model_cards:
            return True
        else:
            return False

    def get_models(self, thread_id, page, page_url, model_names):
        model_list = []
        html_text = get_page_html(thread_id, page, page_url)
        container = html_text.find('div', class_='grid-cols-2')
        model_cards = container.find_all("a", class_='gallery-card')
        model_count = len(model_cards)
        for index, model_card in enumerate(model_cards):
            # print(model_card.getText)
            # model_card_a = model_card.find("a", class_="gallery-thumb")
            model_url = model_card.get("href")
            # model_url = urljoin(page_url, model_url)
            model_name = model_card.find("img").get("alt")
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if model_names and not is_selected_model(model_name, model_names):
                print(
                    f"忽略该model, thread_id:{thread_id}, page:{page}, model:{index + 1}/{model_count},  model_name:{model_name}")
                print(
                    f"忽略该model, thread_id:{thread_id}, page:{page}, model:{index + 1}/{model_count},  model_name:{model_name}")
                continue
            # print(model_name, '###############', model_url)
            model_list.append({"name": model_name, "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, model_url):
        image_urls = []

        try:
            response = requests.get(model_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Model页面超时, model_url:{model_url}")
            return image_urls
        html_text = BeautifulSoup(response.text, "html.parser")
        # print(response.text)

        container = html_text.find('div', class_='content-section')
        image_tags = container.find_all("a", class_='photo-thumb')
        for i, image in enumerate(image_tags):
            image_url = image.get("href")
            if image_url and image_url.startswith('http'):
                image_urls.append({
                    "image_url": image_url
                })

        return image_urls
