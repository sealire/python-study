base_dir = "images"  # 图片目录
project_dir = "F:\\GIT\\python-study\\crawler_images"

http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
}
http_headers_2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}
http_headers_img = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'https://static1.mibogirl.com'
}
http_timeout = 30

download_info_template = {
    "thread_id": 1,
    "website_downloader": "website_downloader",
    "selected_model_names": "selected_model_names",
    "website_info": {
        "title": "website_title",
        "url_template": "https://url_template",
        "max_page": 10,
        "download_min_page": 1,
        "download_max_page": 10,
    },
    "current_download_info": {
        "page_index": 1,
        "page_url": "page_url",
        "model_index_in_page": 1,
        "model_count_in_page": 20,
        "model_info": {
            "dir": "model_dir",
            "name": "model_name",
            "dir_name": "dir_name",
            "urls": "model_urls"
        },
        "model_url_index": 1,
        "model_url_count": 10,
        "model_url": "model_url",
        "model_image_urls": [],
    },
}
