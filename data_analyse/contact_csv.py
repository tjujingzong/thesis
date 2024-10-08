import pandas as pd

# 读取CSV文件
df1 = pd.read_csv('../data_analyse/data_result/202312211754-redis_lan.csv')
df2 = pd.read_csv('../data_analyse/data_result/202312211754-redis_sys.csv')
df3 = pd.read_csv('../data_analyse/data_result/202312211754-redis_vmstate.csv')

# df1仅保留avg-latency列
df1 = df1[['avg-latency']]
# 合并文件
combined_df = pd.concat([df2, df3, df1], axis=1)

# 将合并后的数据保存到新的CSV文件
combined_df.to_csv('../data_analyse/data_result/202312211754-all_data.csv', index=False)
