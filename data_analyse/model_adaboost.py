import warnings

from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=27)

# 训练
model.fit(X_train, y_train)

#输出模型参数
print(model.get_params())