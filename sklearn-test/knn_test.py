import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score


def k1():
    # 加载Iris数据集
    iris = datasets.load_iris()
    X = iris.data[:, :2]  # 只取前两个特征，便于可视化
    y = iris.target

    # 将数据集拆分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 创建KNN模型，设置K值为3
    knn = KNeighborsClassifier(n_neighbors=3)

    # 训练模型
    knn.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = knn.predict(X_test)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print(f"KNN模型的准确率: {accuracy:.4f}")

    # 绘制决策边界和数据点
    h = .02  # 网格步长
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

    # 创建一个二维网格，表示不同的样本空间
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # 使用KNN模型预测网格中的每个点的类别
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制决策边界
    plt.contourf(xx, yy, Z, alpha=0.8)

    # 绘制训练数据点
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', marker='o', s=50)
    plt.title("KNN Demo")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()


def k2():
    # 生成示例数据
    X = np.random.rand(300, 1) * 10
    y = np.sin(X).ravel() + 0.1 * np.random.randn(300)

    # 拆分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 创建KNN回归模型
    knn_reg = KNeighborsRegressor(n_neighbors=5)

    # 训练模型
    knn_reg.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = knn_reg.predict(X_test)

    # 可视化回归结果
    plt.scatter(X_test, y_test, color='red', label='True Values')
    plt.scatter(X_test, y_pred, color='blue', label='Predicted Values')
    plt.title("KNN Regression")
    plt.xlabel("Feature")
    plt.ylabel("Target")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    k2()
