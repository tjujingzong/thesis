import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
df1 = pd.read_csv('../data_analyse/data_result/02category-all_data.csv')

# 假设 df1 是你的数据框架
# df1仅保留avg-latency(ms), category列
df1 = df1[['avg-latency(ms)', 'category']]

# 定义一个字典将数字类别替换为应用名称
category_names = {
    1: 'Redis',
    2: 'MySQL',
    3: 'RabbitMQ',
    4: 'MongoDB',
    5: 'Tomcat',
    6: 'Nginx'
}

# 替换 'category' 列中的数字为具体的应用名称
df1['category'] = df1['category'].map(category_names)

# 绘制箱形图
sns.boxplot(x='category', y='avg-latency(ms)', data=df1,fliersize=3)
# 修改横坐标标签
plt.xlabel('applications')
# # 可以选择性地旋转x轴标签，以提高可读性
# plt.xticks(rotation=30)
plt.ylim(0, 30)
# 显示图形
plt.savefig('../data_analyse/pic2/02category-latency.png')
