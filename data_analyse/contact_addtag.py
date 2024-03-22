import pandas as pd

# 读取CSV文件
df1 = pd.read_csv('../data_analyse/data_result/202402011709-tomcat-all_data.csv')
df2 = pd.read_csv('../data_analyse/data_result/202403201652-mongo-all_data.csv')
df3 = pd.read_csv('../data_analyse/data_result/202403211137-rabbitmq-all_data.csv')
df4 = pd.read_csv('../data_analyse/data_result/redis-all_data-3.csv')

# # 为每个DataFrame添加category列，这里用各自的文件名作为标识
df1['category'] = 1
df2['category'] = 2
df3['category'] = 3
df4['category'] = 4

# 使用pd.concat合并DataFrame，并设置ignore_index=True以便重新索引
combined_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# 将合并后的数据保存到新的CSV文件
combined_df.to_csv('../data_analyse/data_result/01category-all_data.csv', index=False)
