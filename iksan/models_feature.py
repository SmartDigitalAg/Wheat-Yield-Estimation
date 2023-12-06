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

    y = df['drone_yield']
    drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns | df.filter(like='경수').columns#| df.filter(like='분얼').columns #| df.filter(like='경수').columns
    df = df.drop(columns='drone_yield')
    X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])


    model.fit(X, y)

    feature_importance = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance')

    save_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    save_df.to_csv(feature_importance_filename, index=False)

    top_10_features = feature_importance_df.nlargest(10, 'Importance')

    #------barh(가로)
    top_10_features = top_10_features.sort_values(by='Importance')
    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.barh(range(10), top_10_features['Importance'], align="center")
    # ax.barh(range(10), top_10_features['Importance'], align="center", color="green", alpha=0.4)
    ax.set_yticks(range(10))
    ax.set_yticklabels(top_10_features['Feature'])
    ax.set_title(f"{model_name} Top 10 Feature Importance")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    plt.savefig(feature_importance_figname)

    #------bar(세로)
    # top_10_features = top_10_features.sort_values(by='Importance', ascending=False)
    # plt.clf()
    # fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    # ax.bar(top_10_features['Feature'], top_10_features['Importance'], align="center")
    # plt.xticks(rotation=30, ha='right')
    # ax.set_title(f"{model_name} Top 10 Feature Importance")
    # ax.set_xlabel("Feature")
    # ax.set_ylabel("Importance")
    # fig.tight_layout()
    # plt.savefig(feature_importance_figname)

    print(model_name)
    print(list(reversed(top_10_features['Feature'].to_list())))

def main():
    featurefig_output_dir = 'output/feature'
    if not os.path.exists(featurefig_output_dir):
        os.mkdir(featurefig_output_dir)
    filename = f'output/iksan_10data.csv'

    df = pd.read_csv(filename)
    # df = df[df['반복'] != '평균']
    df = df.drop(columns='반복')
    # df['종자_생체중_수확기'] = df['종자_생체중_수확기'] * 25
    drop_columns = df.filter(like='NDRE').columns | df.filter(like='GNDVI').columns |df.filter(like='CVI').columns|df.filter(like='RVI').columns|df.filter(like='NDVI').columns
    df = df.drop(columns=drop_columns)
    draw_feature_importance(df, featurefig_output_dir, f'XGBplant')
    draw_feature_importance(df, featurefig_output_dir, f'RFplant')

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