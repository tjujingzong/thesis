import pandas as pd


def read_data():
    # 假设文件是纯文本格式，每行一个数值
    throughout_data = pd.read_csv('./redis_avg_throughout_mem.csv', header=None)
    cpi_data = pd.read_csv('./redis_cpi_mem.csv', header=None)

    return throughout_data, cpi_data


def correlation():
    throughout_data, cpi_data = read_data()

    # 创建一个布尔索引，表示非零的 CPI 数据行
    non_zero_cpi_index = cpi_data[0] != 0

    # 使用布尔索引过滤数据
    filtered_throughout_data = throughout_data[non_zero_cpi_index]
    filtered_cpi_data = cpi_data[non_zero_cpi_index]

    # 再次检查过滤后的数据长度是否一致
    if len(filtered_throughout_data) != len(filtered_cpi_data):
        print("过滤后数据长度不一致，无法计算相关性。")
        return

    # 计算相关性
    corr = filtered_throughout_data.corrwith(filtered_cpi_data.iloc[:, 0])
    return corr[0]


# 调用函数
correlation_value = correlation()
print("相关性系数 ", correlation_value)
