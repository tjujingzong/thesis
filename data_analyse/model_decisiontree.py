import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 您已经提供的数据加载和预处理代码

# 加载数据
df = pd.read_csv('../data_analyse/data_result/00-all_data.csv')

# 分割数据为特征和目标变量
X = df.drop('avg-latency(ms)', axis=1)
y = df['avg-latency(ms)']
column_names = X.columns
# 标准化特征数据
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 分割数据为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=27)

# 训练决策树回归模型
regressor = DecisionTreeRegressor(random_state=27)
regressor.fit(X_train, y_train)

# 可视化决策树
plt.figure(figsize=(13, 15))
plot_tree(regressor, feature_names=column_names, filled=True, max_depth=2, fontsize=12)

# 保存到pic2文件夹
plt.savefig('../data_analyse/pic2/decision_tree.png')

# 打印决策树模型的参数
print("Decision Tree Parameters:")
print(f"Criterion: {regressor.criterion}")  # 划分质量的评价标准
print(f"Max Depth: {regressor.max_depth}")  # 树的最大深度
print(f"Min Samples Split: {regressor.min_samples_split}")  # 分割内部节点所需的最小样本数
print(f"Min Samples Leaf: {regressor.min_samples_leaf}")  # 叶节点上的最小样本数
print(f"Max Features: {regressor.max_features}")  # 寻找最佳分割时要考虑的特征数量

# 打印树的其他属性
print("\nTree Structure Information:")

print(f"Number of Outputs: {regressor.n_outputs_}")  # 输出的数量
print(f"Tree Depth: {regressor.tree_.max_depth}")  # 实际树的最大深度
print(f"Number of Leaves: {regressor.tree_.node_count}")  # 树中节点的总数
