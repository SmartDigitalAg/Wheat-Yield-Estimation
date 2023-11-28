import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    mae = mean_absolute_error(y_predict, y_test)
    r2 = r2_score(y_predict, y_test)
    return mae, r2, y_predict

def main():
    predict_output_dir = '../output/predict'
    if not os.path.exists(predict_output_dir):
        os.mkdir(predict_output_dir)

    data_filename = '../output/iksan_data_all.csv'
    df = pd.read_csv(data_filename)
    df = df.dropna(axis=1)
    df = df[df['반복'] != '평균']
    y = df['종자_생체중_수확'] * 25
    drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns
    X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=42)

    models = [
        LinearRegression(),
        RandomForestRegressor(),
        XGBRegressor()
    ]

    results = []

    for model in models:
        mae, r2, y_predict = evaluate_model(model, X_train, X_test, y_train, y_test)
        results.append({"Model": type(model).__name__, "MAE": mae, "R2 Score": r2,})

        plt.clf()
        plt.scatter(y_test, y_predict, label='Test Data')
        plt.scatter(y_train, model.predict(X_train), label='Training Data')
        plt.plot([0, max(y_predict)], [0, max(y_predict)])
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.legend(loc='upper left')
        plt.title(f"{type(model).__name__} | mae: {mae:.4f} | r2: {r2:.4f}")
        plt.savefig(os.path.join(predict_output_dir, f"{type(model).__name__}.png") )
        
    print(results)


if __name__ == '__main__':
    main()