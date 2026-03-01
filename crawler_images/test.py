import asyncio
import socket
import ssl
import subprocess
import urllib

import aiohttp
import httpx
import requests
from aiohttp import TCPConnector, ClientSession

from crawler_images import constants
from crawler_images.common import is_selected_model

headers = {
    'Host': 'penthouse-galleries.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0',
    'Connection': 'close',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Connection': 'keep-alive',
    # 'Cookie': '__cf_bm=hAzf7TldUcTP7_uf.ftn6EGF4TisGgKUCu7o31VrYnU-1772268083-1.0.1.1-uzNLpPiUbZc46ooByzjk5Bo8La5GlMu0cwMrEOgorf_i1DQM1p2QoddHYsObUnc9V1rN0ORl4hVTTCyrjt6ffdF2AP6Ubrp7NTgOidX4Sgc; _ga_XQ5W8NM8X4=GS2.1.s1772267093$o1$g1$t1772268117$j30$l0$h0; _ga=GA1.1.335059061.1772267093',
    # "Upgrade-Insecure-Requests": "1",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "If-Modified-Since": "Mon, 09 Feb 2026 10:57:56 GMT",
    # "Priority": "u=0, i",
    # 'etag': '2bea7d2734e3e333096e8da52e3efe6e',  # 清除条件请求头
    # 'If-None-Match': '',  # 清除条件请求头
    # 'Cache-Control': 'no-cache',
    # 'Pragma': 'no-cache',
}


def test_url(url):
    response = requests.get(url, timeout=(60, 60), headers=headers, verify=False)
    print(response.text)


def test_urllib(url):
    socket.setdefaulttimeout(20)
    request = urllib.request.urlopen(url)
    c = request.read()
    request.close()


def test_httpx(url):
    client = httpx.Client(timeout=60, headers=headers, http2=True, follow_redirects=True, verify=False)
    response = client.get(url, timeout=60, headers=headers)
    print(response.text)


def test_curl(url):
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    print(result)


async def fetch_http3_page(url):
    """
    使用aiohttp获取HTTP/3页面内容
    """
    try:
        # 创建支持HTTP/3的连接器
        connector = TCPConnector(
            use_dns_cache=False,
            ttl_dns_cache=300,
        )

        # 创建客户端会话
        async with ClientSession(connector=connector) as session:
            # 发送GET请求
            async with session.get(url, ssl=False) as response:
                # 获取响应内容
                content = await response.text()
                print(f"状态码: {response.status}")
                print(f"URL: {response.url}")
                print(f"内容类型: {response.content_type}")
                print("-" * 50)
                print(content[:500] + "..." if len(content) > 500 else content)
                return content
    except Exception as e:
        print(f"请求失败: {e}")
        return None


async def fetch(session, url):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with session.get(url, ssl=ssl_context) as response:
        return await response.text()


async def get(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        print(html)


async def fetch_http3_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=True) as resp:
            status = resp.status
            content = await resp.text()
            print(f"Status: {status}")
            print(f"Content: {content[:100]}...")  # 打印前100个字符的内容


if __name__ == "__main__":
    test_url("https://deskbabesgirls.com/galleries/0708_lucy_li.html")
    # test_url("https://penthouse-pets.net/2")

    # asyncio.run(get("https://penthouse-galleries.net/galleries/0028.html"))
