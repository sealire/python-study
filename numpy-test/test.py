import numpy as np


def np1():
    a = np.array([1, 2, 3], ndmin=2)
    print(type(a))
    print(a)


def np2():
    a = np.array([1, 2, 3], dtype=complex)
    print(a)

    a = np.array([(1, 2), (3, 4)], dtype=complex)
    print(a)

    print(a.ndim)
    print(a.shape)
    print(a.size)
    print(a.itemsize)
    print(a.dtype)
    print(a.flags)
    print(a.real)
    print(a.imag)
    print(a.data)

def np3():
    a = np.arange(24)
    b = a.reshape(2, 3, 4)
    print(a)
    print(b)

def np4():
    a = np.linspace(1, 88, 30)
    print(a)
    print(a.reshape(2, 3, 5))


if __name__ == "__main__":
    np4()
    print (np.var([1,2,3,4]))