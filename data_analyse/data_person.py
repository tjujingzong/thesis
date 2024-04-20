import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('data_result/01-all_data.csv')
df.drop('avg-latency(ms)', axis=1)
# 计算 Pearson 相关系数矩阵
correlation_matrix = df.corr()

# 绘制热力图
plt.figure(figsize=(15, 12))
plt.subplots_adjust(left=0.15, right=1.0, top=0.95, bottom=0.18)

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Pearson Correlation Matrix', fontsize=18)

plt.savefig('pic2/pearson_correlation_matrix.png')

# 剔除高相关性变量
# 选择一个阈值，例如0.8
threshold = 0.80
columns = correlation_matrix.columns.tolist()

# 查找高度相关的变量对
highly_correlated_pairs = []
for i in range(len(columns)):
    for j in range(i + 1, len(columns)):
        if abs(correlation_matrix.iloc[i, j]) > threshold:
            highly_correlated_pairs.append((columns[i], columns[j]))

# 打印成对的高度相关变量
print('Highly correlated variable pairs:')
for pair in highly_correlated_pairs:
    print(pair)
