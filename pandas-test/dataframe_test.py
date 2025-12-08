import pandas as pd


def df1():
    data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]

    # 创建DataFrame
    df = pd.DataFrame(data, columns=['Site', 'Age'])

    # 使用astype方法设置每列的数据类型
    df['Site'] = df['Site'].astype(str)
    df['Age'] = df['Age'].astype(float)

    print(df)


def df2():
    data = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}

    df = pd.DataFrame(data)

    print(df)


def df3():
    data = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]

    df = pd.DataFrame(data)

    print(df)


def df4():
    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }

    # 数据载入到 DataFrame 对象
    df = pd.DataFrame(data)

    # 返回第一行
    print(df.loc[0])
    # 返回第二行
    print(df.loc[1])


def df5():
    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }

    # 数据载入到 DataFrame 对象
    df = pd.DataFrame(data)

    # 返回第一行和第二行
    print(df.loc[[0, 1]])


def df6():
    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }

    df = pd.DataFrame(data, index=["day1", "day2", "day3"])

    print(df)


def df7():
    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }

    df = pd.DataFrame(data, index=["day1", "day2", "day3"])

    # 指定索引
    print(df.loc["day2"])


def df8():
    # 创建 DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df = pd.DataFrame(data)

    # 查看前两行数据
    print(df.head(2))

    # 查看 DataFrame 的基本信息
    print(df.info())

    # 获取描述统计信息
    print(df.describe())

    # 按年龄排序
    df_sorted = df.sort_values(by='Age', ascending=False)
    print(df_sorted)

    # 选择指定列
    print(df[['Name', 'Age']])

    # 按索引选择行
    print(df.iloc[1:3])  # 选择第二到第三行（按位置）

    # 按标签选择行
    print(df.loc[1:2])  # 选择第二到第三行（按标签）

    # 计算分组统计（按城市分组，计算平均年龄）
    print(df.groupby('City')['Age'].mean())

    # 处理缺失值（填充缺失值）
    df['Age'] = df['Age'].fillna(30)

    # 导出为 CSV 文件
    df.to_csv('output.csv', index=False)


def df9():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df = pd.DataFrame(data)
    # 通过列名访问
    print(df['Name'])

    # 通过属性访问
    print(df.Name)

    # 通过 .loc[] 访问
    print(df.loc[:, 'Name'])

    # 通过 .iloc[] 访问
    print(df.iloc[:, 0])  # 假设 'Column1' 是第一列

    # 访问单个元素
    print(df['Name'][0])
    print(df.loc[0, 'Name'])


def df10():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df = pd.DataFrame(data)

    new_row = pd.DataFrame([['Bym', 37, 'Tk']], columns=['Name', 'Age', 'City'])  # 创建一个只包含新行的DataFrame
    df = pd.concat([df, new_row], ignore_index=True)  # 将新行添加到原始DataFrame

    print(df)


def df11():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df = pd.DataFrame(data)

    print(df[df['Age'] > 30])

    df_dropped = df.drop('Name', axis=1)
    print(df_dropped)
    print(df)

    df_dropped = df_dropped.drop(0)
    print(df_dropped)

    df_dropped = df_dropped.reset_index(drop=True)
    print(df_dropped)

    df_dropped = df_dropped.set_index('City')
    print(df_dropped)


def df12():
    data1 = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df1 = pd.DataFrame(data1)

    data2 = {
        'Name': ['Alice Bob'],
        'Age': [50],
        'City': ['New York']
    }
    df2 = pd.DataFrame(data2)

    df3 = pd.concat([df1, df2], ignore_index=True)
    print(df3)

    # 横向合并
    df4 = pd.merge(df1, df2, on='Name')
    print(df4)


if __name__ == "__main__":
    df12()
