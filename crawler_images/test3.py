import glob
import os

import requests
from bs4 import BeautifulSoup

from crawler_images import constants
from crawler_images.penthouse_pets import PenthousePets

c = PenthousePets()
model_list = c.get_models(1, "", "")
print(model_list)

imgs = c.get_model_image_urls('\\page\\1\\Lily Ivy.htm')
print(imgs)


# with open("F:\\GIT\\python-study\\crawler_images\\images\\PenthousePets\\page\\1\\Lily Ivy.htm", 'r',
#           encoding='utf-8') as file:
#     content = file.read()
#
# soup = BeautifulSoup(content, "html.parser")
#
# image_urls = []
#
# container = soup.find('div', class_='space-y-6')
# grids = container.find_all('div', class_='grid')
# for index, grid in enumerate(grids):
#     image_tags = grid.find_all("a")
#     for i, image in enumerate(image_tags):
#         image_url = image.get("href")
#         if image_url and image_url.startswith('http'):
#             image_urls.append({
#                 "image_url": image_url
#             })
#
# print(image_urls)
# print(len(image_urls))
#
#
# img_data = requests.get(image_urls[0]["image_url"], timeout=constants.http_timeout,
#                                     headers=constants.http_headers).content
# with open(f"F:/image_0.jpg", "wb") as f:
#     f.write(img_data)

