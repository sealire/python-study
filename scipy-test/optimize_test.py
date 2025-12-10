from scipy.optimize import root
from scipy.optimize import minimize
from math import cos


def eqn1(x):
    return x + cos(x)


def eqn2(x):
    return x ** 2 + x + 2


def o1():
    myroot = root(eqn1, 0)
    print(myroot.x)
    print(myroot)


def o2():
    mymin = minimize(eqn2, 0, method='BFGS')
    print(mymin.x)
    print(mymin.fun)


if __name__ == "__main__":
    o2()
