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
    feature_importance_figname = os.path.join(featurefig_output_dir, f'{model_name}_feature_importance.png')
    feature_importance_filename = os.path.join(featurefig_output_dir, f'{model_name}_feature_importance.csv')

    model = None
    if model_name == 'XGB':
        model = XGBRegressor(random_state=42)
    elif model_name == 'RF':
        df = df.dropna(axis=1)
        model = RandomForestRegressor(n_estimators=100, random_state=42)

    y = df['종자_생체중_수확기']
    drop_columns = df.filter(like='생체중').columns | df.filter(like='건물중').columns | df.filter(like='수확').columns
    X = df.drop(columns=drop_columns).select_dtypes(exclude=['object'])


    model.fit(X, y)

    feature_importance = model.feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance')

    feature_importance_df.to_csv(feature_importance_filename, index=False)
    top_10_features = feature_importance_df.nlargest(10, 'Importance')
    top_10_features = top_10_features.sort_values(by='Importance')

    plt.figure(figsize=(18, 6))
    plt.barh(range(10), top_10_features['Importance'], align="center")
    plt.yticks(range(10), top_10_features['Feature'])
    plt.title(f"{model_name} Top 10 Feature Importance")
    plt.xlabel("Importance")
    plt.savefig(feature_importance_figname)

def main():
    featurefig_output_dir = '../output/feature'
    if not os.path.exists(featurefig_output_dir):
        os.mkdir(featurefig_output_dir)


    data_filename = '../output/iksan_data.csv'
    df = pd.read_csv(data_filename)
    df = df[df['반복'] != '평균']
    df['종자_생체중_수확기'] = df['종자_생체중_수확기'] * 25

    draw_feature_importance(df, featurefig_output_dir, 'XGB')
    draw_feature_importance(df, featurefig_output_dir, 'RF')


if __name__ == '__main__':
    main()