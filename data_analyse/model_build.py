import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# Load data
from sklearn.tree import DecisionTreeRegressor

time = "all_data-3"
df = pd.read_csv('../data_analyse/data_result/all_data-3.csv')

# Preprocess data

# Split the data into features and target
X = df.drop('avg-latency', axis=1)
column_names = X.columns
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
y = df['avg-latency']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=27)
model_performance = {}


# Function to train and evaluate models
def train_and_evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    model_performance[model.__class__.__name__] = r2
    print(f'Model: {model.__class__.__name__}')
    print(f'Mean Squared Error: {mse}')
    print(f'Mean Absolute Error: {mae}')
    print(f'R-squared: {r2}\n')

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.xlabel('True Value')
    plt.ylabel('Predicted Value')
    plt.title(f'{model.__class__.__name__}')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    filename = f'../data_analyse/pic/{time}_{model.__class__.__name__}.png'
    plt.savefig(filename)

    # n = X_test.shape[0]  # 样本数量
    # p = X_test.shape[1]  # 自变量的数量
    # r2_adjusted = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    # print(f'Adjusted R-squared: {r2_adjusted}\n')

    # # 确定误差阈值（百分比）
    # error_threshold = 100  # 设定一个阈值，例如10%
    #
    # # 计算每个点的误差（百分比）并记录大误差的点
    # large_errors = []
    # for i, (real, pred) in enumerate(zip(y_test, y_pred)):
    #     if real != 0:  # 防止除以零
    #         error = ((pred - real) / real) * 100
    #         if error > error_threshold:
    #             large_errors.append((i, real, pred, error))

    # # 输出大误差点的信息
    # if large_errors:
    #     print(f'Large errors in model {model.__class__.__name__}:')
    #     for idx, real, pred, error in large_errors:
    #         print(f'Index: {idx}, Real: {real}, Predicted: {pred}, Error: {error}%')
    # else:
    #     print(f'No large errors in model {model.__class__.__name__}')


# List of models to train
models = [
    LinearRegression(),
    Ridge(),
    SVR(),
    DecisionTreeRegressor(),
    RandomForestRegressor(),
    GradientBoostingRegressor(),
    ExtraTreesRegressor(),
    AdaBoostRegressor(base_estimator=DecisionTreeRegressor())
]

# Train and evaluate each model
for model in models:
    train_and_evaluate_model(model, X_train, y_train, X_test, y_test)

print(model_performance)

model = RandomForestRegressor()
model.fit(X, y)

# 显示特征重要性
feature_importances = pd.DataFrame(model.feature_importances_, index=column_names, columns=['Importance']).sort_values(
    'Importance', ascending=False)
print(feature_importances)
