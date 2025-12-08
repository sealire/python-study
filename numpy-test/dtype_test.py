import numpy as np


def dt1():
    dt = np.dtype(np.int32)
    print(dt)

    dt = np.dtype('i4')
    print(dt)


def dt2():
    dt = np.dtype([('age', np.int8)])
    a = np.array([(10,), (20,), (30,)], dtype=dt)
    print(a)
    print(a['age'])


def dt3():
    student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
    a = np.array([('abc', 21, 50), ('xyz', 18, 75)], dtype=student)
    print(a)
    print(a['name'])
    print(a['age'])
    print(a['marks'])


if __name__ == "__main__":
    dt3()
