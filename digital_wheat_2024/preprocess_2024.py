import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

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
        return "수확기"

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

    # df = df.reset_index()
    # df['index'] = df['index'] + 1
    # df = df.rename(columns={'index': 'ID'})
    # df = df.drop(columns=[rep_col, '조사지'])
    return df
def get_dataframe(result ,value_name, id_vars='rep'):
    result.columns = result.iloc[0]
    result = result[1:].reset_index(drop=True)
    result = result.dropna(how='all')
    result = result.melt(id_vars=id_vars, var_name='조사지', value_name=value_name)

    return result

def cut_data(df, var_index, var_name, next_index, next_num, id_vars='rep', exclude=False):
    if not exclude:
        result = df.iloc[var_index['row']+1:next_index['row']-next_num, var_index['col']-1: var_index['col']+8]
    else:

        result =  df.iloc[var_index['row']+1:, var_index['col']-1: var_index['col']+8]

    result = get_dataframe(result, var_name, id_vars)
    return result

def tiller(df, step):
    # df = datas[step]
    height_index = get_index(df, '초장')
    spad_index = get_index(df, 'SPAD')
    lai_index = get_index(df, 'LAI')
    freshweight_index = get_index(df, '생체중')
    dryweight_index = get_index(df, '건물중(')
    dryweight_per_index = get_index(df, '건물중 비율')

    height_df = cut_data(df, height_index, '초장(cm)', lai_index, 3, )
    lai_df = cut_data(df, lai_index, 'LAI', spad_index, 3, )
    spad_df = cut_data(df, spad_index, 'SPAD', spad_index, 1, exclude=True)

    freshweight_df = cut_data(df, freshweight_index, '생체중(g/20*30cm)', dryweight_index, 1, )
    dryweight_df = cut_data(df, freshweight_index, '건물중(20*30cm)', dryweight_per_index, 1, )


    merged = pd.merge(height_df, spad_df, on=['조사지', 'rep'], how='inner')
    merged = pd.merge(merged, lai_df, on=['조사지', 'rep'], how='inner')
    # merged = pd.merge(merged, freshweight_df, on=['조사지', 'rep'], how='inner')
    # merged = pd.merge(merged, dryweight_df, on=['조사지', 'rep'], how='inner')

    if '분얼전기' in step:
        length_index = get_index(df, '유수')
        # dryweight_per_df = cut_data(df, dryweight_per_index, '건물중 비율', length_index, 1, )
        length_df = cut_data(df, length_index, '유수길이(mm)', length_index, 1, exclude=True)
        merged = pd.merge(merged, length_df, on=['조사지', 'rep'], how='inner')
        # merged = pd.merge(merged, dryweight_per_df, on=['조사지', 'rep'], how='inner')

    # elif '분얼후기' in step:
    #     count_cm_index = get_index(df, '경수 (20*20cm2)')
    #     count_m_index = get_index(df, '경수 (1m2)')
    #     dryweight_per_df = cut_data(df, dryweight_per_index, '건물중 비율', count_cm_index, 1, )
    #     count_cm_df = cut_data(df, count_cm_index, '경수 (20*20cm2)', count_m_index, 1)
    #     count_m_df = cut_data(df, count_m_index, '경수 (20*20cm2)', count_m_index, 1, exclude=True)
    #
    #     merged = pd.merge(merged, dryweight_per_df, on=['조사지', 'rep'], how='inner')
    #     merged = pd.merge(merged, count_cm_df, on=['조사지', 'rep'], how='inner')
    #     merged = pd.merge(merged, count_m_df, on=['조사지', 'rep'], how='inner')


    merged = get_ten(merged, 'rep')
    merged['생육단계'] = step.split("(")[-1].replace(")", "")
    merged = merged.rename(columns={"rep": "반복"})

    return merged




