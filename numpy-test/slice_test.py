import numpy as np


def s1():
    a = np.arange(5 * 5 * 6).reshape(5, 5, 6)
    print(a)
    b = a[1:4, :3, ::3]
    print(b)
    print(b.shape)


def s2():
    a = np.arange(5 * 5 * 6).reshape(5, 5, 6)
    print("a:")
    print(a)

    b = a[..., 2]
    print("a[..., 2]:")
    print(b)

    b = a[..., 2:]
    print("a[..., 2:]:")
    print(b)

    b = a[2, ...]
    print("a[2, ...]:")
    print(b)


def s3():
    x = np.array([[1, 2], [3, 4], [5, 6]])
    y = x[[0, 1, 2], [0, 1, 0]]
    print(y)

    x = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
    print('我们的数组是：')
    print(x)
    print('\n')
    rows = np.array([[0, 0], [3, 3]])
    cols = np.array([[0, 2], [0, 2]])
    y = x[rows, cols]
    print('这个数组的四个角元素是：')
    print(y)


def s4():
    a = np.arange(5 * 6).reshape(5, 6)
    mask = (a % 4 == 0) & (a > 12)
    b = a[mask]
    print(b)


def s5():
    arr = np.array([10, 20, 30, 40, 50])

    # 指定索引位置：[1]和[3]
    indices = np.array([1, 3])  # 整数数组

    # 应用花式索引：按indices顺序提取元素
    result = arr[indices]  # 输出：[20, 40]
    print("花式索引结果:", result)


def s6():
    x = np.arange(32).reshape((8, 4))
    print(x)
    # 二维数组读取指定下标对应的行
    print("-------读取下标对应的行-------")
    print(x[[4, 2, 1, 7]])


def s7():
    arr = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])

    # 目标：筛选第0行和第1行中大于25的元素
    # 步骤1：花式索引选择行（返回副本）
    rows = [0, 1]  # 选择第0行和第1行
    sub_arr = arr[rows]  # 子数组：[[10,20,30], [40,50,60]]

    # 步骤2：布尔索引筛选大于25的元素
    mask = sub_arr > 25  # 掩码：[[False,False,True], [True,True,True]]
    result = sub_arr[mask]  # 输出：[30, 40, 50, 60]

    print("组合索引结果:", result)


if __name__ == "__main__":
    s7()
