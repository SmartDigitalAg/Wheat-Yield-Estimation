import os
import re
import pandas as pd
import warnings

# 모든 경고 무시
warnings.filterwarnings('ignore')

# iksan_dir = os.path.join(output_dir, 'iksan')
# if not os.path.exists(iksan_dir):
#     os.makedirs(iksan_dir)


def melted(df, value_name):
    df_melted = df.melt(id_vars='rep', var_name='조사지', value_name=value_name)
    return df_melted



def preprocess_tilering(df_height, df_length, df_spad, df_lai, check_date):
    df_height = melted(df_height, '초장(cm)')
    df_length = melted(df_length, '유수길이(mm)')
    df_spad = melted(df_spad, 'SPAD')
    df_lai = melted(df_lai, 'LAI')

    df_merged = pd.merge(df_height, df_length, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_spad, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_lai, on=['rep', '조사지'], how='inner')

    df_merged = df_merged.rename(columns={'rep': '반복'})
    df_merged['조사일'] = check_date

    return df_merged

def preprocess_flowering_cols(df,  check_date, col_seperator = None):
    if col_seperator == "Unnamed":
        df.columns = [col[0].split(' (')[0] + ('_' + col[1] if 'Unnamed' not in col[1] else '') for col in df.columns]
        # df.columns = [col[0] + ('_' + col[1] if 'Unnamed' not in col[1] else '') for col in df.columns]

    elif col_seperator == ".":
        df.columns = [col.split('.')[0] for col in df.columns]
    elif col_seperator == '\n':
        df.columns = [col.replace('\n', '') for col in df.columns]

    df[['조사지', '조사일']] = df[['조사지', '조사일']].fillna(method='ffill')
    df['조사일'] = check_date

    return df


def preprocess_flowering(df_growth, check_date):
    df_growth = preprocess_flowering_cols(df_growth, check_date, '\n')

    return df_growth

def preprocess_merge(df_merged, step_name):
    df_merged = df_merged.drop(columns='조사일')
    df_merged.columns = [col + f'_{step_name}' if '반복' not in col and '조사지' not in col else col for col in df_merged.columns]
    return df_merged

def preprocess_tillering_pro(filename, sheet_name='23.03.26(분얼전기', check_date = '3월 26일',  step_name = '분얼전기'):
    df_height = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=3).iloc[:17, :]
    df_length = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=24).iloc[:12, :]
    df_spad = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=40).iloc[:12, :]
    df_lai = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=56).iloc[:12, :]

    df_merged = preprocess_tilering(df_height, df_length, df_spad, df_lai, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged
def preprocess_tillering_telo(filename, sheet_name='23.04.17(분얼후기)', check_date = '4월 17일',  step_name = '분얼후기'):
    df_height = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=3).iloc[:12, :]
    # df_length = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=18).iloc[:5, :]
    df_spad = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=26).iloc[:12, :]
    df_lai = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=42).iloc[:12, :]

    df_height = melted(df_height, '초장(cm)')
    df_spad = melted(df_spad, 'SPAD')
    df_lai = melted(df_lai, 'LAI')

    df_merged = pd.merge(df_height, df_spad, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_lai, on=['rep', '조사지'], how='inner')

    df_merged = df_merged.rename(columns={'rep': '반복'})
    df_merged['조사일'] = check_date

    df_merged = preprocess_merge(df_merged, step_name)
    return df_merged

