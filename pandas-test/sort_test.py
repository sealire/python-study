import pandas as pd


def s1():
    # 示例数据
    data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
            'Age': [25, 30, 35, 40],
            'Salary': [50000, 60000, 70000, 80000]}

    df = pd.DataFrame(data)

    # 按照 "Age" 列的值进行降序排序
    df_sorted = df.sort_values(by='Age', ascending=False)
    print(df_sorted)


def s2():
    # 示例数据
    data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
            'Age': [25, 30, 35, 40],
            'Salary': [50000, 60000, 70000, 80000]}

    df = pd.DataFrame(data)

    # 按照行索引进行排序
    df_sorted_by_index = df.sort_index(axis=0)
    print(df_sorted_by_index)


if __name__ == "__main__":
    s2()