def flower(df, step):
    left_df = df.iloc[:, :11]
    left_df['조사지'] = left_df['조사지'].fillna(method='ffill')
    left_df = left_df.drop(columns=['조사일'])
    left_df = left_df[left_df['조사지'] != '조사지']
    left_df = left_df.dropna(how='all', axis=1)
    left_df = get_ten(left_df, '반복')
    left_df['생육단계'] = step.split("(")[-1].replace(")", "")
    left_df.columns = [col.replace("\n", "")  for col in left_df.columns]
    left_df = left_df.rename(columns={'군집(LAI)': 'LAI', '엽록소함량(µmol/m2)': 'SPAD'})

    return left_df
    # if "개화기" in step:
    #     right_df = df.iloc[:, 11:]
    # else:
    #     seed_index = get_index(df, '200립')
    #     right_df = df.iloc[:seed_index['row'], 11:]
    #     if '개화후' in step:
    #         seed_df = df.iloc[seed_index['row']:, 11:17]
    #
    #     else:
    #         count_index = get_index(df, '일수립수')
    #         seed_df = df.iloc[seed_index['row']:, 11:count_index['col']-1]
    #     seed_df.columns = seed_df.iloc[0]
    #     seed_df = seed_df[2:].reset_index(drop=True)
    #     seed_df = seed_df.dropna(how='all', axis=0)
    #     seed_df = seed_df.dropna(how='all', axis=1)
    #     seed_df.columns = ['조사지', '반복', '200립_생체중', '200립_건물중', '200립_건물중 비율']
    #     seed_df['조사지'] = seed_df['조사지'].fillna(method='ffill')
    #     seed_df['생육단계'] = step.split("(")[-1].replace(")", "")


    # right_df.columns = right_df.iloc[0]
    # right_df = right_df[1:].reset_index(drop=True)
    # right_df = right_df.dropna(how='all', axis=0)
    # right_df = right_df.dropna(how='all', axis=1)
    # right_df.columns = ['조사지', '조사일', '반복', '잎_생체중', '잎_건물중', '잎_건물중 비율',
    #                     '줄기_생체중', '줄기_건물중', '줄기_건물중 비율', '종자_생체중', '종자_건물중', '종자_건물중 비율']
    #
    # right_df['조사지'] = right_df['조사지'].fillna(method='ffill')
    # right_df = right_df.drop(columns=['조사일'])
    # right_df = right_df.dropna(how='all', axis=1)
    # right_df = get_ten(right_df, '반복')
    # right_df['생육단계'] = step.split("(")[-1].replace(")", "")
    #
    # result = pd.merge(left_df, right_df, on=['조사지', '생육단계', '반복'], how='inner')
    # if not '개화기' in step:
    #     result = pd.merge(result, seed_df, on=['조사지', '생육단계', '반복'], how='inner')

    # return result


def harvest_count(df, step):
    count_index = get_index(df, '일수립수')
    real_index = get_index(df, '농가 실측 수량')
    count_df = df.iloc[count_index['row']+1:real_index['row'], count_index['col']-1: count_index['col']+8]
    count_df = get_dataframe(count_df, '일수립수')
    count_df = get_ten(count_df, 'rep')
    growths = flower(df, step)
    count_df = count_df.rename(columns={"rep": "반복"})
    merged = pd.merge(growths, count_df, on=['반복', '조사지'], how='inner')

    return merged

def concat_vegetation_indices(data_dir):
    all_df = pd.DataFrame({'Feature ID': range(81)})
    for file in os.listdir(data_dir):
        if 'vegetation_indices' in file:
            df = pd.read_csv(os.path.join(data_dir, file))
            cols = [col for col in df.columns if 'NDVI' in col or 'CVI' in col or 'NDRE' in col or 'RVI' in col or 'GNDVI' in col or 'Feature ID' in col or 'yield' in col]
            df = df[cols]
            df = df.groupby('Feature ID').mean().reset_index()

            all_df = all_df.merge(df, on='Feature ID', how='left')
    all_df['조사지'] = all_df['Feature ID'].astype(int).apply(lambda x: f'Plot {cal_plot(x)}')
    all_df["반복"] = all_df.groupby("조사지").cumcount() + 1
    all_df = all_df.rename(columns={'Feature ID': 'ID'})
    return all_df
