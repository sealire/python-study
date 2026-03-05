import glob
import os
import random
import re

from bs4 import BeautifulSoup

from crawler_images.common import is_selected_model
from crawler_images.constants import project_dir


class Penthouse:

    def __init__(self, download_min_page=1, download_max_page=-1):
        self.website_title = "penthouse"
        self.local_base_dir = project_dir + "\\images\\" + self.website_title
        self.download_min_page = download_min_page
        self.download_max_page = download_max_page

    def get_website_info(self):
        return {
            "title": self.website_title,
            "url_template": "https://penthouse-galleries.net/penthouse_galleries_{page}.html",
            "max_page": 26,
            "download_min_page": self.download_min_page,
            "download_max_page": self.download_max_page,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        dir = self.local_base_dir + "\\page\\" + str(download_info["current_download_info"]["page_index"])
        html_files = []
        pattern = os.path.join(dir, "*.html")
        html_files.extend(glob.glob(pattern))
        pattern = os.path.join(dir, "*.htm")
        html_files.extend(glob.glob(pattern))

        for index, html_file in enumerate(html_files):
            start = html_file.rfind("\\")
            end = html_file.rfind(".htm")
            model_name = html_file[start + 1:end]
            index = model_name.find(" - ")
            model_name = model_name[:index]
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_url = html_file.replace(self.local_base_dir, "")
                model_dir_name = model_name + " - " + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": [model_url]})

        return model_list

    def get_model_images(self, download_info):
        model_images = []
        with open(self.local_base_dir + download_info["current_download_info"]["model_url"], 'r', encoding='utf-8') as file:
            html_text = file.read()
        html_text = BeautifulSoup(html_text, "html.parser")
        container = html_text.find('div', class_='space-y-6')
        grids = container.find_all('div', class_='grid')
        for index, grid in enumerate(grids):
            image_tags = grid.find_all("a")
            for i, image in enumerate(image_tags):
                image_url = image.get("href")
                if image_url and image_url.startswith('http'):
                    model_images.append({
                        "image_url": image_url.strip()
                    })

        return model_images
