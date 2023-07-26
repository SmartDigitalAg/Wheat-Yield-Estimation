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

    df = pd.read_csv("../output/input_report/맥류작황보고서.csv")

    # '지역', '재배조건', '품종', '생체중(g/㎡)', '건물중(g/㎡,%)', '건물중비율(%)', 'year',
    # '초장(cm)_12월10일', '초장(cm)_2월20일', '초장(cm)_3월20일', '초장(cm)_4월10일',
    # '초장(cm)_5월1일', '간장(cm)', '완전종실중(kg/10a)', '설립중(kg/10a)', 'l중(g)',
    # '1,000립중(g)', '수장(cm)', '경수(cm)_12월10일', '경수(cm)_2월20일', '경수(cm)_3월20일',
    # '경수(cm)_4월10일', '경수(cm)_5월1일', '유효경비율(%)', '수수(개/m2)', '출현기',
    # '출현양부(양/부)', '출현일수(일)', '초장(㎝)', '경수(개/㎡)', '주간엽수(매)', '지상부건물중(g/㎡)',
    # '토양수분(%)', '병해(0-9)', '충해(0-9)', '기타재해(0-9)', '생육재생기', '초장(cm)',
    # '유수장(mm)', '유수분화정도(1-10)', '토양수분(0-15cm)', '토양수분(16-30cm)', '한발해(0-9)',
    # '습해(0-9)', '최고분얼기', '최고분얼수(개/㎡)', '도복(0-9)', '출수시', '출수기', '출수전',
    # '1수영화수(개)', '간장(cm)\t', '최고분얼수', '유효경수(개/㎡)', '출수기생체중(g/㎡)',
    # '출수기건물중(g/㎡)', '출수기건물중비율(%)', '수수(개/㎡)', '1수립수(개)', '성숙기', '결실률(%)',
    # '간중(kg/10a)', '간중종실중비율(%)', '리터중(g)', '천립중(g)', '1수완전립수', '시험년도', '맥종',
    # '파폭', '시비량_기비_N', '시비량_기비_K20', '시비량_기비_P205', '시비량_추비_N', '파종기', '파종량',
    # '휴폭(cm)'

    y = df['완전종실중(kg/10a)']
    col_x = [
        '초장(cm)_12월10일', '초장(cm)_2월20일', '초장(cm)_3월20일', '초장(cm)_4월10일',
        '초장(cm)_5월1일', '간장(cm)', '경수(cm)_12월10일', '경수(cm)_2월20일', '경수(cm)_3월20일',
        '경수(cm)_4월10일', '경수(cm)_5월1일', '토양수분(%)', '병해(0-9)', '충해(0-9)', '기타재해(0-9)',
        # '초장(cm)', '유수장(mm)', '유수분화정도(1-10)',
        '토양수분(0-15cm)', '토양수분(16-30cm)', '한발해(0-9)',
        '습해(0-9)', '도복(0-9)', 'dssat_yield', 'aqua_yield',
        '품종_금강밀', '품종_농림4호', '품종_백강',
        '품종_새금강', '품종_올밀', '품종_우리밀', '품종_육성3호', '품종_조경밀', '품종_조광', '품종_조품밀',# '재배조건_답리작', '재배조건_전작'
    ]
    w_c = list(df.filter(regex='first|second|third|fourth').columns)
    w_c.append('cumsum_tavg')
    col = col_x + w_c
    X = df[col]

    print(col)

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

        print(y_predict)

    # 결과를 DataFrame으로 정리
    results_df = pd.DataFrame(results)
    print("************************************")
    print(results_df)

    # 결과를 엑셀 파일로 저장
    save_to_excel(os.path.join(output_dir, "model_results_report.xlsx"), results_df)

if __name__ == '__main__':
    main()