import pandas as pd

# Converting the string data to a dataframe
df = pd.read_csv('data_result/00-all_data.csv')

# 删除cs (context switches/s)列
df = df.drop('cs (context switches/s)', axis=1)
