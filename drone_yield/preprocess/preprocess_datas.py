
import pandas as pd
import os


def cal_plot(x):
    if 1 <= x <= 10:
        return 6
    elif 11 <= x <= 20:
        return 5
    elif 21 <= x <= 30:
        return 4
    elif 31 <= x <= 40:
        return 3

    elif 41 <= x <= 50:
        return 7
    elif 51 <= x <= 60:
        return 8
    elif 61 <= x <= 70:
        return 2
    elif 71 <= x <= 80:
        return 1

def mean_data(df, con, year):
    if con == '드론':
        df['plot'] = df['ID'].apply(cal_plot)
        val = ['NDVI', 'GNDVI', 'RVI', 'CVI', 'NDRE']
    else:
        df['초장(cm)'] = df.apply(lambda row: row['간장(cm)'] + row['수장(cm)'] if pd.isna(row['초장(cm)']) else row['초장(cm)'],
                                axis=1)

        df['plot'] = ((df['ID'] - 1) // 10) + 1
        val = ['초장(cm)', 'LAI', 'SPAD']

    df = df.sort_values(['ID', 'plot']).reset_index(drop=True)
    df = df.groupby(['plot', '생육단계'])[val].mean().reset_index()
    # df['파종'] = df['plot'].apply(lambda x: '광산' if x <= 4 else '세조')
    # df['시비'] = df['plot'].apply(lambda x: '추비' if x in [2, 3, 6, 7] else '기비')
    df['year'] = year
    # print(df)
    return df


input_dir = "../output"
drone_24 = pd.read_csv(os.path.join(input_dir, "2024_drone.csv"))
growth_24 = pd.read_csv(os.path.join(input_dir, "2024_growth.csv"))
drone_23 = pd.read_csv(os.path.join(input_dir, "2023_drone.csv"))
growth_23 = pd.read_csv(os.path.join(input_dir, "2023_growth.csv"))

growth_24 = mean_data(growth_24, '생육', 2024)
drone_24 = mean_data(drone_24, '드론', 2024)

df_24 = pd.merge(growth_24, drone_24, on=['plot', 'year', '생육단계'], how='inner')


growth_23 = mean_data(growth_23, '생육', 2023)
drone_23 = mean_data(drone_23, '드론', 2023)
df_23 = pd.merge(growth_23, drone_23, on=['plot', 'year', '생육단계'], how='inner')
df = pd.concat([df_24, df_23])
df['생육단계'] = df['생육단계'].apply(lambda x: '수확기' if x == '수확' else x)
df.to_csv("../output/data.csv", index=False, encoding='utf-8-sig')





