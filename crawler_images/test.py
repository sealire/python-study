import requests

from crawler_images import constants

url = "https://penthouse-galleries.net/galleries/0107.html"
response = requests.get(url, timeout=constants.http_timeout,
                                headers=constants.http_headers)

print(response.text)