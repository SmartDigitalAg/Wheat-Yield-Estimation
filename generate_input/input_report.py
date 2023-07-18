import os
import pandas as pd

def merge_summary(info_df):
    list_dfs = []

    for idx, row in info_df.iterrows():
        stn_Ids = str(row['지점코드']).split('.')[0]
        weather_summary = pd.read_csv(f"../output/weather/summary_{stn_Ids}.csv")
        list_dfs.append(weather_summary)
    df_merge = pd.concat(list_dfs)

    return df_merge

def main():
    output_dir = "../output/input_report/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    info_df = pd.read_excel("../input/맥류작황보고서_정보.xlsx").head(14)

    report = pd.read_csv("../output/report/맥류작황보고서.csv")
    cropmodel = pd.read_csv("../output/cropmodel/작물모델결과.csv")
    weather_summary = merge_summary(info_df)

    merged = pd.merge(report, weather_summary, how="inner", left_on=['station', 'year'], right_on=['station', 'season_year'])
    merged['year'] = merged['year'].astype(int)
    merged.drop('season_year', axis=1, inplace=True)
    # merged.to_csv(os.path.join(output_dir, "맥류작황보고서_기상.csv"), index=False)

    merged = pd.get_dummies(merged, columns=['품종'])
    merged = pd.get_dummies(merged, columns=['재배조건'])

    merged = pd.merge(cropmodel, merged, left_on=['실제지역', 'year'], right_on=['지역', 'year'], how='inner')
    merged.to_csv(os.path.join(output_dir, "맥류작황보고서.csv"), index=False)
        
        
        


if __name__ == '__main__':
    main()