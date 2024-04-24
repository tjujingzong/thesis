import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from deepforest import CascadeForestRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('../data_analyse/data_result/02-all_data.csv')

# 分离特征和目标变量
X = df.drop('avg-latency(ms)', axis=1)
column_names = X.columns
# scaler = MinMaxScaler()
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df['avg-latency(ms)']

# 数据切分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=27)


# 定义模型训练和评估函数
def train_and_evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test).ravel()
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print(f'R2: {r2:.4f}')
    print(f'MSE: {mse:.4f}')
    print(f'MAE: {mae:.4f}')
    print(f'MAPE: {mape:.4f}\n')


# 绘制学习曲线
def plot_learning_curves(model, X_train, y_train, X_test, y_test):
    print(f"Plotting Learning Curves for {model.__class__.__name__}...")
    print(len(X_train))
    train_errors, test_errors = [], []
    for m in range(1, len(X_train), 100):
        print(m)
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_test_predict = model.predict(X_test)
        train_errors.append(mean_squared_error(y_train[:m], y_train_predict))
        test_errors.append(mean_squared_error(y_test, y_test_predict))

    plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="Train")
    plt.plot(np.sqrt(test_errors), "b-", linewidth=3, label="Test")
    plt.legend(loc="upper right", fontsize=14)
    plt.xlabel("Training set size", fontsize=14)
    plt.ylabel("RMSE", fontsize=14)
    plt.title("Learning Curves for " + model.__class__.__name__)
    plt.show()
    print(f"Learning Curves for {model.__class__.__name__} - Plotting Complete")


# 定义模型列表
models = [
    # RandomForestRegressor(),
    # AdaBoostRegressor(base_estimator=DecisionTreeRegressor()),
    # CascadeForestRegressor(),
    RandomForestRegressor(
        n_estimators=100,  # 从0.22版本开始默认值是100；在早期版本中，默认值是10
        criterion='squared_error',
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        bootstrap=True,
        oob_score=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        ccp_alpha=0.0,
        max_samples=None
    ),
    AdaBoostRegressor(
        base_estimator=DecisionTreeRegressor(),
        n_estimators=50,
        learning_rate=1.0,
        loss='linear',
        random_state=None
    ),
    CascadeForestRegressor(
        n_estimators=2,
        max_depth=None,
        min_samples_leaf=1,
        n_trees=100,  # 每个cascade layer的树的数量
        n_jobs=-1,
        random_state=None
    )
]

# 训练并评估每个模型，同时绘制学习曲线
for model in models:
    train_and_evaluate_model(model, X_train, y_train, X_test, y_test)
    # plot_learning_curves(model, X_train, y_train, X_test, y_test)
