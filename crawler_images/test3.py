import glob
import os
import re

from crawler_images import constants

dirs = [
    "F:\\GIT\\python-study\\crawler_images\\images\\penthouse\\page\\1",
    "F:\\GIT\\python-study\\crawler_images\\images\\penthouse\\page\\2",
    # "F:\\GIT\\python-study\\crawler_images\\images\\penthouse\\page\\3",
]

pattern = r"https://penthouse-galleries.net/galleries/\d+.html"


def get_html_files(dir):
    html_files = []
    pattern = os.path.join(dir, "*.html")
    html_files.extend(glob.glob(pattern))
    pattern = os.path.join(dir, "*.htm")
    html_files.extend(glob.glob(pattern))
    return html_files


def get_html_text(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_text = file.read()
    return html_text


def get_urls(dirs):
    urls = []
    for sub_dir in dirs:
        html_files = get_html_files(sub_dir)
        for html_file in html_files:
            html_text = get_html_text(html_file)
            matches = re.findall(pattern, html_text)
            if not matches:
                continue

            index = html_text.find("<title>")
            text = html_text[index + 7:index + 50]
            index = text.find(" - ")
            model_name = text[:index]
            model_name = re.sub(r'[?/\'|.]', '', model_name)
            model_name = model_name.strip()

            urls.append({"name": model_name, "url": matches[0]})
    return urls


def save_model_url_to_file(website_title, urls):
    website_dir = os.path.join(constants.base_dir, website_title)
    website_info_filename = f"{website_dir}/website_info.txt"
    with open(website_info_filename, "a", encoding='utf-8') as file:
        for url in urls:
            file.write(url["name"] + " [" + url["url"] + "]\r\n")


def save_urls(dirs):
    urls = get_urls(dirs)
    save_model_url_to_file('penthouse', urls)


save_urls(dirs)