import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
import matplotlib.pyplot as plt
import seaborn as sns  # 使用Seaborn来增强绘图效果

# 数据导入
df = pd.read_csv('../data_analyse/data_result/02-all_data.csv')

# 数据预处理
X = df.drop('avg-latency(ms)', axis=1)
column_names = X.columns
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df['avg-latency(ms)']

# 数据划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=27)

# 模型定义和训练
model = AdaBoostRegressor(base_estimator=DecisionTreeRegressor())
model.fit(X_train, y_train)

# 提取特征重要性并排序
feature_importances = model.feature_importances_
indices = np.argsort(feature_importances)  # 降序排序的索引
# 创建颜色映射
colors = sns.color_palette("YlOrRd", len(indices))  # 创建从黄色到红色的颜色渐变
# 绘制特征重要性图
plt.figure(figsize=(10, 8))
sns.barplot(x=feature_importances[indices], y=column_names[indices], palette=colors)
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title('Feature Importance Sorted by Score')
plt.subplots_adjust(left=0.25)
plt.savefig('../data_analyse/pic2/adaboost_feature_importance.png')
