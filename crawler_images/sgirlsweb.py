import re

import requests
from bs4 import BeautifulSoup

from crawler_images import constants
from crawler_images.common import is_selected_model


class Sgirlsweb:

    def get_website_info(self):
        return {
            "title": "Sgirlsweb",
            "url_template": "https://www.sgirlsweb.com/all-sexy-girls/{page}/",
        }

    def check_page_exist(self, page_url):
        try:
            response = requests.get(page_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Page页面超时, page_url:{page_url}")
            return False
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find('ul', id='iids')
        if not container:
            return False
        model_cards = container.find_all("li", class_='item')
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
        container = soup.find('ul', id='iids')
        model_cards = container.find_all("li", class_='item')
        for i, model_card in enumerate(model_cards):
            # print(model_card.getText)
            # model_card_a = model_card.find("a", class_="gallery-thumb")
            # model_url = urljoin(page_url, model_url)
            model_h2 = model_card.find("div", class_="item-pdat-text").find("h2")
            model_name = model_h2.get_text(strip=True)
            model_name = re.sub(r'[?/\'|]', '', model_name)
            model_name = model_name.strip()
            if model_names and not is_selected_model(model_name, model_names):
                continue

            model_name_split = model_name.replace(' ', "-").lower()
            model_urls = self.get_model_urls(model_name_split)
            # print(model_name, '###############', model_url)
            model_list.append({"name": model_name, "urls": model_urls})

        return model_list

    def get_model_urls(self, model_name_split):
        model_urls = []
        max_page_index = 1
        base_url = "https://www.sgirlsweb.com/girl/" + model_name_split + "/photo-gallery/"
        while True:
            max_page = self.get_max_model_image_page(base_url, max_page_index)
            if max_page <= max_page_index:
                break
            max_page_index = max_page

        for page in range(1, max_page_index + 1):  # 遍历页码
            model_url = base_url + str(page) + "/"
            model_urls.append(model_url)

        return model_urls

    def get_max_model_image_page(self, base_url, page_index):
        model_url = base_url + str(page_index) + "/"
        try:
            response = requests.get(model_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Model页面超时, page_url:{model_url}")
            return page_index
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find('div', class_='pages')
        if not container:
            return page_index
        lis = container.find_all("li")
        count = len(lis)
        last = lis[count - 3]
        pa = last.find("a")
        if pa:
            return int(pa.string)
        else:
            return page_index

    def get_model_image_urls(self, model_url):
        image_urls = []

        try:
            response = requests.get(model_url, timeout=constants.http_timeout, headers=constants.http_headers)
        except requests.exceptions.Timeout:
            print(f"EXCEPT-获取Model页面超时, model_url:{model_url}")
            return image_urls
        soup = BeautifulSoup(response.text, "html.parser")
        # print(response.text)

        container = soup.find('ul', id='iids')
        image_tags = container.find_all("li", class_='fl-photo-item')
        for i, image in enumerate(image_tags):
            img = image.find("a", class_="athumb").find("img")
            image_url = img.get("src")
            if image_url and image_url.startswith('http'):
                image_url = image_url.replace("static3", "static1")
                image_url = image_url.replace("thumbs-photos/480", "")
                index = image_url.rfind("/") + 1
                image_url = image_url[:index] + "mibogirl-" + image_url[index:]
                image_urls.append({
                    "image_url": image_url
                })

        return image_urls
