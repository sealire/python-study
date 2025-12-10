import pandas as pd


def a1():
    # 示例数据
    data = {'Department': ['HR', 'Finance', 'HR', 'IT', 'IT'],
            'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Salary': [50000, 60000, 55000, 70000, 75000]}

    df = pd.DataFrame(data)

    # 按照部门分组，并计算每个部门的平均薪资
    grouped = df.groupby('Department')['Salary'].mean()
    print(grouped)


def a2():
    # 示例数据
    data = {'Department': ['HR', 'Finance', 'HR', 'IT', 'IT'],
            'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Salary': [50000, 60000, 55000, 70000, 75000]}

    df = pd.DataFrame(data)

    # 按照部门分组，并计算每个部门的薪资的平均值和总和
    grouped_multiple = df.groupby('Department').agg({'Salary': ['mean', 'sum']})
    print(grouped_multiple)


def a3():
    # 示例数据
    data = {'Department': ['HR', 'Finance', 'HR', 'IT', 'IT'],
            'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Salary': [50000, 60000, 55000, 70000, 75000]}

    df = pd.DataFrame(data)

    # 按照部门分组后，按薪资降序排序
    grouped_sorted = df.groupby('Department').apply(lambda x: x.sort_values(by='Salary', ascending=False))
    print(grouped_sorted)


def a4():
    # 示例数据
    data = {'Department': ['HR', 'Finance', 'HR', 'IT', 'IT'],
            'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Salary': [50000, 60000, 55000, 70000, 75000]}

    df = pd.DataFrame(data)

    # 使用 pivot_table 计算每个部门的薪资平均值
    pivot_table = df.pivot_table(values='Salary', index='Department', aggfunc='mean')
    print(pivot_table)


if __name__ == "__main__":
    a4()
