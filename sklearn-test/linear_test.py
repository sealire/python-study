import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def l1():
    # 生成一些随机数据
    np.random.seed(0)
    x = 2 * np.random.rand(100, 1)
    y = 4 + 3 * x + np.random.randn(100, 1)

    # 创建线性回归模型
    model = LinearRegression()

    # 拟合模型
    model.fit(x, y)

    # 输出模型的参数
    print(f"斜率 (w): {model.coef_[0][0]}")
    print(f"截距 (b): {model.intercept_[0]}")

    # 预测
    y_pred = model.predict(x)

    # 可视化拟合结果
    plt.scatter(x, y)
    plt.plot(x, y_pred, color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linear Regression Fit')
    plt.show()


if __name__ == "__main__":
    l1()
