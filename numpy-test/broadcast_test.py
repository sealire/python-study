import numpy as np


def bc1():
    a = np.array([1, 2, 3, 4])
    b = np.array([10, 20, 30, 40])
    c = a * b
    print(c)


def bc2():
    a = np.array([[0, 0, 0],
                  [10, 10, 10],
                  [20, 20, 20],
                  [30, 30, 30]])
    b = np.array([0, 1, 2])
    print(a + b)


if __name__ == "__main__":
    bc2()
