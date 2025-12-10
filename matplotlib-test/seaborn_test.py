import seaborn as sns
import matplotlib.pyplot as plt


def s1():
    # 设置主题和颜色调色板
    sns.set_theme(style="darkgrid", palette="pastel")
    # 示例数据
    products = ["Product A", "Product B", "Product C", "Product D"]
    sales = [120, 210, 150, 180]

    # 创建柱状图
    sns.barplot(x=products, y=sales)

    # 添加标签和标题
    plt.xlabel("Products")
    plt.ylabel("Sales")
    plt.title("Product Sales by Category")

    # 显示图表
    plt.show()


if __name__ == "__main__":
    s1()
