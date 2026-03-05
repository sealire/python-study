from crawler_images.common import save_image_by_chunk

headers = {
    'Referer': 'https://www.sgirlsweb.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36',
}

image_url = "https://static1.mibogirl.com/sybil-a/mibogirl-sybil-a-006.jpg"
save_image_by_chunk(image_url, "jpg", 1, 1, 1, "images", headers)
