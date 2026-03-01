import glob
import os

import requests
from bs4 import BeautifulSoup

from crawler_images import constants
from crawler_images.common import is_selected_model

local_base_dir = "F:\\GIT\\python-study\\crawler_images\\images\\PenthousePets"


class PenthousePets:

    def get_website_info(self):
        return {
            "title": "PenthousePets",
            "url_template": "https://penthouse-pets.net/{page}",
        }

    def check_page_exist(self, page, page_url):
        return page <= 26

    def get_models(self, page, page_url, model_names):
        model_list = []

        dir = local_base_dir + "\\page\\" + str(page)

        html_files = []
        pattern = os.path.join(dir, "*.html")
        html_files.extend(glob.glob(pattern))
        pattern = os.path.join(dir, "*.htm")
        html_files.extend(glob.glob(pattern))

        for index, html_file in enumerate(html_files):
            start = html_file.rfind("\\")
            end = html_file.rfind(".htm")
            model_url = html_file.replace(local_base_dir, "")
            model_list.append({"name": html_file[start + 1:end], "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, model_url):
        image_urls = []

        with open(local_base_dir + model_url, 'r',
                  encoding='utf-8') as file:
            html_text = file.read()

        soup = BeautifulSoup(html_text, "html.parser")

        container = soup.find('div', class_='space-y-6')
        grids = container.find_all('div', class_='grid')
        for index, grid in enumerate(grids):
            image_tags = grid.find_all("a")
            for i, image in enumerate(image_tags):
                image_url = image.get("href")
                if image_url and image_url.startswith('http'):
                    image_urls.append({
                        "image_url": image_url
                    })

        return image_urls
