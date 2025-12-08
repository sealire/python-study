import numpy as np


def la1():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[11, 12], [13, 14]])
    print(np.dot(a, b))
    print(np.vdot(a, b))


def la2():
    x = np.array([[1, 2], [3, 4]])
    y = np.linalg.inv(x)  # 逆矩阵
    print(x)
    print(y)
    print(np.dot(x, y))


def la3():
    a = np.array([[1, 1, 1], [0, 2, 5], [2, 5, -1]])

    print('数组 a：')
    print(a)
    ainv = np.linalg.inv(a)

    print('a 的逆：')
    print(ainv)

    print('矩阵 b：')
    b = np.array([[6], [-4], [27]])
    print(b)

    print('计算：A^(-1)B：')
    x = np.linalg.solve(a, b)
    print(x)


if __name__ == "__main__":
    la3()
