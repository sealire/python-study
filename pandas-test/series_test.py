import pandas as pd
import numpy as np


def s1():
    # 创建一个Series对象，指定名称为'A'，值分别为1, 2, 3, 4
    # 默认索引为0, 1, 2, 3
    series = pd.Series([1, 2, 3, 4])

    # 显示Series对象
    print(series)

    # 如果你想要显式地设置索引，可以这样做：
    custom_index = [1, 2, 3, 4]  # 自定义索引
    series_with_index = pd.Series([1, 2, 3, 4], index=custom_index, name='A')

    # 显示带有自定义索引的Series对象
    print(series_with_index)


def s2():
    a = ["Google", "Runoob", "Wiki"]
    myvar = pd.Series(a, index=["x", "y", "z"])
    print(myvar)


def s3():
    sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
    myvar = pd.Series(sites)
    print(myvar)


def s4():
    # 创建 Series
    data = [1, 2, 3, 4, 5, 6]
    index = ['a', 'b', 'c', 'd', 'e', 'f']
    s = pd.Series(data, index=index)

    # 查看基本信息
    print("索引：", s.index)
    print("数据：", s.values)
    print("数据类型：", s.dtype)
    print("前两行数据：", s.head(2))

    # 使用 map 函数将每个元素加倍
    s_doubled = s.map(lambda x: x * 2)
    print("元素加倍后：", s_doubled)

    # 计算累计和
    cumsum_s = s.cumsum()
    print("累计求和：", cumsum_s)

    # 查找缺失值（这里没有缺失值，所以返回的全是 False）
    print("缺失值判断：", s.isnull())

    # 排序
    sorted_s = s.sort_values()
    print("排序后的 Series：", sorted_s)


def s5():
    # 指定索引创建 Series
    s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])

    # 获取值
    # print(s[2])  # 获取索引为2的值
    print(s['a'])  # 返回索引标签 'a' 对应的元素

    # 获取多个值
    subset = s[1:4]  # 获取索引为1到3的值
    print(subset)

    # 索引和值的对应关系
    for index, value in s.items():
        print(f"Index: {index}, Value: {value}")

    # 使用切片语法来访问 Series 的一部分
    print(s['a':'c'])  # 返回索引标签 'a' 到 'c' 之间的元素
    print(s[:3])  # 返回前三个元素

    # 为特定的索引标签赋值
    s['a'] = 10  # 将索引标签 'a' 对应的元素修改为 10
    print(s['a'])

    del s['a']  # 删除索引标签 'a' 对应的元素
    print(s)

    s_dropped = s.drop(['b'])  # 返回一个删除了索引标签 'b' 的新 Series
    print(s_dropped)


def s6():
    s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    s2 = s * 2
    print(s2)

    filtered_series = s2[s2 > 5]  # 选择大于2的元素
    print(filtered_series)

    sq = np.sqrt(s2)  # 对每个元素取平方根
    print(sq)


def s7():
    s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    print(s.sum())  # 输出 Series 的总和
    print(s.mean())  # 输出 Series 的平均值
    print(s.max())  # 输出 Series 的最大值
    print(s.min())  # 输出 Series 的最小值
    print(s.std())  # 输出 Series 的标准差


def s8():
    s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    print(s.index)  # 获取索引
    print(s.values)  # 获取值数组
    print(s.describe())  # 获取描述统计信息
    print(s.idxmax())  # 获取最大值的索引
    print(s.idxmin())  # 获取最小值的索引

    # 其他属性和方法
    print(s.dtype)  # 数据类型
    print(s.shape)  # 形状
    print(s.size)  # 元素个数
    print(s.head())  # 前几个元素，默认是前 5 个
    print(s.tail())  # 后几个元素，默认是后 5 个
    print(s.sum())  # 求和
    print(s.mean())  # 平均值
    print(s.std())  # 标准差
    print(s.min())  # 最小值
    print(s.max())  # 最大值


if __name__ == "__main__":
    s8()
