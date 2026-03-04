import re
from urllib.parse import urljoin

from crawler_images.common import get_page_html, get_model_image_html, is_selected_model


class Deskbabes:

    def get_website_info(self):
        return {
            "title": "deskbabes",
            "url_template": "https://deskbabesgirls.com/?page={page}",
            "max_page": 14,
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
                model_url = urljoin(download_info["current_download_info"]["page_url"], model_url)
                model_list.append({"name": model_name, "urls": [model_url]})


        return model_list

    def get_model_image_urls(self, download_info):
        image_urls = []
        html_text = get_model_image_html(download_info)
        if not html_text:
            return image_urls
        container = html_text.find('div', class_='content-section')
        image_tags = container.find_all("a", class_='photo-thumb')
        for i, image in enumerate(image_tags):
            image_url = image.get("href")
            if image_url and image_url.startswith('http'):
                image_urls.append({
                    "image_url": image_url.strip()
                })

        return image_urls
