import warnings
from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

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

# 定义贝叶斯优化的搜索空间

search_spaces = {
    'base_estimator__max_depth': Integer(1, 40),
    'base_estimator__min_samples_split': Integer(2, 20),
    'base_estimator__min_samples_leaf': Integer(1, 10),
    'n_estimators': Integer(10, 500),
    'learning_rate': Real(0.001, 5, prior='log-uniform'),
    'loss': Categorical(['linear', 'square', 'exponential']),
}

# 创建 BayesSearchCV 对象
opt = BayesSearchCV(model, search_spaces, n_iter=32, scoring='neg_mean_squared_error', cv=5)

# 拟合 BayesSearchCV
opt.fit(X, y)

# 打印最优参数和最优分数
print("最佳参数：", opt.best_params_)
print("最佳分数：", opt.best_score_)
