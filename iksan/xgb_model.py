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

from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


def draw_feature_importance(df, feature_importance_figname, feature_importance_filename):
    y = df['종자_생체중_수확']
    drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns
    X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])
    model = XGBRegressor(random_state=42)
    model.fit(X, y)

    feature_importance = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance')

    # Create a horizontal bar plot
    plt.figure(figsize=(18, 6))
    plt.barh(range(X.shape[1]), feature_importance_df['Importance'], align="center")
    plt.yticks(range(X.shape[1]), feature_importance_df['Feature'])
    plt.title("XGB Feature Importance")
    plt.xlabel("Importance")
    plt.savefig(feature_importance_figname)

    feature_importance_df.to_csv(feature_importance_filename, index=False)

def predict_yield(df, feature_predict_figname):
    y = df['종자_생체중_수확']
    # drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns
    # X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])
    # X_cols = ['간장(cm)_개화후2주', '군집(LAI)_개화후2주', '엽록소함량(µmol/m2)_개화후2주', '경수(20*20cm2)_개화후4주']
    plot_cols = df.filter(like='조사지').columns
    X_cols = ['엽록소함량(µmol/m2)_개화후4주', '간장(cm)_개화후2주', 'SPAD_분얼전기',  '군집(LAI)_개화기', '엽록소함량(µmol/m2)_개화후2주']
    X_cols =  list(plot_cols) + X_cols
    X = df[X_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=42)

    model = XGBRegressor(random_state=42)
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
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_predict, label='Test Data')
    plt.scatter(y_train, model.predict(X_train), label='Training Data')
    plt.plot([0, max(y_predict)], [0, max(y_predict)])
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.legend(loc='upper left')
    plt.title(f"{type(model).__name__} | RMSE: {rmse:.4f} | r2: {r2score:.4f}")
    plt.savefig(feature_predict_figname)

def main():
    featurefig_output_dir = '../output/feature'
    if not os.path.exists(featurefig_output_dir):
        os.mkdir(featurefig_output_dir)
    feature_importance_figname = os.path.join(featurefig_output_dir, 'XGB_feature_importance.png')
    feature_importance_filename = os.path.join(featurefig_output_dir, 'XGB_feature_importance.csv')

    predict_output_dir = '../output/predict'
    if not os.path.exists(predict_output_dir):
        os.mkdir(predict_output_dir)
    feature_predict_figname = os.path.join(predict_output_dir, 'XGB_predict.png')

    data_filename = '../output/iksan_data.csv'
    df = pd.read_csv(data_filename)
    df = df[df['반복'] != '평균']
    df['종자_생체중_수확'] = df['종자_생체중_수확'] * 25
    df = pd.get_dummies(df, columns=['조사지'], prefix='조사지')


    draw_feature_importance(df, feature_importance_figname, feature_importance_filename)
    predict_yield(df, feature_predict_figname)

if __name__ == '__main__':
    main()