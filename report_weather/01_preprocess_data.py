import os
import pandas as pd

input_dir = '../input'
output_dir = '../output'

report_weather_dir = os.path.join(output_dir, 'report_weather')
if not os.path.exists(report_weather_dir):
    os.makedirs(report_weather_dir)

want = 'origin' # re/origin
report_dir = os.path.join(output_dir, 'report', f'{want}_datas')
weather_dir = os.path.join(output_dir, 'cache_weather')

data_dir = os.path.join(report_weather_dir, want)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 상순: 1~10 / 중순: 11~20 /하순: 21~31

def preprocess_weather(station_code_dict):
    all_stations = pd.DataFrame()
    for stnNm, stnID in station_code_dict.items():
        df = pd.read_csv(os.path.join(weather_dir, f'all_{stnID}.csv'))

        # 10월 ~ 12월에 seasonyear(year + 1)
        df['season_year'] = df['year']
        df.loc[df["month"] > 9, "season_year"] = df['year'] + 1

        # winter_temp: 파종 ~ 월동 전 온도 > 10월 ~ 2월 중순 => season_year를 기준으로
        winter = df[df['month'].isin([10, 11, 12, 1, 2]) | ((df['month'] == 2) & (df['day'] <= 20))] # 전년도 10월 ~ 당해년도 2월 중순
        winter_temp = winter.groupby('season_year')['tavg'].mean().reset_index().loc[1:] # 데이터의 시작 연도는 전년도가 없기 때문에 제대로된 값을 얻을 수 없음
        winter_temp.columns = ['year', 'winter_tavg'] # 전체 병합을 위해 column 명 재설정

        # vegetative_temp: 월동 후 영양생장기 온도 > 2월 하순 ~ 3월 중순
        vegetative = df[((df['month'] == 2) & (df['day'] >= 21)) | ((df['month'] == 3) & (df['day'] <= 20))] # 2월 하순 ~ 3월 중순
        vegetative_temp = vegetative.groupby('year')['tavg'].mean().reset_index()
        vegetative_temp.columns = ['year', 'vegetative_tavg']

        # spring_temp: 수잉기 온도 > 4월 상순 ~ 중순
        spring = df[(df['month'] == 4) & (df['day'] <= 20)] # 4월 상순 ~ 중순
        spring_temp = spring.groupby('year')['tavg'].mean().reset_index()
        spring_temp.columns = ['year', 'spring_tavg']

        # flowering_temp_rain: 출수기 및 개화기 온도와 강수량 > 4월 하순 ~ 5월 상순
        flowering= df[((df['month'] == 4) & (df['day'] >= 21)) | ((df['month'] == 5) & (df['day'] <=10))] # 4월 하순 ~ 5월 상순
        flowering_temp = flowering.groupby('year')['tavg'].mean().reset_index()
        flowering_rain = flowering.groupby('year')['rainfall'].sum().reset_index()
        flowering_temp_rain = pd.merge(flowering_temp, flowering_rain, on='year', how='inner')
        flowering_temp_rain.columns = ['year', 'flowering_tavg', 'flowering_rain']

        # summer_temp_hrad: 등숙기 온도와 일조시간 > 5월
        summer = df[df['month'] == 5]
        summer_temp = summer.groupby('year')['tavg'].mean().reset_index()
        summer_hrad = summer.groupby('year')['sunshine'].sum().reset_index()
        summer_temp_hrad = pd.merge(summer_temp, summer_hrad, on='year', how='inner')
        summer_temp_hrad.columns = ['year', 'summer_tavg', 'summer_hrad']

        merged = pd.merge(winter_temp, vegetative_temp, on='year', how='inner')
        merged = pd.merge(merged, spring_temp, on='year', how='inner')
        merged = pd.merge(merged, flowering_temp_rain, on='year', how='inner')
        merged = pd.merge(merged, summer_temp_hrad, on='year', how='inner')

        merged['지역'] = stnNm
        all_stations = pd.concat([all_stations, merged])

    return all_stations


def report_summary_df(result, list_condition):
    print(want, result['품종'].unique())


    for condition, func in list_condition:
        df_condition = result.pivot_table(index='year', columns=condition, values='완전종실중(kg/10a)', aggfunc=func)
        print(df_condition.columns)
        print(result.pivot_table(index='year', columns=condition, values='완전종실중(kg/10a)', aggfunc='sum').columns)
        df_condition.to_csv(os.path.join(data_dir, f"맥류작황보고서_{condition}별_생산량.csv"), encoding='utf-8-sig')


