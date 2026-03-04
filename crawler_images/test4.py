import requests
import urllib.request
from urllib.parse import urljoin
import os
import time
from typing import Optional


def download_image_with_requests(url: str, save_path: str, headers: dict = None) -> bool:
    """
    使用requests模拟浏览器下载图片

    Args:
        url: 图片URL
        save_path: 保存路径
        headers: 自定义请求头

    Returns:
        bool: 是否下载成功
    """
    try:
        # 默认请求头模拟浏览器
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        if headers:
            default_headers.update(headers)

        response = requests.get(url, headers=default_headers, timeout=30)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"requests下载失败: {e}")
        return False


def download_image_with_urllib(url: str, save_path: str, headers: dict = None) -> bool:
    """
    使用urllib模拟浏览器下载图片

    Args:
        url: 图片URL
        save_path: 保存路径
        headers: 自定义请求头

    Returns:
        bool: 是否下载成功
    """
    try:
        # 创建请求对象
        req = urllib.request.Request(url)

        # 设置默认请求头
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        if headers:
            default_headers.update(headers)

        for key, value in default_headers.items():
            req.add_header(key, value)

        # 发送请求并保存文件
        response = urllib.request.urlopen(req)
        with open(save_path, 'wb') as f:
            f.write(response.read())
        return True
    except Exception as e:
        print(f"urllib下载失败: {e}")
        return False


def smart_download_image(url: str, save_path: str, referer: str = None) -> bool:
    """
    智能下载图片，自动尝试多种方法

    Args:
        url: 图片URL
        save_path: 保存路径
        referer: 来源页面地址

    Returns:
        bool: 是否下载成功
    """
    # 确保保存目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 构造请求头
    headers = {}
    if referer:
        headers['Referer'] = referer

    print(f"正在尝试下载: {url}")

    # 方法1: 使用requests下载
    print("尝试使用requests下载...")
    if download_image_with_requests(url, save_path, headers):
        print(f"✓ 成功下载到: {save_path}")
        return True

    # 方法2: 使用urllib下载
    print("尝试使用urllib下载...")
    temp_path = save_path + ".temp"
    if download_image_with_urllib(url, temp_path, headers):
        os.rename(temp_path, save_path)
        print(f"✓ 成功下载到: {save_path}")
        return True
    else:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # 方法3: 添加更多请求头重试
    print("尝试添加更多请求头...")
    extended_headers = {
        'Referer': referer or url,
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    if download_image_with_requests(url, save_path, extended_headers):
        print(f"✓ 成功下载到: {save_path}")
        return True

    print("✗ 所有下载方法均失败")
    return False


def batch_download_images(urls: list, save_dir: str, delay: float = 1.0) -> dict:
    """
    批量下载图片

    Args:
        urls: 图片URL列表
        save_dir: 保存目录
        delay: 下载间隔时间(秒)

    Returns:
        dict: 下载结果统计
    """
    results = {'success': 0, 'failed': 0, 'details': []}

    for i, url in enumerate(urls):
        try:
            # 从URL提取文件名
            filename = url.split('/')[-1].split('?')[0] or f'image_{i}.jpg'
            save_path = os.path.join(save_dir, filename)

            # 下载图片
            success = smart_download_image(url, save_path)

            if success:
                results['success'] += 1
            else:
                results['failed'] += 1

            results['details'].append({
                'url': url,
                'path': save_path,
                'success': success
            })

            # 延时避免被封IP
            if i < len(urls) - 1:
                time.sleep(delay)

        except Exception as e:
            results['failed'] += 1
            results['details'].append({
                'url': url,
                'error': str(e),
                'success': False
            })

    return results


def main():
    """主函数 - 示例用法"""
    print("=== 图片下载工具 ===\n")

    # 单张图片下载示例
    test_urls = [
        "https://deskbabesgirls.com/images/data/f0106/full/VGI1088P040019.jpg"
    ]

    save_directory = "./downloaded_images"

    print("开始批量下载测试图片...")
    results = batch_download_images(test_urls, save_directory, delay=1.0)

    print("\n=== 下载完成 ===")
    print(f"成功: {results['success']} 张")
    print(f"失败: {results['failed']} 张")

    # 显示详细结果
    print("\n详细信息:")
    for detail in results['details']:
        status = "✓" if detail['success'] else "✗"
        print(f"{status} {detail.get('url', 'Unknown')} -> {detail.get('path', 'N/A')}")


if __name__ == "__main__":
    main()
