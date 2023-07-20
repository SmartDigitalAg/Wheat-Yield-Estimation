import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def main():
    output_dir = "../output/model_result"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv("../output/input_kosis/전국_생산량_기상.csv")

    df['rainfall_sum'] = df.filter(regex='rainfall').sum(axis='columns')
    df['sunshine_sum'] = df.filter(regex='sunshine').sum(axis='columns')

    y = df['value']
    X = df[['cumsum_tavg', 'rainfall_sum', 'sunshine_sum']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=42)

    # linear regression
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)

    y_predict_lr = model_lr.predict(X_test)

    mae_lr = mean_absolute_error(y_predict_lr, y_test)
    r2_lr = r2_score(y_predict_lr, y_test)

    plt.subplot(2, 2, 1)
    plt.scatter(y_test, y_predict_lr)
    plt.scatter(y_train, model_lr.predict(X_train))
    plt.plot([0, max(y_predict_lr)], [0, max(y_predict_lr)])
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"Linear Regression | mae: {mae_lr:.4f} | r2: {r2_lr:.4f}")

    # randomforest
    model_rf = RandomForestRegressor()
    model_rf.fit(X_train, y_train)

    y_predict_rf = model_rf.predict(X_test)

    mae_rf = mean_absolute_error(y_predict_rf, y_test)
    r2_rf = r2_score(y_predict_rf, y_test)

    plt.subplot(2, 2, 2)
    plt.scatter(y_test, y_predict_rf)
    plt.scatter(y_train, model_rf.predict(X_train))
    plt.plot([0, max(y_predict_rf)], [0, max(y_predict_rf)])
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"RandomForest Regression | mae: {mae_rf:.4f} | r2: {r2_rf:.4f}")

    # XGBoost
    model_xgb = XGBRegressor()
    model_xgb.fit(X_train, y_train)

    y_predict_xgb = model_xgb.predict(X_test)

    mae_xgb = mean_absolute_error(y_predict_xgb, y_test)
    r2_xgb = r2_score(y_predict_xgb, y_test)

    plt.subplot(2, 2, 3)
    plt.scatter(y_test, y_predict_xgb)
    plt.scatter(y_train, model_xgb.predict(X_train))
    plt.plot([0, max(y_predict_xgb)], [0, max(y_predict_xgb)])
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"XGBoost Regression | mae: {mae_xgb:.4f} | r2: {r2_xgb:.4f}")


    plt.show()

if __name__ == '__main__':
    main()