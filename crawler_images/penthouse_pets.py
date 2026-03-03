import glob
import os
import re

from bs4 import BeautifulSoup

from crawler_images.common import is_selected_model

local_base_dir = "F:\\GIT\\python-study\\crawler_images\\images\\PenthousePets"


class PenthousePets:

    def get_website_info(self):
        return {
            "title": "PenthousePets",
            "url_template": "https://penthouse-pets.net/{page}",
        }

    def check_page_exist(self, download_info):
        return download_info["current_download_info"]["page_index"] <= 26

    def get_models_in_page(self, download_info):
        model_list = []
        dir = local_base_dir + "\\page\\" + str(download_info["current_download_info"]["page_index"])
        html_files = []
        pattern = os.path.join(dir, "*.html")
        html_files.extend(glob.glob(pattern))
        pattern = os.path.join(dir, "*.htm")
        html_files.extend(glob.glob(pattern))

        for index, html_file in enumerate(html_files):
            start = html_file.rfind("\\")
            end = html_file.rfind(".htm")
            model_name = html_file[start + 1:end]
            model_name = model_name.replace('- Penthouse Galleries', "")
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            if len(model_name) > 100:
                model_name = model_name[:100]
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_url = html_file.replace(local_base_dir, "")
                model_list.append({"name": model_name, "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, download_info):
        image_urls = []
        with open(local_base_dir + download_info["current_download_info"]["model_url"], 'r', encoding='utf-8') as file:
            html_text = file.read()
        html_text = BeautifulSoup(html_text, "html.parser")
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
