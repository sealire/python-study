import pandas as pd


def j1():
    # 创建 DataFrame
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    })

    # 将 DataFrame 转换为 JSON 字符串
    json_str = df.to_json()

    print(json_str)


def j2():
    # 创建 DataFrame
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    })

    # 将 DataFrame 转换为 JSON 文件，指定 orient='records'
    s = df.to_json('data.json', orient='records', lines=True)
    print(s)


def j3():
    df = pd.read_json('data.json', orient='records')

    print(df.to_string())


def j4():
    # JSON 数据
    json_data = '''
    [
      {"Name": "Alice", "Age": 25, "City": "New York"},
      {"Name": "Bob", "Age": 30, "City": "Los Angeles"},
      {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]
    '''

    # 从 JSON 字符串读取数据，指定 orient='records'
    df = pd.read_json(json_data, orient='records')

    print(df)


if __name__ == "__main__":
    j4()
