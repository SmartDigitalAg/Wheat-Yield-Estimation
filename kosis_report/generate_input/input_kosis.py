import os
import pandas as pd

def merge_data(stn_Ids):
    period_df = pd.read_csv(f"../output/weather/period_{stn_Ids}.csv")

    period_df['eff_tavg'] = period_df['tavg'].apply(lambda x: x - 5 if x >= 5 else 0)
    period_df['cumsum_tavg'] = period_df.groupby('season_year')['eff_tavg'].transform(pd.Series.cumsum)

    sot = period_df[(period_df['month'] == 5) & (period_df['day'] == 31)]
    df_sot = sot[['season_year', 'cumsum_tavg']]

    mean = period_df.groupby(['month', 'season_year'])[['tavg', 'tmin', 'tmax', 'humid', 'wind']].mean().reset_index()
    sum = period_df.groupby(['season_year', 'month'])[['sunshine', 'rainfall', 'snow']].sum().reset_index()
    summary = pd.merge(mean, sum, on=['season_year', 'month'], how='inner')
    summary.sort_values(by=['season_year', 'month']).reset_index(inplace=True)

    reshape = summary.pivot(index='season_year', columns='month')
    reshape.columns = ['_'.join(map(str, col)) for col in reshape.columns.values]
    reshape = reshape.reset_index()

    df = pd.merge(reshape, df_sot, on='season_year', how='inner')

    return df

def main():
    output_dir = "../output/input_kosis/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filenames = [x.strip(".csv") for x in os.listdir("../output/kosis/") if x.endswith(".csv")]

    code = pd.read_excel("../input/지점코드.xlsx")

    station = pd.DataFrame(filenames, columns=['지점명'])
    station['파일명'] = station['지점명']
    station['지점명'] = station['지점명'].str.split('_').str[1].str[0:2]


    info_df = pd.merge(code, station, on='지점명', how='inner')

    files = []
    list_dfs = []
    for idx, row in info_df.iterrows():
        stn_Nm = row['지점명']
        filename = row['파일명']
        stn_Ids = row['지점코드']

        period = merge_data(stn_Ids)
        summary = pd.read_csv(f"../output/weather/summary_{stn_Ids}.csv")
        wheat = pd.read_csv(f'../output/kosis/{filename}.csv')

        period['year'] = period['season_year']
        period = period.drop(columns = ['cumsum_tavg', 'season_year'])
        summary['year'] = summary['season_year']
        wheat = wheat[wheat['item'] == '단위생산량']


        weather = pd.merge(period, summary, on='year', how='inner')
        weather_wheat = pd.merge(wheat, weather, on='year', how='inner')


        weather_wheat.to_csv(os.path.join(output_dir, f"{stn_Nm}_기상.csv"), index=False, encoding="utf-8-sig")

        list_dfs.append(weather_wheat)
        files.append(filename)

    df_merge = pd.concat(list_dfs)
    df_merge.to_csv(os.path.join(output_dir, "전국_기상.csv"), encoding="utf-8-sig", index=False)
    print(set(filenames) - set(files))  # 기상데이터 없는 지역


if __name__ == '__main__':
    main()