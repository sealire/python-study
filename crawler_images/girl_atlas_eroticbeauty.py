import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from crawler_images import constants


class GirlAtlasEroticBeauty:

    def get_website_info(self):
        return {
            "title": "girl-atlas-EroticBeauty",
            "url_template": "https://girl-atlas.xyz/tag?id=672731e13aeba47e60ecad35&p={page}",
        }

    def check_page_exist(self, page_url):
        try:
            response = requests.get(page_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Page页面超时, page_url:{page_url}")
            return False
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find('div', id='div-tag')
        if not container:
            return False
        model_cards = container.find_all("div", class_='card-body')
        if model_cards:
            return True
        else:
            return False

    def get_models(self, page_url, model_names):
        model_list = []

        try:
            response = requests.get(page_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Page页面超时, page_url:{page_url}")
            return False
        soup = BeautifulSoup(response.text, "html.parser")

        # print(response.text)
        container = soup.find('div', id='div-tag')
        model_cards = container.find_all("div", class_='card-body')
        for i, model_card in enumerate(model_cards):
            # print(model_card.getText)
            model_card_h4 = model_card.find("h4").find("a")
            model_url = model_card_h4.get("href")
            model_url = urljoin(page_url, model_url)
            model_name = model_card_h4.string
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
        soup = BeautifulSoup(response.text, "html.parser")
        # print(response.text)

        container = soup.find('div', class_='gallery')
        image_tags = container.find_all("a")

        for i, image in enumerate(image_tags):
            image_url = image.get("src") or image.get("data-src")
            if not image_url:
                continue
            image_full_url = urljoin(model_url, image_url)
            if image_full_url and image_full_url.startswith('http'):
                image_urls.append({
                    "image_url": image_full_url
                })

        return image_urls
