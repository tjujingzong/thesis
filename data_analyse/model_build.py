import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../data_analyse/data_result/all_data-2.csv')

# Preprocess data

# Split the data into features and target
X = df.drop('avg latency', axis=1)
column_names = X.columns
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df['avg latency']

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

    # n = X_test.shape[0]  # 样本数量
    # p = X_test.shape[1]  # 自变量的数量
    # r2_adjusted = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    # print(f'Adjusted R-squared: {r2_adjusted}\n')


# List of models to train
models = [
    LinearRegression(),
    Ridge(),
    Lasso(),
    RandomForestRegressor(),
    GradientBoostingRegressor(),
    SVR()
]

# Train and evaluate each model
for model in models:
    train_and_evaluate_model(model, X_train, y_train, X_test, y_test)

# 找出R²值最高的模型
best_model_name = max(model_performance, key=model_performance.get)
best_model = [model for model in models if model.__class__.__name__ == best_model_name][0]

# 使用最佳模型进行预测
best_model.fit(X_train, y_train)
y_pred_best = best_model.predict(X_test)

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_best, alpha=0.5)
plt.xlabel('true value')
plt.ylabel('predicted value')
plt.title(f'{best_model_name}')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red')  # 绘制参考线

# 保存图片
plt.savefig(f'../data_analyse/pic/{best_model_name}.png')

model = RandomForestRegressor()
model.fit(X, y)

# 显示特征重要性
feature_importances = pd.DataFrame(model.feature_importances_, index=column_names, columns=['Importance']).sort_values(
    'Importance', ascending=False)
print(feature_importances)