def preprocess_flowering1(filename, sheet_name='23.05.04(개화기)',  check_date = '5월 4일',  step_name = '개화기'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I')

    df_merged = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged


def preprocess_flowering2(filename, sheet_name='23.05.19(개화후2주)', check_date = '5월 18일',  step_name = '개화후2주'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:G')

    df_merged = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged


def preprocess_flowering4(filename, sheet_name='23.06.01(개화후4주)', check_date = '6월 2일',  step_name = '개화후4주'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:G')

    df_merged = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged


def preprocess_harvesting(filename, sheet_name='23.06.12(수확)', check_date = '6월 13일',  step_name = '수확기'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:J')

    df_merged = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_merged = preprocess_merge(df_merged, step_name)


    return df_merged

def final_preprocess(df):
    df['반복'] = pd.to_numeric(df['반복'], errors='coerce')  # 숫자로 변환, 변환 불가한 값은 NaN으로 처리
    df = df.dropna(subset=['반복'])
    df['조사지'] = df['조사지'].str.replace('Plot', '').str.strip().astype(int)
    df = df.sort_values(['조사지', '반복']).reset_index(drop=True)
    # print(df)

    df = df.reset_index().rename(columns={'index': 'ID'})
    df['ID'] = df['ID'] + 1

    df = df.drop(columns=['반복'])
    value_vars = [col for col in df.columns if 'ID' not in col]
    df_melted = pd.melt(df, id_vars=['ID'], value_vars=value_vars,
                        var_name='지표_생육단계', value_name='value')
    df_melted['지표'] = df_melted['지표_생육단계'].str.split('_').str[0]
    df_melted['생육단계'] = df_melted['지표_생육단계'].str.split('_').str[1]
    df_melted = df_melted.drop(columns='지표_생육단계')
    df_melted = df_melted.pivot_table(index=['ID', '생육단계'], columns='지표', values='value').reset_index()
    # print(df_melted.columns)
    df_melted = df_melted.rename(columns={'엽록소함량(µmol/m2)': 'SPAD', '군집(LAI)':'LAI'})
    # print(df_melted.shape)
    return df_melted


def generate_data(filename):
    tillering_pro = preprocess_tillering_pro(filename)
    tillering_telo = preprocess_tillering_telo(filename)
    flowering1 = preprocess_flowering1(filename)
    flowering2 = preprocess_flowering2(filename)
    flowering4 = preprocess_flowering4(filename)
    harvesting = preprocess_harvesting(filename)
    tillering_pro = final_preprocess(tillering_pro)
    tillering_telo = final_preprocess(tillering_telo)
    flowering1 = final_preprocess(flowering1)
    flowering2 = final_preprocess(flowering2)
    flowering4 = final_preprocess(flowering4)
    harvesting = final_preprocess(harvesting)

    df = pd.concat([tillering_pro, tillering_telo, flowering1, flowering2, flowering4, harvesting], ignore_index=True)

    # print(df['ID'].unique())
    return df

    # print(tillering_pro, tillering_pro.shape)
    # print(tillering_telo, tillering_telo.shape)
    # print(flowering1, flowering1.shape)
    # print(flowering2,   flowering2.shape)
    # print(flowering4, flowering4.shape)
    # print(harvesting, harvesting.shape)

    #
    # df_all = pd.merge(tillering_pro, tillering_telo, on=['반복', '조사지'], how='inner')
    # df_all = pd.merge(df_all, flowering1, on=['반복', '조사지'], how='inner')
    # df_all = pd.merge(df_all, flowering2, on=['반복', '조사지'], how='inner')
    # df_all = pd.merge(df_all, flowering4, on=['반복', '조사지'], how='inner')
    # df_all = pd.merge(df_all, harvesting, on=['반복', '조사지'], how='inner')
    # df_all.to_csv("./output/iksan_data_plant.csv", index=False)
    #
    # return df_all

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
    input_dir = '../input/2023'
    output_dir = '../output'
    os.makedirs(output_dir, exist_ok=True)


    growth_filename = os.path.join(input_dir, '생육조사결과.xlsx')
    drone_filename = os.path.join(input_dir, '샘플링위치별_식생지수및수확량.xlsx')

    # output_filename = os.path.join(output_dir, 'iksan_data_all_new.csv')

    growth_df = generate_data(growth_filename)

    drone_df = pd.read_excel(drone_filename)
    drone_df = prerpocess_drone(drone_df)

    growth_df.to_csv(os.path.join(output_dir, '2023_growth.csv'), index=False, encoding='utf-8-sig')
    drone_df.to_csv(os.path.join(output_dir, '2023_drone.csv'), index=False, encoding='utf-8-sig')

    # print(growth_df.columns)

    # merged = pd.merge(growth_df, drone_df, on=['ID', '생육단계'], how='inner')
    # merged.to_csv("../output/2023_growth.csv", index=False, encoding='utf-8-sig')

    # print(df_all[['관개', '시비', '파종']])
    # df_all.to_csv(output_filename, index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()