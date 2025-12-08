import pandas as pd


def c1():
    # 三个字段 name, site, age
    nme = ["Google", "Runoob", "Taobao", "Wiki"]
    st = ["www.google.com", "www.runoob.com", "www.taobao.com", "www.wikipedia.org"]
    ag = [90, 40, 80, 98]

    # 字典
    dict = {'name': nme, 'site': st, 'age': ag}

    df = pd.DataFrame(dict)

    # 保存 dataframe
    df.to_csv('site.csv', index=False, mode='a', header=False)


def c2():
    df = pd.read_csv('site.csv', sep=',', header=0, names=['name', 'site', 'age'],
                     dtype={'name': str, 'site': str, 'age': int})
    print(df.head())
    print(df.info())


if __name__ == "__main__":
    c2()
