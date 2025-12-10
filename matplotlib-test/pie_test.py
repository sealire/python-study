import matplotlib.pyplot as plt
import numpy as np


def p1():
    y = np.array([35, 25, 25, 15])

    plt.pie(y)
    plt.show()


def p2():
    # 数据
    sizes = [15, 30, 45, 10]

    # 饼图的标签
    labels = ['A', 'B', 'C', 'D']

    # 饼图的颜色
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

    # 突出显示第二个扇形
    explode = (0, 0.1, 0, 0)

    # 绘制饼图
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)

    # 标题
    plt.title("RUNOOB Pie Test")

    # 显示图形
    plt.show()


if __name__ == "__main__":
    p2()