def reshape_statics(df, cols_lst):
    s_cols = ['mean', 'max', 'min', 'std']
    s_df = df[cols_lst].describe().reset_index()
    s_df = s_df[s_df['index'].isin(s_cols)]
    s_df = s_df.T.reset_index()
    s_df.columns = s_df.iloc[0]
    s_df = s_df.iloc[1:]

    return s_df


def generate_statics(df):
    weather_eng_list = ['winter_tavg', 'vegetative_tavg', 'spring_tavg', 'flowering_tavg', 'flowering_rain',
                        'summer_tavg', 'summer_hrad']
    weather_kor_list = ['파종~월동 전 온도', '월동 후 영양생장기 온도', '수잉기 온도', '출수기 및 개화기 온도', '출수기 및 개화기 강수량', '등숙기 온도', '등숙기 일조시간']
    weather_dct = dict(zip(weather_eng_list, weather_kor_list))

    # 기상요인 기초 통계
    weather_s = reshape_statics(df, weather_eng_list)
    weather_s['index'] = weather_s['index'].apply(lambda x: weather_dct[x])

    # 밀 생산요인 기초 통계
    # if want == 'origin':
    #     wheat_list = ["수수(개/m2)", "결실립수(개)", "1,000립중(g)", "완전종실중(kg/10a)"]
    # else:
    wheat_list = ["수수(개/㎡)", "결실립수(개)", "천립중(g)", "완전종실중(kg/10a)"]

    wheat_s = reshape_statics(df, wheat_list)

    s = pd.concat([weather_s, wheat_s])
    s = s.rename(columns={'index':'항목'})

    s.to_csv(os.path.join(data_dir, '기초통계.csv'), index=False, encoding='utf-8-sig')

def main():
    report_info = pd.read_excel(os.path.join(input_dir, '맥류작황보고서_정보.xlsx'))[:14]
    station_code_dict = {row['지역'] : int(row['지점코드']) for idx, row in report_info.iterrows()}
    station_list = list(set(station_code_dict.values()))

    report_df = pd.read_csv(os.path.join(report_dir, '맥류작황보고서.csv'))
    # 이삭수, 이삭당립수, 천립중 > '맥종', '지역', '재배조건', '품종', '1,000립중(g)', '수수(개/m2)', '결실립수(개)', 'year'
    # report_df = report_df[['맥종', '지역', '재배조건', '품종', '1,000립중(g)', '수수(개/m2)', '결실립수(개)', 'year']]

    summary_weather = preprocess_weather(station_code_dict)
    # preprocess_report(station_list)
    # merge_datas()
    result = pd.merge(summary_weather, report_df, on=['year', '지역'], how='inner') # 기상대가 설치되지 않았던 해는 null 값
    if want == 'origin':
        # streamlit에서 처리하기 편하게 원본 데이터와 재정리한 데이터의 항목명을 재정리한 데이터의 항목명으로 통일
        result.columns = ['year', 'winter_tavg', 'vegetative_tavg', 'spring_tavg', 'flowering_tavg', 'flowering_rain',
                          'summer_tavg', 'summer_hrad', '지역', '맥종', '재배조건', '품종', '1수영화수(개)', '결실립수(개)',
                          '간중(kg/10a)', '간중종실중비율(%)', '경수(개/㎡)_12월10일', '경수(개/㎡)_2월20일', '경수(개/㎡)_3월20일',
                          '경수(개/㎡)_4월10일', '경수(개/㎡)_5월1일', '유효경비율(%)', '수수(개/㎡)', '출수기생체중(g/㎡)',
                          '출수기건물중(g/㎡)', '출수기건물중비율(%)', '초장(cm)_12월10일', '초장(cm)_2월20일',
                          '초장(cm)_3월20일', '초장(cm)_4월10일', '초장(cm)_5월1일', '간장(cm)',
                          '완전종실중(kg/10a)', '설립중(kg/10a)', '리터중(g)', '천립중(g)', '수장(cm)']
    result = result.drop_duplicates(subset=list(result.columns), keep='first')

    result.to_csv(os.path.join(data_dir, '맥류작황보고서_기상요인.csv'), index=False)
    print(want, result['품종'].unique())

    generate_statics(result)



    list_condition = [
        ('지역', 'mean'),
        ('품종', 'mean'),
        ('재배조건', 'mean')]

    report_summary_df(result, list_condition)

if __name__ == '__main__':
    main()
    # preprocess_weather('90')
