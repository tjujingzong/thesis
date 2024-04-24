import warnings

from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

# 忽略特定的 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# 读取数据
df = pd.read_csv('../data_analyse/data_result/02-all_data.csv')

# 分离特征和目标变量
X = df.drop('avg-latency(ms)', axis=1)
y = df['avg-latency(ms)']

# 数据标准化
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 创建 AdaBoostRegressor 模型实例
model = AdaBoostRegressor(base_estimator=DecisionTreeRegressor())

# 定义要搜索的参数网格
param_grid = {
    # 'base_estimator__max_depth': [1, 2, 3, 4, 5],
    'n_estimators': [50, 100, 150],
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0],
    # 'loss': ['linear', 'square', 'exponential']
    'loss': ['linear']
}

# 创建 GridSearchCV 对象，整个数据集用于搜索和交叉验证
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')

# 拟合 GridSearchCV
grid_search.fit(X, y)

# 打印最优参数和最优分数
print("最佳参数：", grid_search.best_params_)
print("最佳分数：", grid_search.best_score_)
