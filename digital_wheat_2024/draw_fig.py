import os
import platform
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc

from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import matplotlib.cm as cm

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

if platform.system() == "Windows":
    font_path = "C:/Windows/Fonts/NGULIM.TTF"  # 원하는 폰트 경로
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)
elif platform.system() == "Darwin":
    rc('font', family='AppleGothic')


def model_result_scatter_plot(model, X_train, X_test, y_train, y_test, y_predict, score_dct, head_title, result_scatter_path):
    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax.scatter(y_test, y_predict, label='Test Data', color='black', edgecolors='black', marker='o', s=100)
    ax.scatter(y_train, model.predict(X_train), label='Training Data', color='black', marker='o', facecolors='none', s=100)

    ax.set_xlim([0, max(max(y_predict), max(y_test)) * 1.05])
    ax.set_ylim([0, max(max(y_predict), max(y_test)) * 1.05])

    ax.plot([ax.get_xlim()[0], max(ax.get_xlim()[1], max(y_test))],
            [ax.get_xlim()[0], max(ax.get_xlim()[1], max(y_test))],
            color='red', linestyle='-', linewidth=1.5)

    ax.set_xlabel("Actual(g/m²)", fontsize=16)
    ax.set_ylabel("Predicted(g/m²)", fontsize=16)
    ax.legend(loc='upper left')
    ax.set_title(f"{head_title}\n "
                 f"Train Score - MAE: {score_dct['train_mae']:.4f} | RMSE: {score_dct['train_rmse']:.4f} | R2: {score_dct['train_r2']:.4f}\n"
                 f"Test Score - MAE: {score_dct['test_mae']:.4f} | RMSE: {score_dct['test_mae']:.4f} | R2: {score_dct['test_r2']:.4f}", fontsize=16 )  # Model name as head title
    plt.savefig(result_scatter_path)
    plt.close()


def feature_importance_bar_plot(top_10_features, model_op, year, feature_bar_path):
    cmap = cm.get_cmap('coolwarm')

    # 빨간색 (높은 값)과 파란색 (낮은 값)
    blue_rgb = cmap(0)  # 파란색
    red_rgb = cmap(1)  # 빨간색

    vi_vars = ['NDVI', 'CVI', 'GNDVI', 'NDRE', 'RVI']
    top_10_features['color'] = top_10_features['Feature'].apply(lambda x: '#80796BFF' if x.split("_")[0] in vi_vars else '#374E5599')
    top_10_features = top_10_features.sort_values(by='Importance', ascending=True)


    # # 그래프 그리기
    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.barh(top_10_features['Feature'], top_10_features['Importance'], align="center", color=top_10_features['color'], edgecolor='black' )
    # ax.set_yticks(range(10))
    ax.set_yticklabels(top_10_features['Feature'], fontsize=14 )
    ax.set_title(f"{model_op} 상위 10개 변수 중요도 {year}", fontsize=16)
    ax.set_xlabel("Importance")
    ax.legend(
        handles=[
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#80796BFF', markersize=14, label='식생지수'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#374E5599', markersize=14, label='생육지표',)
        ],
        loc='lower right', fontsize=16
    )

    fig.tight_layout()
    plt.savefig(feature_bar_path)
    plt.close()
