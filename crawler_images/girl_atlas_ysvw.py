import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {"User-Agent": "Mozilla/5.0"}


class GirlAtlasYsvw:

    def get_website_info(self):
        return {
            "title": "girl-atlas-Ysvw",
            "url_template": "https://girl-atlas.xyz/tag?id=57653d1458e03930fbb7e344&p={page}",
        }

    def get_models(self, page_url):
        model_list = []

        response = requests.get(page_url, timeout=5, headers=headers)
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
            model_list.append({"name": model_name, "url": model_url})

        return model_list

    def get_model_image_urls(self, model_url):
        image_urls = []

        response = requests.get(model_url, timeout=5, headers=headers)
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
