import re

from crawler_images.common import is_selected_model, get_page_html, get_model_image_html


class Virtuagirlgirls:

    def get_website_info(self):
        return {
            "title": "Virtuagirlgirls",
            "url_template": "https://virtuagirlgirls.com/?page={page}",
        }

    def check_page_exist(self, thread_id, page, page_url):
        html_text = get_page_html(thread_id, page, page_url)
        if not html_text:
            return False
        container = html_text.find('div', class_='grid-cols-2')
        if not container:
            return False
        model_cards = container.find_all("a", class_='gallery-card')
        if model_cards:
            return True
        else:
            return False

    def get_models(self, thread_id, page, page_url, model_names):
        model_list = []
        html_text = get_page_html(thread_id, page, page_url)
        if not html_text:
            return model_list
        container = html_text.find('div', class_='grid-cols-2')
        model_cards = container.find_all("a", class_='gallery-card')
        model_count = len(model_cards)
        for index, model_card in enumerate(model_cards):
            # print(model_card.getText)
            # model_card_a = model_card.find("a", class_="gallery-thumb")
            model_url = model_card.get("href")
            # model_url = urljoin(page_url, model_url)
            model_name = model_card.find("img").get("alt")
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()
            if model_names and not is_selected_model(model_name, model_names):
                print(
                    f"忽略该model, thread_id:{thread_id}, page:{page}, model:{index + 1}/{model_count},  model_name:{model_name}")
                continue
            # model_name = model_name.replace('/', "")
            # model_name = model_name.replace('|', "")
            # model_name = model_name.replace('\'', "")
            # model_name = model_name.replace('?', "")
            # print(model_name, '###############', model_url)
            model_list.append({"name": model_name, "urls": [model_url]})

        return model_list

    def get_model_image_urls(self, thread_id, page, model_index, model_url_index, model_url):
        image_urls = []
        html_text = get_model_image_html(thread_id, page, model_index, model_url_index, model_url)
        if not html_text:
            return image_urls
        container = html_text.find('div', class_='content-section')
        image_tags = container.find_all("a", class_='photo-thumb')
        for i, image in enumerate(image_tags):
            image_url = image.get("href")
            if image_url and image_url.startswith('http'):
                image_urls.append({
                    "image_url": image_url
                })

        return image_urls
