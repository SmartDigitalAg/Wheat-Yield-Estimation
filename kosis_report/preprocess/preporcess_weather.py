import pandas as pd
import os
import tqdm

def weather_period(output_dir, stn_Ids, stn_Nm):
    '''
    불러온 기상데이터 재배기간을 고려해 정리
    '''
    daily = pd.read_csv(f"../output/cache_weather/all_{stn_Ids}.csv")
    daily["season_year"] = daily["year"]
    daily.loc[daily["month"] > 9, "season_year"] = daily["year"] + 1
    daily['station'] = stn_Nm

    df_period = daily[~daily["month"].isin([6, 7, 8, 9])].copy()
    df_period.to_csv(os.path.join(output_dir, f"period_{stn_Ids}.csv"), index=False, encoding="utf-8-sig")


def weather_summary(output_dir, stn_Nm, stn_Ids, drop_col):
    '''

    '''
    df = pd.read_csv(os.path.join(output_dir, f"period_{stn_Ids}.csv"))

    df['eff_tavg'] = df['tavg'].apply(lambda x: x - 5 if x >= 5 else 0)

    df['cumsum_tavg'] = df.groupby('season_year')['eff_tavg'].transform(pd.Series.cumsum)

    sot = df[(df['month'] == 5) & (df['day'] == 31)]

    df_sot = sot[['season_year', 'cumsum_tavg']]

    mean = df.groupby(['month', 'season_year'])[['tavg', 'tmin', 'tmax', 'humid', 'wind']].mean().reset_index()
    sum = df.groupby(['season_year', 'month'])[['sunshine', 'rainfall', 'snow']].sum().reset_index()
    summary = pd.merge(mean, sum, on=['season_year', 'month'], how='inner')
    summary.sort_values(by=['season_year', 'month']).reset_index(inplace=True)

    reshape = summary.pivot(index='season_year', columns='month')
    reshape.columns = ['_'.join(map(str, col)) for col in reshape.columns.values]
    reshape = reshape.reset_index()

    df = pd.merge(reshape, df_sot, on='season_year', how='inner')
    cumsum = df[['cumsum_tavg', 'season_year']]
    df = df.drop('cumsum_tavg', axis=1)

    items = ['tavg', 'tmin', 'tmax', 'rainfall']

    for item in items:
        a = df.filter(regex=item)
        cols = [int(col.split('_')[1]) for col in a.columns]
        if item != 'rainfall':

            df[f'first_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 9 <= num <= 10]].mean(
                axis=1)
            df[f'second_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 11 <= num <= 12]].mean(
                axis=1)
            df[f'third_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 1 <= num <= 2]].mean(axis=1)
            df[f'fourth_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 3 <= num <= 5]].mean(
                axis=1)

        else:
            df[f'first_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 9 <= num <= 10]].sum(axis=1)
            df[f'second_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 11 <= num <= 12]].sum(
                axis=1)
            df[f'third_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 1 <= num <= 2]].sum(axis=1)
            df[f'fourth_{item}'] = a.loc[:, [col for col, num in zip(a.columns, cols) if 3 <= num <= 5]].sum(axis=1)
        df.drop(a.columns, axis=1, inplace=True)

    w_col = df.filter(regex="|".join(drop_col)).columns

    df = df.drop(w_col, axis=1)

    merged = pd.merge(df, cumsum, on = 'season_year', how='outer')
    merged['station'] = stn_Nm
    merged.to_csv(os.path.join(output_dir, f"summary_{stn_Ids}.csv"), index=False, encoding="utf-8-sig")

    return merged

def main():
    output_dir = "../output/weather/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    info_df = pd.read_excel("../input/지점코드.xlsx")

    drop_col = ['wind', 'sunshine', 'snow', 'humid', 'tmin', 'tmax']

    for idx, row in info_df.iterrows():
        print(row['지점코드'], row['지점명'])
        stn_Ids = row['지점코드']
        stn_Nm = row['지점명']

        weather_period(output_dir, stn_Ids, stn_Nm)
        weather_summary(output_dir, stn_Nm, stn_Ids, drop_col)


if __name__ == '__main__':
    main()