import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


iksan_dir = "../output/iksan"

predict_output_dir = os.path.join(iksan_dir, 'predict')
if not os.path.exists(predict_output_dir):
    os.mkdir(predict_output_dir)

def predict_yield(df, feature_predict_figname):
    y = df['drone_yield']
    # drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns
    # X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])

    # plot_cols = df.filter(like='조사지').columns
    # X_cols = ['간장(cm)_개화후2주', 'CVI_개화후2주', '엽록소함량(µmol/m2)_개화후4주',  'SPAD_분얼전기', 'NDRE_개화기',
    #           '군집(LAI)_개화후2주', '군집(LAI)_개화기',]
    # X_cols = ['간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'NDVI_개화후4주',  'CVI_개화후4주', '엽록소함량(µmol/m2)_개화후2주', 'SPAD_분얼전기', 'NDRE_개화기']
    # X_cols = ['CVI_개화후2주', '엽록소함량(µmol/m2)_개화후4주', '간장(cm)_개화후2주', 'NDRE_개화기', '군집(LAI)_개화기', '군집(LAI)_개화후2주']
    # X_cols = ['간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'NDVI_개화후4주', 'CVI_개화후4주', '엽록소함량(µmol/m2)_개화후2주', 'SPAD_분얼전기','NDRE_개화기', '관개', '시비', '파종']
    # X_cols = ['LAI_분얼후기', 'GNDVI_개화후2주', '군집(LAI)_개화기', '초장(cm)_분얼후기', 'NDRE_개화기', '엽록소함량(µmol/m2)_개화후4주', 'CVI_개화후2주', 'SPAD_분얼전기', '군집(LAI)_개화후2주', '간장(cm)_개화후2주', '관개', '시비', '파종']
    # X_cols = ['GNDVI_개화후2주', '군집(LAI)_개화기', 'NDRE_개화기', '엽록소함량(µmol/m2)_개화후4주', 'CVI_개화후2주',
    #           '군집(LAI)_개화후2주', '간장(cm)_개화후2주', '관개', '시비', '파종']

    # X_cols = ['간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'SPAD_분얼전기', '엽록소함량(µmol/m2)_개화후4주']

    # X_cols = ['군집(LAI)_개화기', '엽록소함량(µmol/m2)_개화후4주', '유수길이(mm)_분얼전기', '엽록소함량(µmol/m2)_개화후2주', 'LAI_분얼후기', '간장(cm)_개화후2주',
    #  '초장(cm)_분얼전기', 'SPAD_분얼전기', '초장(cm)_분얼후기', '군집(LAI)_개화후2주']
    # X_cols = ['간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'SPAD_분얼전기']
    # X_cols = ['간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'SPAD_분얼전기', 'CVI_개화후2주', '엽록소함량(µmol/m2)_개화후4주', 'NDRE_개화기',
    #           '초장(cm)_분얼후기', '군집(LAI)_개화기', 'LAI_분얼전기', 'GNDVI_개화후2주']

    #-------drone 포함
    X_cols = ['CVI_개화기', 'NDRE_분얼후기', 'NDRE_개화후2주', 'GNDVI_분얼후기', '엽록소함량(µmol/m2)_개화기', 'GNDVI_개화후2주', '군집(LAI)_개화기', 'CVI_개화후2주', '초장(cm)_분얼전기', 'CVI_분얼전기']
    #-------생육조사결과만
    X_cols = ['엽록소함량(µmol/m2)_개화기', '군집(LAI)_개화기', '군집(LAI)_개화후2주', '간장(cm)_개화후4주', '수장(cm)_개화후4주', '초장(cm)_분얼전기', 'SPAD_분얼후기', 'LAI_분얼후기', '엽록소함량(µmol/m2)_개화후2주', '군집(LAI)_개화후4주']
    print(", ".join(X_cols))
    plot_cols = ['관개', '시비', '파종']
    X_cols = plot_cols + X_cols
    X_cols = list(set(X_cols))
    X = df[X_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=142)
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    mae = mean_absolute_error(y_predict, y_test)
    mse = mean_squared_error(y_test, y_predict)
    rmse = np.sqrt(mse)
    r2score = r2_score(y_predict, y_test)

    print('MAE: {:.2f}'.format(mae))
    print('R2score: {:.2f}'.format(r2score))
    print('RMSE: {:.2f}'.format(rmse))

    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.scatter(y_test, y_predict, label='Test Data')
    ax.scatter(y_train, model.predict(X_train), label='Training Data')
    # plt.plot([0, max(max(y_predict), max(y_test))], [0, max(max(y_predict), max(y_test))])
    ax.set_xlim([0, max(max(y_predict), max(y_test)) * 1.05])
    ax.set_ylim([0, max(max(y_predict), max(y_test)) * 1.05])
    ax.plot([ax.get_xlim()[0], max(ax.get_xlim()[1], max(y_test))],
            [ax.get_xlim()[0], max(ax.get_xlim()[1], max(y_test))])
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.legend(loc='upper left')
    ax.set_title(f"{type(model).__name__} | RMSE: {rmse:.4f} | r2: {r2score:.4f}")
    plt.savefig(feature_predict_figname)


def main():
    feature_predict_figname = os.path.join(predict_output_dir, 'RFplant_predict.png')

    data_filename = os.path.join(iksan_dir, 'iksan_10data.csv')
    df = pd.read_csv(data_filename)
    # df = df[df['반복'] != '평균']
    # df['종자_생체중_수확기'] = df['종자_생체중_수확기'] * 25

    # df = pd.get_dummies(df, columns=['조사지'], prefix='조사지')
    df = df.dropna(axis=1)

    predict_yield(df, feature_predict_figname)


if __name__ == '__main__':
    main()
    # drone_filename = '../input/iksan/샘플링위치별_식생지수및수확량.xlsx'
    # df = pd.read_excel(drone_filename, sheet_name='샘플링위치별_식생지수및수확량')
    # df = df.drop(columns=['ID','yield(kg/10a)'])
    # cols = [col.split("_")[1] for col in df.columns]
    # cols = list(set(cols))
    # print(cols)