import matplotlib.pyplot as plt
import matplotlib


def b1():
    a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])

    for i in a:
        print(i)


def b2():
    plt.rcParams['font.family'] = 'FangSong'  # 替换为你选择的字体

    # 创建数据
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    # 绘制折线图
    plt.plot(x, y)

    # 添加标题和标签
    plt.title('折线图示例')
    plt.xlabel('X轴')
    plt.ylabel('Y轴')

    # 显示图形
    plt.show()


if __name__ == "__main__":
    b2()
