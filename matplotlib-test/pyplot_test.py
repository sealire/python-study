import matplotlib.pyplot as plt
import numpy as np


def p1():
    xpoints = np.array([0, 6])
    ypoints = np.array([0, 100])

    plt.plot(xpoints, ypoints)
    plt.show()


def p2():
    x = np.arange(0, 4 * np.pi, 0.1)  # start,stop,step
    y = np.sin(x)
    z = np.cos(x)
    plt.plot(x, y, x, z)
    plt.show()


def p3():
    ypoints = np.array([1, 3, 4, 5, 8, 9, 6, 1, 3, 4, 5, 2, 4])

    plt.plot(ypoints, marker='o')
    plt.show()


def p4():
    ypoints = np.array([6, 2, 13, 10])

    plt.plot(ypoints, linestyle='dotted')
    plt.show()


def p5():
    x1 = np.array([0, 1, 2, 3])
    y1 = np.array([3, 7, 5, 9])
    x2 = np.array([0, 1, 2, 3])
    y2 = np.array([6, 2, 13, 10])

    plt.plot(x1, y1, x2, y2)
    plt.show()


def p6():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 4, 9, 16, 25])
    plt.plot(x, y)

    plt.title("RUNOOB TEST TITLE")
    plt.xlabel("x - label", loc="left")
    plt.ylabel("y - label", loc="top")

    plt.show()


def p7():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 4, 9, 16, 25])

    plt.title("RUNOOB grid() Test")
    plt.xlabel("x - label")
    plt.ylabel("y - label")

    plt.plot(x, y)

    plt.grid(color='r', linestyle='--', linewidth=0.5)

    plt.show()


def p8():
    # plot 1:
    xpoints = np.array([0, 6])
    ypoints = np.array([0, 100])

    plt.subplot(1, 2, 1)
    plt.plot(xpoints, ypoints)
    plt.title("plot 1")

    # plot 2:
    x = np.array([1, 2, 3, 4])
    y = np.array([1, 4, 9, 16])

    plt.subplot(1, 2, 2)
    plt.plot(x, y)
    plt.title("plot 2")

    plt.suptitle("RUNOOB subplot Test")
    plt.show()


def p9():
    # plot 1:
    x = np.array([0, 6])
    y = np.array([0, 100])

    plt.subplot(2, 2, 1)
    plt.plot(x, y)
    plt.title("plot 1")

    # plot 2:
    x = np.array([1, 2, 3, 4])
    y = np.array([1, 4, 9, 16])

    plt.subplot(2, 2, 2)
    plt.plot(x, y)
    plt.title("plot 2")

    # plot 3:
    x = np.array([1, 2, 3, 4])
    y = np.array([3, 5, 7, 9])

    plt.subplot(2, 2, 3)
    plt.plot(x, y)
    plt.title("plot 3")

    # plot 4:
    x = np.array([1, 2, 3, 4])
    y = np.array([4, 5, 6, 7])

    plt.subplot(2, 2, 4)
    plt.plot(x, y)
    plt.title("plot 4")

    plt.suptitle("RUNOOB subplot Test")
    plt.show()


def p10():
    # 创建一些测试数据 -- 图1
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)

    # 创建一个画像和子图 -- 图2
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Simple plot')

    # 创建两个子图 -- 图3
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.plot(x, y)
    ax1.set_title('Sharing Y axis')
    ax2.scatter(x, y)

    # 创建四个子图 -- 图4
    fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
    axs[0, 0].plot(x, y)
    axs[1, 1].scatter(x, y)

    # 共享 x 轴
    plt.subplots(2, 2, sharex='col')

    # 共享 y 轴
    plt.subplots(2, 2, sharey='row')

    # 共享 x 轴和 y 轴
    plt.subplots(2, 2, sharex='all', sharey='all')

    # 这个也是共享 x 轴和 y 轴
    plt.subplots(2, 2, sharex=True, sharey=True)

    # 创建标识为 10 的图，已经存在的则删除
    fig, ax = plt.subplots(num=10, clear=True)

    plt.show()


if __name__ == "__main__":
    p10()
