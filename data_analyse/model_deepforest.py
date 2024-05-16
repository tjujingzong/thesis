import warnings
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from deepforest import CascadeForestRegressor

# 忽略特定的 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# 读取数据
df = pd.read_csv('../data_analyse/data_result/02-all_data.csv')

# 分离特征和目标变量
X = df.drop('avg-latency(ms)', axis=1)
y = df['avg-latency(ms)']

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 定义深度森林模型的参数网格
param_grid = {
    'n_estimators': [1, 2, 3, 4],
    'n_trees': [50, 100, 150],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10, 15],
    'min_samples_leaf': [1, 2, 4, 6]
}

# 创建深度森林模型实例
model = CascadeForestRegressor()

# 设置网格搜索
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')

# 执行网格搜索
grid_search.fit(X_scaled, y)

# 输出最佳参数和最佳模型性能
print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score: {:.2f}".format(-grid_search.best_score_))

# Best parameters: {'max_depth': 20, 'min_samples_leaf': 2, 'min_samples_split': 2, 'n_estimators': 2, 'n_trees': 50}
# Best cross-validation score: 4.61
