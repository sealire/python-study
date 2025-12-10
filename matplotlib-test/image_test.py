import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def img1():
    # 生成一个二维随机数组
    img = np.random.rand(10, 10)

    # 绘制灰度图像
    plt.imshow(img, cmap='gray')

    # 显示图像
    plt.show()


def img2():
    # 生成一个随机的彩色图像
    img = np.random.rand(10, 10, 3)

    # 绘制彩色图像
    plt.imshow(img)

    # 显示图像
    plt.show()


def img3():
    # 生成一个二维随机数组
    data = np.random.rand(10, 10)

    # 绘制热力图
    plt.imshow(data, cmap='hot')

    # 显示图像
    plt.colorbar()
    plt.show()


def img4():
    # 加载地图图像, 下载地址：https://static.jyshare.com/images/demo/map.jpeg
    img = Image.open('map.jpeg')

    # 转换为数组
    data = np.array(img)

    # 绘制地图
    plt.imshow(data)

    # 隐藏坐标轴
    plt.axis('off')

    # 显示图像
    plt.show()


def img5():
    n = 4

    # 创建一个 n x n 的二维numpy数组
    a = np.reshape(np.linspace(0, 1, n ** 2), (n, n))

    plt.figure(figsize=(12, 4.5))

    # 第一张图展示灰度的色彩映射方式，并且没有进行颜色的混合
    plt.subplot(131)
    plt.imshow(a, cmap='gray', interpolation='nearest')
    plt.xticks(range(n))
    plt.yticks(range(n))
    # 灰度映射，无混合
    plt.title('Gray color map, no blending', y=1.02, fontsize=12)

    # 第二张图展示使用viridis颜色映射的图像，同样没有进行颜色的混合
    plt.subplot(132)
    plt.imshow(a, cmap='viridis', interpolation='nearest')
    plt.yticks([])
    plt.xticks(range(n))
    # Viridis映射，无混合
    plt.title('Viridis color map, no blending', y=1.02, fontsize=12)

    # 第三张图展示使用viridis颜色映射的图像，并且使用了双立方插值方法进行颜色混合
    plt.subplot(133)
    plt.imshow(a, cmap='viridis', interpolation='bicubic')
    plt.yticks([])
    plt.xticks(range(n))
    # Viridis 映射，双立方混合
    plt.title('Viridis color map, bicubic blending', y=1.02, fontsize=12)

    plt.show()


def img6():
    img_array = plt.imread('tiger.jpeg')
    tiger = img_array / 255
    # print(tiger)

    # 显示图像
    plt.figure(figsize=(10, 6))

    for i in range(1, 5):
        plt.subplot(2, 2, i)
        x = 1 - 0.2 * (i - 1)
        plt.axis('off')  # hide coordinate axes
        plt.title('x={:.1f}'.format(x))
        plt.imshow(tiger * x)

    plt.show()


def img7():
    img_array = plt.imread('tiger.jpeg')
    tiger = img_array / 255
    # print(tiger)

    # 显示图像
    plt.figure(figsize=(6, 6))
    plt.imshow(tiger[:300, 100:400, :])
    plt.axis('off')
    plt.show()


def img8():
    img_array = plt.imread('tiger.jpeg')
    tiger = img_array / 255
    # print(tiger)

    # 显示图像
    red_tiger = tiger.copy()

    red_tiger[:, :, [1, 2]] = 0

    plt.figure(figsize=(10, 10))
    plt.imshow(red_tiger)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    img8()
