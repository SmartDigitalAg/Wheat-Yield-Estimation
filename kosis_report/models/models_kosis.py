import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def save_to_excel(file_name, data_frame):
    book = Workbook()
    sheet = book.active
    for row in dataframe_to_rows(data_frame, index=False, header=True):
        sheet.append(row)
    book.save(file_name)

def evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    mae = mean_absolute_error(y_predict, y_test)
    r2 = r2_score(y_predict, y_test)
    return mae, r2, y_predict

def main():
    output_dir = "../output/model_result"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv("../output/input_kosis/전국_기상.csv")

    # df['rainfall_sum'] = df.filter(regex='rainfall').sum(axis='columns')
    # df['sunshine_sum'] = df.filter(regex='sunshine').sum(axis='columns')


    y = df['value']

    w_c = list(df.filter(regex='first|second|third|fourth').columns)
    w_c.append('cumsum_tavg')

    print(w_c)
    X = df[w_c]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    models = [
        LinearRegression(),
        RandomForestRegressor(),
        XGBRegressor()
    ]

    results = []

    for model in models:
        mae, r2, y_predict = evaluate_model(model, X_train, X_test, y_train, y_test)
        results.append({"Model": type(model).__name__, "MAE": mae, "R2 Score": r2,})

        plt.scatter(y_test, y_predict)
        plt.scatter(y_train, model.predict(X_train))
        plt.plot([0, max(y_predict)], [0, max(y_predict)])
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.title(f"{type(model).__name__} | mae: {mae:.4f} | r2: {r2:.4f}")
        plt.show()

    # 결과를 DataFrame으로 정리
    results_df = pd.DataFrame(results)

    # 결과를 엑셀 파일로 저장
    save_to_excel(os.path.join(output_dir, "model_results_kosis.xlsx"), results_df)

if __name__ == '__main__':
    main()