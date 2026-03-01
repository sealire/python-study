import requests
from bs4 import BeautifulSoup

from crawler_images import constants


class Deskbabesgirls:

    def get_website_info(self):
        return {
            "title": "Deskbabesgirls",
            "url_template": "https://deskbabesgirls.com/?page={page}",
        }

    def check_page_exist(self, page_url):
        try:
            response = requests.get(page_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Page页面超时, page_url:{page_url}")
            return False
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find('div', class_='grid-cols-2')
        if not container:
            return False
        model_cards = container.find_all("a", class_='gallery-card')
        if model_cards:
            return True
        else:
            return False

    def get_models(self, page_url):
        model_list = []

        try:
            response = requests.get(page_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Page页面超时, page_url:{page_url}")
            return False
        soup = BeautifulSoup(response.text, "html.parser")

        # print(response.text)
        container = soup.find('div', class_='grid-cols-2')
        model_cards = container.find_all("a", class_='gallery-card')
        for i, model_card in enumerate(model_cards):
            # print(model_card.getText)
            # model_card_a = model_card.find("a", class_="gallery-thumb")
            model_url = model_card.get("href")
            # model_url = urljoin(page_url, model_url)
            model_name = model_card.find("img").get("alt")
            model_name = model_name.replace('/', "")
            model_name = model_name.replace('|', "")
            model_name = model_name.replace('\'', "")
            # print(model_name, '###############', model_url)
            model_list.append({"name": model_name, "url": model_url})

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

        container = soup.find('div', class_='content-section')
        image_tags = container.find_all("a", class_='photo-thumb')
        for i, image in enumerate(image_tags):
            image_url = image.get("href")
            if image_url and image_url.startswith('http'):
                image_urls.append({
                    "image_url": image_url
                })

        return image_urls
