import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from deepforest import CascadeForestRegressor
from sklearn.tree import DecisionTreeRegressor

# 打印scikit-learn的版本
print(sklearn.__version__)
time = "00-all_data"
df = pd.read_csv('../data_analyse/data_result/00-all_data.csv')

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

    print(f'R2: {r2:.5f}')
    print(f'MSE: {mse:.5f}')
    print(f'MAE: {mae:.5f}')
    print(f'MAPE: {mape:.5f}\n')


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
    RandomForestRegressor(),
    AdaBoostRegressor(base_estimator=DecisionTreeRegressor()),
    CascadeForestRegressor()
]

# 训练并评估每个模型，同时绘制学习曲线
for model in models:
    train_and_evaluate_model(model, X_train, y_train, X_test, y_test)
    # plot_learning_curves(model, X_train, y_train, X_test, y_test)
