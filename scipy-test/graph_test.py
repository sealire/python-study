import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.sparse.csgraph import floyd_warshall
from scipy.sparse.csgraph import bellman_ford


def g1():
    arr = np.array([
        [0, 1, 2],
        [1, 0, 0],
        [2, 0, 0]
    ])

    newarr = csr_matrix(arr)

    print(connected_components(newarr))


def g2():
    arr = np.array([
        [0, 1, 2],
        [1, 0, 0],
        [2, 0, 0]
    ])

    newarr = csr_matrix(arr)
    # Dijkstra(迪杰斯特拉)最短路径算法，用于计算一个节点到其他所有节点的最短路径。
    print(dijkstra(newarr, return_predecessors=True, indices=2))


def g3():
    arr = np.array([
        [0, 1, 2],
        [1, 0, 0],
        [2, 0, 0]
    ])

    newarr = csr_matrix(arr)
    # 弗洛伊德算法算法是解决任意两点间的最短路径的一种算法。
    print(floyd_warshall(newarr, return_predecessors=True))


def g4():
    arr = np.array([
        [0, -1, 2],
        [1, 0, 0],
        [2, 0, 0]
    ])

    newarr = csr_matrix(arr)
    # 贝尔曼-福特算法是解决任意两点间的最短路径的一种算法。
    print(bellman_ford(newarr, return_predecessors=True, indices=0))


if __name__ == "__main__":
    g4()
