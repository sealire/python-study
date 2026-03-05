import random
import re

from crawler_images.common import is_selected_model, get_page_html, get_model_image_html


class Sgirlsweb:

    def __init__(self, download_min_page=1, download_max_page=-1):
        self.download_min_page = download_min_page
        self.download_max_page = download_max_page

    def get_website_info(self):
        return {
            "title": "sgirlsweb",
            "url_template": "https://www.sgirlsweb.com/all-sexy-girls/{page}/",
            "max_page": 9,
            "download_min_page": self.download_min_page,
            "download_max_page": self.download_max_page,
            "independent_download_image": False,
        }

    def get_models_in_page(self, download_info):
        model_list = []
        html_text = get_page_html(download_info)
        if not html_text:
            return model_list
        container = html_text.find('ul', id='iids')
        model_cards = container.find_all("li", class_='item')
        for model_index, model_card in enumerate(model_cards):
            model_h2 = model_card.find("div", class_="item-pdat-text").find("h2")
            model_name = model_h2.get_text(strip=True)
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if is_selected_model(model_name, download_info):
                model_name_split = model_name.replace(' ', "-").lower()
                model_urls = self.get_model_urls(download_info, model_index, model_name_split)
                model_dir_name = model_name + " - " + str(random.randint(100000, 999999))
                model_list.append({"name": model_name, "dir_name": model_dir_name, "urls": model_urls})

        return model_list

    def get_model_urls(self, download_info, model_index, model_name_split):
        model_urls = []
        max_page_index = 1
        base_url = "https://www.sgirlsweb.com/girl/" + model_name_split + "/photo-gallery/"
        while True:
            max_page = self.get_max_model_image_page(download_info["thread_id"], model_index, base_url, max_page_index)
            if max_page <= max_page_index:
                break
            max_page_index = max_page
            print(f"Sgirlsweb, {model_name_split}, max_page_index:{max_page_index}")

        for page in range(1, max_page_index + 1):  # 遍历页码
            model_url = base_url + str(page) + "/"
            model_urls.append(model_url)

        return model_urls

    def get_max_model_image_page(self, thread_id, model_index, base_url, page_index):
        model_url = base_url + str(page_index) + "/"
        html_text = get_model_image_html(thread_id, page_index, model_index, page_index, model_url)
        container = html_text.find('div', class_='pages')
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

    def get_model_images(self, download_info):
        model_images = []
        html_text = get_model_image_html(download_info)
        if not html_text:
            return model_images
        container = html_text.find('ul', id='iids')
        image_tags = container.find_all("li", class_='fl-photo-item')
        for i, image in enumerate(image_tags):
            img = image.find("a", class_="athumb").find("img")
            image_url = img.get("src")
            if image_url and image_url.startswith('http'):
                # image_url = image_url.replace("static3", "static1")
                image_url = image_url.replace("thumbs-photos/480/", "thumbs-photos/1080/")
                # index = image_url.rfind("/") + 1
                # image_url = image_url[:index] + "mibogirl-" + image_url[index:]
                model_images.append({
                    "image_url": image_url.strip()
                })

        return model_images
