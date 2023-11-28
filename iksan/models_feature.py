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


def draw_feature_importance(df, featurefig_output_dir, model_name):
    feature_importance_figname = os.path.join(featurefig_output_dir, f'fig_{model_name}importance.png')
    feature_importance_filename = os.path.join(featurefig_output_dir, f'raw_{model_name}importance.csv')

    model = None
    if 'XGB' in model_name:
        model = XGBRegressor(random_state=42)
    elif 'RF' in model_name:
        df = df.dropna(axis=1)
        model = RandomForestRegressor(n_estimators=100, random_state=42)

    y = df['종자_생체중_수확기']
    drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns | df.filter(like='경수').columns#| df.filter(like='분얼').columns #| df.filter(like='경수').columns
    X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])


    model.fit(X, y)

    feature_importance = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance')

    save_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    save_df.to_csv(feature_importance_filename, index=False)

    top_10_features = feature_importance_df.nlargest(10, 'Importance')
    top_10_features = top_10_features.sort_values(by='Importance')

    plt.figure(figsize=(18, 6))
    plt.barh(range(10), top_10_features['Importance'], align="center")
    plt.yticks(range(10), top_10_features['Feature'])
    plt.title(f"{model_name} Top 10 Feature Importance")
    plt.xlabel("Importance")
    plt.savefig(feature_importance_figname)
    print(model_name)
    print(top_10_features['Feature'].to_list())

def main():
    featurefig_output_dir = '../output/feature'
    if not os.path.exists(featurefig_output_dir):
        os.mkdir(featurefig_output_dir)
    filename = f'../output/iksan_data_all_test.csv'

    df = pd.read_csv(filename)
    # df = df[df['반복'] != '평균']
    df = df.drop(columns='반복')
    df['종자_생체중_수확기'] = df['종자_생체중_수확기'] * 25

    draw_feature_importance(df, featurefig_output_dir, f'XGB')
    draw_feature_importance(df, featurefig_output_dir, f'RF')

    # data_filename = '../output/iksan_data_drone.csv'
    # data_filename = '../output/iksan_data_all.csv'
    # # data_filename = '../output/iksan_data_plant.csv'

    # file_dict = ['drone', 'plant', 'all_test']
    # for key in file_dict:
    #     filename = f'../output/iksan_data_{key}.csv'
    #
    #     df = pd.read_csv(filename)
    #     # df = df[df['반복'] != '평균']
    #     df = df.drop(columns='반복')
    #     df['종자_생체중_수확기'] = df['종자_생체중_수확기'] * 25
    #
    #     draw_feature_importance(df, featurefig_output_dir, f'XGB{key}')
    #     draw_feature_importance(df, featurefig_output_dir, f'RF{key}')


if __name__ == '__main__':
    main()