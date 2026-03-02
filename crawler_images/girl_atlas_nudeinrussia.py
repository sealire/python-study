import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from crawler_images import constants
from crawler_images.common import is_selected_model, get_page_html, get_model_image_html


class GirlAtlasNudeInRussia:

    def get_website_info(self):
        return {
            "title": "girl-atlas-NudeInRussia",
            "url_template": "https://girl-atlas.xyz/tag?id=6724be52bbdf7a4d7370e1a8&p={page}",
        }

    def check_page_exist(self, thread_id, page, page_url):
        html_text = get_page_html(thread_id, page, page_url)
        if not html_text:
            return False
        container = html_text.find('div', id='div-tag')
        if not container:
            return False
        model_cards = container.find_all("div", class_='card-body')
        if model_cards:
            return True
        else:
            return False

    def get_models(self, thread_id, page, page_url, model_names):
        model_list = []
        html_text = get_page_html(thread_id, page, page_url)
        if not html_text:
            return model_list
        container = html_text.find('div', id='div-tag')
        model_cards = container.find_all("div", class_='card-body')
        model_count = len(model_cards)
        for index, model_card in enumerate(model_cards):
            # print(model_card.getText)
            model_card_h4 = model_card.find("h4").find("a")
            model_url = model_card_h4.get("href")
            model_url = urljoin(page_url, model_url)
            model_name = model_card_h4.string
            if model_names and not is_selected_model(model_name, model_names):
                print(
                    f"忽略该model, thread_id:{thread_id}, page:{page}, model:{index + 1}/{model_count},  model_name:{model_name}")
                continue
            # print(model_name, '###############', model_url)
            model_list.append({"name": model_name, "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, thread_id, page, model_index, model_url_index, model_url):
        image_urls = []
        html_text = get_model_image_html(thread_id, page, model_index, model_url_index, model_url)
        if not html_text:
            return image_urls
        container = html_text.find('div', class_='gallery')
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
