import numpy as np
from scipy.sparse import csr_matrix


def s1():
    arr = np.array([0, 0, 0, 0, 0, 1, 1, 0, 2])
    print(csr_matrix(arr))


def s2():
    arr = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 2]])
    print(csr_matrix(arr).data)


def s3():
    arr = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 2]])
    print(csr_matrix(arr).count_nonzero())


def s4():
    arr = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 2]])

    mat = csr_matrix(arr)
    print(mat)

    mat.eliminate_zeros()
    print(mat)


def s5():
    arr = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 2]])
    newarr = csr_matrix(arr).tocsc()
    print(newarr)


if __name__ == "__main__":
    s5()
