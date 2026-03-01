import requests
import time
import random
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
# from fake_useragent import UserAgent


class AntiAntiSpider:
    def __init__(self):
        self.session = requests.Session()
        # self.ua = UserAgent()

        # 配置重试策略
        retry_strategy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get_random_headers(self):
        """生成随机请求头"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def random_delay(self, min_delay=1, max_delay=3):
        """随机延时"""
        time.sleep(random.uniform(min_delay, max_delay))

    def get_with_retry(self, url, **kwargs):
        """带重试机制的GET请求"""
        headers = kwargs.pop('headers', self.get_random_headers())
        timeout = kwargs.pop('timeout', 10)

        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=timeout,
                **kwargs
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def post_with_retry(self, url, data=None, **kwargs):
        """带重试机制的POST请求"""
        headers = kwargs.pop('headers', self.get_random_headers())
        timeout = kwargs.pop('timeout', 10)

        try:
            response = self.session.post(
                url,
                data=data,
                headers=headers,
                timeout=timeout,
                **kwargs
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None


def main():
    # 示例使用
    spider = AntiAntiSpider()

    # 目标URL
    url = "https://penthouse-galleries.net/galleries/g02602.amp.html"

    # 发送请求
    print("正在发送请求...")
    response = spider.get_with_retry(url)

    if response and response.status_code == 200:
        print("请求成功!")
        print(f"状态码: {response.status_code}")
        print("响应内容预览:")
        print(str(response.text)[:200] + "...")
    else:
        print("请求失败!")


if __name__ == "__main__":
    main()
