import os
import platform
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc

from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

import draw_fig

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

if platform.system() == "Windows":
    font_path = "C:/Windows/Fonts/NGULIM.TTF"  # 원하는 폰트 경로
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)
elif platform.system() == "Darwin":
    rc('font', family='AppleGothic')


def get_model_x_y(df, y_value, model_name):
    model = None
    if 'rf' in model_name:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        model = XGBRegressor(n_estimators=100, random_state=42, max_depth=3, early_stopping_rounds=100,)


    X = df.drop(columns=y_value)
    y = df[y_value]


    return model, X, y

def get_top_features(df, y_value, model_name, model_op, year, result_path):
    model, X, y = get_model_x_y(df, y_value, model_name)

    if 'rf' in model_name:
        model.fit(X, y)
    else:
        model = XGBRegressor(n_estimators=100, random_state=42, max_depth=3, )
        model.fit(X, y)

    model.fit(X, y)

    feature_importance = model.feature_importances_
    feature_names = df.drop(columns=y_value).columns  # Use original dataframe columns for feature names
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    top_10_features_df = feature_importance_df.head(10)

    # top_10_features_df = feature_importance_df.nlargest(10, 'Importance')
    top_10_features_df.to_csv(f'{result_path}.csv', index=False, encoding='utf-8-sig')
    draw_fig.feature_importance_bar_plot(top_10_features_df, model_op, year,f'{result_path}.png')

    top_10_features_list = top_10_features_df['Feature'].to_list()

    return top_10_features_list

def get_model_score(y_train, y_train_predict, y_test, y_test_predict):
    # Train set scores
    train_mae = mean_absolute_error(y_train, y_train_predict)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_predict))
    train_r2 = r2_score(y_train, y_train_predict)

    # Test set scores
    test_mae = mean_absolute_error(y_test, y_test_predict)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_predict))
    test_r2 = r2_score(y_test, y_test_predict)



    score_dct = {'train_mae': train_mae, 'train_rmse': train_rmse, 'train_r2': train_r2,
                 'test_mae': test_mae, 'test_rmse': test_rmse, 'test_r2': test_r2}

    return score_dct

def run_model(df, y_value, model_name, head_title, result_scatter_path):

    model, X, y = get_model_x_y(df, y_value, model_name)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=42)
    # model.fit(X_train, y_train)
    if 'rf' in model_name:

        model.fit(X_train, y_train)
    else:
        model.fit(
            X_train,
            y_train,
            eval_set=[(X_test, y_test)],
            # eval_metric="rmse",  # 평가 지표
            verbose=False  # 학습 과정을 출력
        )

    y_train_predict = model.predict(X_train)
    y_test_predict = model.predict(X_test)


    score_dct = get_model_score(y_train, y_train_predict, y_test, y_test_predict)

    draw_fig.model_result_scatter_plot(model, X_train, X_test, y_train, y_test, y_test_predict, score_dct, head_title, result_scatter_path)
    return score_dct

def select_columns(data_path, y_value, select_option, model_name, model_op, year, result_path=None, apsim_option=False):

    df = pd.read_csv(data_path)
    df = df.drop(columns='조사지')
    if year != '전체':
        df = df[df['year'] == year]
    df = df.drop(columns=['year'])
    if select_option == 'growth':
        exclude_drone_vars = ['NDVI', 'NDRE', 'RVI', 'GNDVI', 'CVI']
        select_cols = [col for col in df.columns if not col.split("_")[0] in exclude_drone_vars]
    elif select_option == 'drone':
        exclude_growth_vars = ['1수영화수', '초장(cm)', '유수길이(mm)', 'SPAD', 'LAI', '간장(cm)', '수장(cm)']
        select_cols = [col for col in df.columns if not col.split("_")[0] in exclude_growth_vars]
    else:
        if apsim_option:
            no_expert_df = df.drop(columns=['파종', '시비', '관개',])
            top_10_features = get_top_features(no_expert_df, y_value, model_name, model_op, year, result_path)
            select_cols = list(set(['파종', '시비', '관개', 'yield_apsim', y_value] + top_10_features))
        else:
            no_expert_df = df.drop(columns=['파종', '시비', '관개',])
            top_10_features = get_top_features(no_expert_df, y_value, model_name, model_op, year, result_path)
            select_cols = list(set(['파종', '시비', '관개', y_value] + top_10_features))

    df = df[select_cols]
    return df


def loop_model(years, model_names, select_options, data_path, y_value, result_dir, result_save_path, apsim_option=False):
    result_list = []
    for year in years:
        for model_name, model_op in model_names.items():
            for select_option, select_op in select_options.items():
                head_title = f'{model_op} {select_op} {year}'

                model_result_dir = os.path.join(result_dir, model_name)
                os.makedirs(model_result_dir, exist_ok=True)
                result_scatter_path = os.path.join(model_result_dir, f"모델결과_{select_op}_{year}.png")
                result_feature_path = os.path.join(model_result_dir, f"상위10개변수_{year}")

                df = select_columns(data_path, y_value, select_option,model_name, model_op, year,
                                    result_path=result_feature_path, apsim_option=apsim_option)

                score_dct = run_model(df, y_value, model_name, head_title, result_scatter_path)
                score_dct['model_name'], score_dct['select_option'], score_dct['year'] = model_op, select_op, year
                print(score_dct)
                result_list.append(score_dct)
    result_df = pd.DataFrame(result_list)
    result_df = result_df.sort_values(by='test_r2', ascending=False)
    result_df.to_csv(result_save_path, index=False, encoding='utf-8-sig')

def main():
    result_dir = './output'
    data_path = os.path.join(result_dir, 'data_apsim.csv')
    result_save_path = os.path.join(result_dir, 'apsim_result.csv')
    version = 'v04'

    y_value = '수량(g/m2)_수확기'
    years = [2023, 2024, '전체']
    model_names = {f'{version}_result_rf': 'RandomForest', f'{version}_result_xgb': "XGBoost"}
    select_options = {'growth': "생육조사", 'drone': "드론식생지수", 'top10':'상위10개변수'}

    loop_model(years, model_names, select_options, data_path, y_value, result_dir, result_save_path, apsim_option=True)





if __name__ == '__main__':
    main()