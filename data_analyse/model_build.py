import warnings

import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from deepforest import CascadeForestRegressor
warnings.simplefilter(action='ignore', category=FutureWarning)
# Load data
from sklearn.tree import DecisionTreeRegressor

print(sklearn.__version__)
time = "00-all_data"
df = pd.read_csv('../data_analyse/data_result/00-all_data.csv')

# Preprocess data

# Split the data into features and target
X = df.drop('avg-latency(ms)', axis=1)
column_names = X.columns
# scaler = MinMaxScaler()
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = df['avg-latency(ms)']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=27)
model_performance = {}


# Function to train and evaluate models
def train_and_evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test).ravel()
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test))

    model_performance[model_names[model.__class__.__name__]] = {
        'R2': r2,
        'MSE': mse,
        'MAE': mae,
        "MAPE": mape
    }

    print(f'Model: {model.__class__.__name__}')
    print(f'R2: {r2:.5f}')
    print(f'MSE: {mse:.5f}')
    print(f'MAE: {mae:.5f}')
    print(f'MAPE: {mape:.5f}\n')

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.xlabel('True Value(ms)')
    plt.ylabel('Predicted Value(ms)')
    plt.title(f'{model.__class__.__name__}')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red')

    plt.xlim(0, 25)
    plt.ylim(0, 25)

    filename = f'../data_analyse/pic/{time}_{model.__class__.__name__}.png'
    plt.savefig(filename)


# List of models to train
models = [
    LinearRegression(),
    SVR(),
    KNeighborsRegressor(),
    DecisionTreeRegressor(),

    # GradientBoostingRegressor(),
    # ExtraTreesRegressor(),

    # RandomForestRegressor(),
    # AdaBoostRegressor(base_estimator=DecisionTreeRegressor()),
    # CascadeForestRegressor()
]

model_names = {
    'LinearRegression': 'LR',
    'Ridge': 'Ridge',
    'SVR': 'SVR',
    'KNeighborsRegressor': 'KNN',
    'DecisionTreeRegressor': 'DTR',
    'RandomForestRegressor': 'RFR',
    'GradientBoostingRegressor': 'GBR',
    'ExtraTreesRegressor': 'ETR',
    'AdaBoostRegressor': 'AdaBoost',
    'CascadeForestRegressor': "CFR"
}

# Train and evaluate each model
for model in models:
    train_and_evaluate_model(model, X_train, y_train, X_test, y_test)


def plot_importances():
    model = RandomForestRegressor()
    model.fit(X, y)
    # 显示特征重要性
    feature_importances = pd.DataFrame(model.feature_importances_, index=column_names,
                                       columns=['Importance']).sort_values(
        'Importance', ascending=False)
    print(feature_importances)
    # 将特征重要性可视化
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importances.index, feature_importances['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.subplots_adjust(left=0.25)
    plt.savefig(f'../data_analyse/pic/{time}_feature_importance.png')


def plot_model_performance(model_performance):
    labels = list(model_performance.keys())
    mse_values = [model_performance[model]['MSE'] for model in labels]
    mae_values = [model_performance[model]['MAE'] for model in labels]
    r2_values = [model_performance[model]['R2'] for model in labels]
    mape_values = [model_performance[model]['MAPE'] for model in labels]

    x = np.arange(len(labels))  # the label locations
    width = 0.1  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 6))  # 宽度是15英寸，高度是6英寸。
    rects1 = ax.bar(x - 1.5 * width, mse_values, width, label='MSE')
    rects2 = ax.bar(x - 0.5 * width, mae_values, width, label='MAE')
    rects3 = ax.bar(x + 0.5 * width, mape_values, width, label='MAPE')
    rects4 = ax.bar(x + 1.5 * width, r2_values, width, label='R2')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Models')
    ax.set_ylabel('Scores')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig(f'../data_analyse/pic/{time}_model_performance.png')


plot_model_performance(model_performance)
