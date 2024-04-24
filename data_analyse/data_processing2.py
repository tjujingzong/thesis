import pandas as pd

# 读取CSV文件
df = pd.read_csv('data_result/01-all_data.csv')

df.drop('L1_dcache_load_misses(%)', axis=1, inplace=True)
df.drop('block_in(blocks/s)', axis=1, inplace=True)
df.drop('block_out(blocks/s)', axis=1, inplace=True)
df.drop('system_time(%)', axis=1, inplace=True)

# 保存到新的CSV文件
df.to_csv('data_result/02-all_data.csv', index=False)
# df z-score标准化
df = (df - df.mean()) / df.std()
# df保留三位有效数字
df = df.round(3)
print(df)
