import os
import re
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def get_index(df, keyword):
    locations = df.applymap(lambda x: keyword in str(x))
    rows, cols = locations.to_numpy().nonzero()

    return {'row': rows[0], 'col': cols[0]}


def get_ten(df, rep_col):
    df = df[(df[rep_col] != 'avg') & (df[rep_col] != 'stdev')]
    df[rep_col] = df[rep_col].astype(int)
    df = df[df[rep_col] <= 10]
    df = df.reset_index(drop=True)
    df = df.sort_values(['조사지', rep_col])
    df = df.reset_index()
    df['index'] = df['index'] + 1
    df = df.rename(columns={'index': 'ID'})
    df = df.drop(columns=[rep_col, '조사지'])
    return df
def get_dataframe(result ,value_name):
    result.columns = result.iloc[0]
    result = result[1:].reset_index(drop=True)
    result = result.dropna(how='all')
    result = result.melt(id_vars='rep', var_name='조사지', value_name=value_name)

    return result


def tiller_pro(df, step):
    # df = datas[step]
    height_index = get_index(df, '초장')
    spad_index = get_index(df, 'SPAD')
    lai_index = get_index(df, 'LAI')
    # length_index = get_index(df, '유수')


    height_df = df.iloc[height_index['row']+1:lai_index['row']-3, height_index['col']-1: height_index['col']+8]
    height_df = get_dataframe(height_df, '초장(cm)')

    spad_df = df.iloc[spad_index['row']+1:, spad_index['col']-1: spad_index['col']+8]
    spad_df = get_dataframe(spad_df, 'SPAD')

    lai_df = df.iloc[lai_index['row']+1:spad_index['row']-3, lai_index['col']-1: lai_index['col']+8]
    lai_df = get_dataframe(lai_df, 'LAI')

    # length_df = df.iloc[length_index['row']+1:, length_index['col']-1: length_index['col']+8]
    # length_df = get_dataframe(length_df, '유수')
    # print(length_df)

    merged = pd.merge(height_df, spad_df, on=['조사지', 'rep'], how='inner')
    merged = pd.merge(merged, lai_df, on=['조사지', 'rep'], how='inner')
    if '분얼전기' in step:
        length_index = get_index(df, '유수')
        length_df = df.iloc[length_index['row']+1:, length_index['col']-1: length_index['col']+8]
        length_df = get_dataframe(length_df, '유수길이(mm)')
        merged = pd.merge(merged, length_df, on=['조사지', 'rep'], how='inner')

    merged = get_ten(merged, 'rep')
    merged['생육단계'] = step.split("(")[-1].replace(")", "")
    return merged




def flower(df, step):
    # df = datas[step]
    df = df.iloc[:, :11]
    df['조사지'] = df['조사지'].fillna(method='ffill')
    # df['조사지'] = df['조사지'].str.split(' ').str[1].astype(int)
    df = df.drop(columns=['조사일'])
    df = df[df['조사지'] != '조사지']
    df['조사지'] = df['조사지'].str.split(' ').str[1].astype(int)
    df = df.dropna(how='all', axis=1)
    df = get_ten(df, '반복')
    df['생육단계'] = step.split("(")[-1].replace(")", "")
    # df.columns = [col.split("(")[0] if '수량' not in col and '경수' not in col else col for col in df.columns]
    df.columns = [col.replace("\n", "")  for col in df.columns]
    df = df.rename(columns={'군집(LAI)': 'LAI', '엽록소함량(µmol/m2)': 'SPAD', '경수(20*30cm2)':'경수(20*20cm2)'})
    return df


def harvest_count(df, step):
    count_index = get_index(df, '일수립수')
    real_index = get_index(df, '농가 실측 수량')
    count_df = df.iloc[count_index['row']+1:real_index['row'], count_index['col']-1: count_index['col']+8]
    count_df = get_dataframe(count_df, '일수립수')
    count_df = get_ten(count_df, 'rep')
    growths = flower(df, step)
    merged = pd.merge(growths, count_df, on='ID', how='inner')
    return merged


def add_stage(x):

    if x <= pd.to_datetime("2024-03-21"):
        return "분얼전기"
    elif pd.to_datetime("2024-03-21") < x <= pd.to_datetime("2024-04-11"):
        return "분얼후기"
    elif pd.to_datetime("2024-04-11") < x <= pd.to_datetime("2024-04-26"):
        return "개화기"
    elif pd.to_datetime("2024-04-26") < x <= pd.to_datetime("2024-05-09"):
        return "개화후2주"
    elif pd.to_datetime("2024-05-09") < x <= pd.to_datetime("2024-05-24"):
        return "개화후4주"
    elif pd.to_datetime("2024-05-24") < x:
        return "수확"

def concat_vegetation_indices(data_dir):
    all_df = pd.DataFrame({'Feature ID': range(81)})
    for file in os.listdir(data_dir):
        if 'vegetation_indices' in file:
            df = pd.read_csv(os.path.join(data_dir, file))
            cols = [col for col in df.columns if 'NDVI' in col or 'CVI' in col or 'NDRE' in col or 'RVI' in col or 'GNDVI' in col or 'Feature ID' in col]
            df = df[cols]
            df = df.groupby('Feature ID').mean().reset_index()
            all_df = all_df.merge(df, on='Feature ID', how='left')

    all_df = all_df.rename(columns={'Feature ID': 'ID'})
    return all_df
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
    data_dir = '../input/2024'
    growth_filename = '../input/2024/2024_생육조사결과(최종본).xlsx'
    output_dir= '../output'
    drone_df = concat_vegetation_indices(data_dir)
    drone_df = prerpocess_drone(drone_df)
    datas = pd.read_excel(growth_filename, sheet_name=None)
    # '24.03.21(분얼전기)', '24.04.11(분얼후기)', '24.04.26(개화기)', '24.05.09(개화후2주)', '24.05.24(개화후4주)', '24.06.07(수확)'
    # flower(datas, '24.05.24(개화후4주)')


    growth_df = pd.DataFrame()
    for step, df in datas.items():
        if step != '24.03.07' and step != 'avg':
            if '분얼' in step:
                result = tiller_pro(df, step)
            elif '수확' in step:
                result = harvest_count(df, step)

            else:
                result = flower(df, step)


            growth_df = pd.concat([growth_df, result], axis=0)

    growth_df.to_csv(os.path.join(output_dir, '2024_growth.csv'), index=False, encoding='utf-8-sig')
    drone_df = drone_df[drone_df['ID'] != 0]
    drone_df.to_csv(os.path.join(output_dir, '2024_drone.csv'), index=False, encoding='utf-8-sig')
    # merged = pd.merge(growth_df, drone_df, on=['ID', '생육단계'], how='inner')
    # merged.to_csv("../output/2024_growth.csv", index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()