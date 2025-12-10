import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def p1():
    # 示例数据
    data = {'Year': [2015, 2016, 2017, 2018, 2019, 2020],
            'Sales': [100, 150, 200, 250, 300, 350]}
    df = pd.DataFrame(data)

    # 绘制折线图
    df.plot(kind='line', x='Year', y='Sales', title='Sales Over Years', xlabel='Year', ylabel='Sales', figsize=(10, 6))
    plt.show()


def p2():
    # 示例数据
    data = {'Category': ['A', 'B', 'C', 'D'],
            'Value': [10, 15, 7, 12]}
    df = pd.DataFrame(data)

    # 绘制柱状图
    df.plot(kind='bar', x='Category', y='Value', title='Category Values', xlabel='Category', ylabel='Value',
            figsize=(8, 5))
    plt.show()


def p3():
    # 示例数据
    data = {'Height': [150, 160, 170, 180, 190],
            'Weight': [50, 60, 70, 80, 90]}
    df = pd.DataFrame(data)

    # 绘制散点图
    df.plot(kind='scatter', x='Height', y='Weight', title='Height vs Weight', xlabel='Height (cm)',
            ylabel='Weight (kg)', figsize=(8, 5))
    plt.show()


def p4():
    # 示例数据
    data = {'Scores': [55, 70, 85, 90, 60, 75, 80, 95, 100, 65]}
    df = pd.DataFrame(data)

    # 绘制直方图
    df.plot(kind='hist', y='Scores', bins=5, title='Scores Distribution', xlabel='Scores', figsize=(8, 5))
    plt.show()


def p5():
    # 示例数据
    data = {'Scores': [55, 70, 85, 90, 60, 75, 80, 95, 100, 65]}
    df = pd.DataFrame(data)

    # 绘制箱线图
    df.plot(kind='box', title='Scores Boxplot', ylabel='Scores', figsize=(8, 5))
    plt.show()


def p6():
    # 示例数据
    data = {'Category': ['A', 'B', 'C', 'D'],
            'Value': [10, 15, 7, 12]}
    df = pd.DataFrame(data)

    # 绘制饼图
    df.plot(kind='pie', y='Value', labels=df['Category'], autopct='%1.1f%%', title='Category Proportions',
            figsize=(8, 5))
    plt.show()


def p7():
    # 示例数据
    data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
    df = pd.DataFrame(data)

    # 绘制热力图
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.show()


def p8():
    # 示例数据
    data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
    df = pd.DataFrame(data)

    sns.pairplot(df)
    plt.show()


def p9():
    # 示例数据
    data = {'Year': [2015, 2016, 2017, 2018, 2019],
            'Sales': [100, 150, 200, 250, 300]}
    df = pd.DataFrame(data)

    # 绘制折线图
    plt.plot(df['Year'], df['Sales'], color='blue', marker='o')

    # 自定义
    plt.title('Sales Over Years')
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.grid(True)

    # 显示
    plt.show()


if __name__ == "__main__":
    p9()
