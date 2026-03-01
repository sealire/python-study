import re

from crawler_images.istrippergirls import Istrippergirls

image_url = "https://static3.mibogirl.com/thumbs-photos/480/melena-a/melena-a-002.jpg"
image_url = image_url.replace("thumbs-photos/480", "")
index = image_url.rfind("/")+1
image_url = image_url[:index] + "mibogirl-" + image_url[index:]
print(image_url)