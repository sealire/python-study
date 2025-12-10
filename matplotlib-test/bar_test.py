import matplotlib.pyplot as plt
import numpy as np


def b1():
    x = np.array(["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"])
    y = np.array([12, 22, 6, 18])

    plt.bar(x, y)
    plt.show()


def b2():
    x = np.array(["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"])
    y = np.array([12, 22, 6, 18])

    plt.barh(x, y, color="#4CAF50")
    plt.show()


def b3():
    x = np.array(["Runoob-1", "Runoob-2", "Runoob-3", "C-RUNOOB"])
    y = np.array([12, 22, 6, 18])

    plt.bar(x, y, color=["#4CAF50", "red", "hotpink", "#556B2F"], width=0.5)
    plt.show()


if __name__ == "__main__":
    b3()
