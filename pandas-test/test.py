import pandas as pd

if __name__ == "__main__":
    data = {'name': ['google', 'baidu'], 'age': [10, 20]}
    df = pd.DataFrame(data)
    print(df)

    series_apples = pd.Series([1, 3, 7, 4])
    series_bananas = pd.Series([2, 6, 3, 5])

    # 将两个Series对象相加，得到DataFrame，并指定列名
    df = pd.DataFrame({'Apples': series_apples, 'Bananas': series_bananas})

    # 显示DataFrame
    print(df)