def prerpocess_drone(df):
    # vi_cols = [col for col in df.columns if not 'ID' in col and 'yield' not in col]
    vi_cols = (df.columns).tolist()
    vi_cols.remove('조사지')
    vi_cols.remove('반복')
    df_melted = pd.melt(df, id_vars=['반복', '조사지'], value_vars=vi_cols,
                        var_name='연도_지표', value_name='value')
    df_melted['date'] = df_melted['연도_지표'].str.split('_').str[0]
    df_melted['지표'] = df_melted['연도_지표'].str.split('_').str[1]
    lst = []
    for vi in df_melted['지표'].unique():
        df_each = df_melted[df_melted['지표'] == vi][['조사지', '반복', 'date', 'value']].rename(columns={'value': vi})
        lst.append(df_each)
    # result = pd.merge(lst[0], lst[1], on=['반복', 'date', '조사지'], how='inner')
    result = pd.merge(lst[1], lst[2], on=['반복', 'date', '조사지'], how='inner')
    result = pd.merge(result, lst[3], on=['반복', 'date', '조사지'], how='inner')
    result = pd.merge(result, lst[4], on=['반복', 'date', '조사지'], how='inner')
    result = pd.merge(result, lst[5], on=['반복', 'date', '조사지'], how='inner')

    result['생육단계'] = pd.to_datetime(result['date'].apply(lambda x: f"20{x[:2]}-{x[2:4]}-{x[4:]}")).apply(add_stage)

    result = result.drop(columns=['date'])
    result['CVI'] = result['CVI'] / 100
    return result


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

def get_data(growth_filename, drone_data_dir):
    drone_df = concat_vegetation_indices(drone_data_dir)
    drone_df = prerpocess_drone(drone_df)
    datas = pd.read_excel(growth_filename, sheet_name=None)

    growth_df = pd.DataFrame()
    for step, df in datas.items():
        if step != '24.03.07' and step != 'avg':
            if '분얼' in step:
                result = tiller(df, step)
            elif '수확' in step:
                step = '수확기'
                result = harvest_count(df, step)

            else:
                result = flower(df, step)


            growth_df = pd.concat([growth_df, result], axis=0)

    merged = pd.merge(growth_df, drone_df, on=['조사지', '생육단계', '반복'], how='inner')

    cols = [col for col in merged.columns if not '경수' in col]
    merged = merged[cols]
    value_cors = list(merged.columns)
    value_cors.remove('생육단계')
    value_cors.remove('조사지')
    value_cors.remove('반복')

    df_melted = pd.melt(merged, id_vars=['조사지', '생육단계', '반복'], value_vars=value_cors,
                        var_name='지표', value_name='값')

    df_melted['지표_생육단계'] = df_melted['지표'] + '_' + df_melted['생육단계']
    df_pivot = df_melted.pivot(index=['조사지', '반복'], columns='지표_생육단계', values='값')

    df_result = df_pivot.reset_index()
    df_result = df_result.dropna(axis=1, how='all')
    df_result['관개'] = 0
    df_result['시비'] = 0
    df_result['파종'] = 0
    df_result['관개'] = df_result['조사지'].apply(lambda x: 1 if x == 'Plot 3' or x == 'Plot 4' or x == 'Plot 7' or x == 'Plot 8' else 0)
    df_result['시비'] = df_result['조사지'].apply(lambda x: 1 if x == 'Plot 2' or x == 'Plot 3' or x == 'Plot 6' or x == 'Plot 7' else 0)
    df_result['파종'] = df_result['조사지'].apply(lambda x: 1 if x == 'Plot 5' or x == 'Plot 6' or x == 'Plot 7' or x == 'Plot 8' else 0)

    return df_result
def main():
    input_dir ='./input'
    data_dir = os.path.join(input_dir, '2024')
    growth_filename = os.path.join(data_dir, '2024_생육조사결과(최종본).xlsx')
    output_filename = os.path.join(input_dir, '2024_data.csv')

    df_result = get_data(growth_filename, data_dir)
    df_result.to_csv(output_filename, index=False)


if __name__ == '__main__':
    main()