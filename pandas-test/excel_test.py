import pandas as pd


def e1():
    # 创建一个简单的 DataFrame
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    })

    # 将 DataFrame 写入 Excel 文件，写入 'Sheet1' 表单
    df.to_excel('output.xlsx', sheet_name='Sheet1', index=False)


def e2():
    df = pd.read_excel('output.xlsx', sheet_name=['Sheet1', 'Sheet2'])

    # 打印读取的 DataFrame
    print(df)


def e3():
    # 创建一个简单的 DataFrame
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    })

    # 写入多个表单，使用 ExcelWriter
    with pd.ExcelWriter('output.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        df.to_excel(writer, sheet_name='Sheet2', index=False)


def e4():
    # 使用 ExcelFile 加载 Excel 文件
    excel_file = pd.ExcelFile('output.xlsx')

    # 查看所有表单的名称
    print(excel_file.sheet_names)

    # 读取指定的表单
    df = excel_file.parse('Sheet1')
    print(df)

    # 关闭文件
    excel_file.close()


if __name__ == "__main__":
    e4()
