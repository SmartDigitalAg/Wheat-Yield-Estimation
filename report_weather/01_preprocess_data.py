import os
import pandas as pd

input_dir = '../input'
output_dir = '../output'
report_dir = os.path.join(output_dir, 'report')
weather_dir = os.path.join(output_dir, 'cache_weather')
concated_dir = os.path.join(report_dir, 'concated')
report_weather_dir = os.path.join(output_dir, 'report_weather')
if not os.path.exists(report_weather_dir):
    os.makedirs(report_weather_dir)

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


def preprocess_report(station_list):
    stage = pd.read_csv(os.path.join(concated_dir, 'stage.csv'))
    method = pd.read_csv(os.path.join(concated_dir, 'method.csv'))
    common_col = ['맥종', '지역', '재배조건', '품종', 'year']
    merged = pd.merge(stage, method, on=common_col, how='inner')
    merged = merged[merged['지역'].isin(station_list)]

    return merged



def main():


    report_info = pd.read_excel(os.path.join(input_dir, '맥류작황보고서_정보.xlsx'))[:14]
    station_code_dict = {row['지역'] : int(row['지점코드']) for idx, row in report_info.iterrows()}
    station_list = list(set(station_code_dict.values()))

    report_df = pd.read_csv(os.path.join(report_dir, '맥류작황보고서.csv'))
    # 이삭수, 이삭당립수, 천립중 > '맥종', '지역', '재배조건', '품종', '1,000립중(g)', '수수(개/m2)', '결실립수(개)', 'year'
    report_df = report_df[['맥종', '지역', '재배조건', '품종', '1,000립중(g)', '수수(개/m2)', '결실립수(개)', 'year']]

    summary_weather = preprocess_weather(station_code_dict)
    # preprocess_report(station_list)
    # merge_datas()
    result = pd.merge(summary_weather, report_df, on=['year', '지역'], how='inner') # 기상대가 설치되지 않았던 해는 null 값
    result.to_csv(os.path.join(report_weather_dir, '맥류작황보고서_기상요인분석.csv'), index=False)

if __name__ == '__main__':
    main()
    # preprocess_weather('90')
