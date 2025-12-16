import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def linear_test_1():
    # 假设我们有一个简单的房价数据集
    data = {
        '面积': [50, 60, 80, 100, 120],
        '房价': [150, 180, 240, 300, 350]
    }
    df = pd.DataFrame(data)

    # 特征和标签
    X = df[['面积']]
    y = df['房价']

    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(pd.DataFrame({
        '面积': [50, 140]
    }))

    print(f"预测的房价: {y_pred}")


def logistic_test_1():
    # 加载鸢尾花数据集
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 只取前两类做二分类任务
    X = X[y != 2]
    y = y[y != 2]

    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练逻辑回归模型
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)

    # 评估模型
    print(f"分类准确率: {accuracy_score(y_test, y_pred):.2f}")


def svm_test_1():
    # 加载鸢尾花数据集
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 训练 SVM 模型
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)

    # 评估模型
    print(f"SVM 分类准确率: {accuracy_score(y_test, y_pred):.2f}")


def tree_test_1():
    # 加载鸢尾花数据集
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 训练决策树模型
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)

    # 评估模型
    print(f"决策树分类准确率: {accuracy_score(y_test, y_pred):.2f}")


def k_means_test_1():
    # 生成一个简单的二维数据集
    X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

    # 训练 K-means 模型
    model = KMeans(n_clusters=4)
    model.fit(X)

    # 预测聚类结果
    y_kmeans = model.predict(X)
    print(y_kmeans)

    # 可视化聚类结果
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
    plt.show()


def pca_test_1():
    # 加载鸢尾花数据集
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 降维到 2 维
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # 可视化结果
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
    plt.title('PCA of Iris Dataset')
    plt.show()


if __name__ == "__main__":
    pca_test_1()
