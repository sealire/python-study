import urllib

import requests

from crawler_images.common import get_html_by_selenium
#
# html_url = "https://deskbabesgirls.com/galleries/0011_sandra_shine.html"
# html_text = get_html_by_selenium(html_url)
# print(html_text)

headers = {
    'Referer': 'https://deskbabesgirls.com',
    'User-Agent': 'Mozilla/5.0'
}
img_url = "https://deskbabesgirls.com/images/data/c0104/full/VGI0642P010010.jpg"
urllib.request.urlretrieve(img_url, 'image.jpg')