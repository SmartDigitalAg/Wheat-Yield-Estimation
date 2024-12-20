import os
import pandas as pd

def add_stage(x):
    if x <= pd.to_datetime("2023-01-30"):
        return "분얼전"
    elif pd.to_datetime("2023-01-30") < x <= pd.to_datetime("2023-03-21"):
        return "분얼전기"
    elif pd.to_datetime("2023-03-21") < x <= pd.to_datetime("2023-04-17"):
        return "분얼후기"
    elif pd.to_datetime("2023-04-17") < x <= pd.to_datetime("2023-05-01"):
        return "개화기"
    elif pd.to_datetime("2023-05-01") < x <= pd.to_datetime("2023-05-21"):
        return "개화후2주"
    elif pd.to_datetime("2023-05-21") < x <= pd.to_datetime("2023-06-01"):
        return "개화후4주"
    elif pd.to_datetime("2023-06-01") < x:
        return "수확기"

def preprocess_weather(df):
    df['생육단계'] = pd.to_datetime(df['일시']).apply(add_stage)

    statics = df.groupby('생육단계').agg(
        {
            '평균기온(°C)': ['mean', 'std'],
            '일강수량(mm)': ['sum', 'std'],
            '평균 풍속(m/s)': ['mean', 'std'],
            '평균 상대습도(%)': ['mean', 'std'],
        }

    ).reset_index()
    statics.columns = ['_'.join(col) for col in statics.columns]
    statics = statics.rename(columns={'생육단계_': '생육단계'})
    # df_replicated = pd.concat([statics] * 80, ignore_index=True)
    return statics
    # print(statics)
    # df_melted = statics.melt(id_vars='생육단계_', var_name='측정값', value_name='값')
    # 
    # # '생육단계_'와 '측정값'을 조합해 열 이름을 생성
    # df_melted['열 이름'] = df_melted['측정값'] + '_' + df_melted['생육단계_']
    # 
    # # 열 이름을 index로 pivot하여 열을 펼침
    # df_pivoted = df_melted.pivot_table(columns='열 이름', values='값')
    # 
    # # index 초기화
    # df_pivoted = df_pivoted.reset_index(drop=True)
    # df_replicated = pd.concat([df_pivoted] * 80, ignore_index=True)
    # return df_replicated

def prerpocess_drone(df):
    vi_cols = [col for col in df.columns if not 'ID' in col and 'yield' not in col]
    df_melted = pd.melt(df, id_vars=['ID'], value_vars=vi_cols,
                        var_name='연도_지표', value_name='value')
    df_melted['date'] = df_melted['연도_지표'].str.split('_').str[0]
    df_melted['지표'] = df_melted['연도_지표'].str.split('_').str[1]
    lst = []
    for vi in df_melted['지표'].unique():
        df_each = df_melted[df_melted['지표'] == vi][['ID', 'date', 'value']].rename(columns={'value': vi})
        lst.append(df_each)

    result = pd.merge(lst[0], lst[1], on=['ID', 'date'])
    result = pd.merge(result, lst[2], on=['ID', 'date'])
    result = pd.merge(result, lst[3], on=['ID', 'date'])
    result = pd.merge(result, lst[4], on=['ID', 'date'])
    result['생육단계'] = pd.to_datetime(result['date'].apply(lambda x: f"20{x[:2]}-{x[2:4]}-{x[4:]}")).apply(add_stage)
    return result

def main():
    path = "../iksan/output/iksan_10data.csv"

    weather = pd.read_csv("../input/iksan/기상(2022-2023).csv", encoding='cp949')
    weather['생육단계'] = pd.to_datetime(weather['일시']).apply(add_stage)
    weather_preprocessed = preprocess_weather(weather)


    drone = pd.read_excel("../input/iksan/샘플링위치별_식생지수및수확량.xlsx")
    drone_preprocessed = prerpocess_drone(drone)
    print(drone_preprocessed.shape)
    print(drone_preprocessed['생육단계'].unique())
    growth = pd.read_csv("./output/iksan_data_all_new.csv")
    print(growth['생육단계'].unique())
    print(growth['ID'].unique())

    # result = pd.merge(drone_preprocessed, weather_preprocessed, on='생육단계')
    # print(result.shape)
    result = pd.merge(drone_preprocessed, growth, on=['생육단계', 'ID'])
    print(result.shape)
    result.to_csv("./output/2023_growth.csv", index=False, encoding='utf-8-sig')





    # result = pd.concat([df_statweather_staticsics, iksan], axis=1)
    # result.to_csv("iksan_10data.csv", index=False)


if __name__ == '__main__':
    main()