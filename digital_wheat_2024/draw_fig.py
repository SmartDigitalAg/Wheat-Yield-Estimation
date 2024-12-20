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

    ax.scatter(y_test, y_predict, label='Test Data', color='black', edgecolors='black', marker='o')
    ax.scatter(y_train, model.predict(X_train), label='Training Data', color='black', marker='o', facecolors='none')

    ax.set_xlim([0, max(max(y_predict), max(y_test)) * 1.05])
    ax.set_ylim([0, max(max(y_predict), max(y_test)) * 1.05])

    ax.plot([ax.get_xlim()[0], max(ax.get_xlim()[1], max(y_test))],
            [ax.get_xlim()[0], max(ax.get_xlim()[1], max(y_test))],
            color='red', linestyle='-', linewidth=1.5)

    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.legend(loc='upper left')
    ax.set_title(f"{head_title}\nMAE: {score_dct['MAE']:.4f} | RMSE: {score_dct['RMSE']:.4f} | R2: {score_dct['R2']:.4f}")  # Model name as head title
    plt.savefig(result_scatter_path)
    plt.close()


def featuere_importance_bar_plot(top_10_features, model_name, feature_bar_path):
    top_10_features = top_10_features.sort_values(by='Importance')
    plt.clf()
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.barh(range(10), top_10_features['Importance'], align="center", color="gray")
    # ax.barh(range(10), top_10_features['Importance'], align="center", color="green", alpha=0.4)
    ax.set_yticks(range(10))
    ax.set_yticklabels(top_10_features['Feature'])
    ax.set_title(f"{model_name} Top 10 Feature Importance")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    plt.savefig(feature_bar_path)
    plt.close()
