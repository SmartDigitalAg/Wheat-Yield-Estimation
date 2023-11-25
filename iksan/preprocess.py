import os
import re
import pandas as pd

def melted(df, value_name):
    df_melted = df.melt(id_vars='rep', var_name='조사지', value_name=value_name)
    return df_melted

def preprocess_tilering(df_height, df_length, df_spad, df_lai, df_fresh, df_dry, df_dryrate, check_date):
    df_height = melted(df_height, '초장(cm)')
    df_length = melted(df_length, '유수길이(mm)')
    df_spad = melted(df_spad, 'SPAD')
    df_lai = melted(df_lai, 'LAI')
    df_fresh = melted(df_fresh, '생체중')
    df_dry = melted(df_dry, '건물중')
    df_dryrate = melted(df_dryrate, '건물중비율')

    df_merged = pd.merge(df_height, df_length, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_spad, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_lai, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_fresh, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_dry, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_dryrate, on=['rep', '조사지'], how='inner')
    df_merged = df_merged.rename(columns={'rep': '반복'})
    df_merged['조사일'] = check_date
    df_merged['반복'] = df_merged['반복'].apply(lambda x: '평균' if x == 'avg' else ('표준편차' if x=='stdev' else x))

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

def preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date):
    df_growth = preprocess_flowering_cols(df_growth, check_date,'\n')
    df_yield = preprocess_flowering_cols(df_yield, check_date, 'Unnamed')
    df_200 = preprocess_flowering_cols(df_200, check_date,  'Unnamed')
    df_gyeong = preprocess_flowering_cols(df_gyeong, check_date, '.')
    
    df_merged = pd.merge(df_growth, df_yield, on=['조사지', '조사일', '반복'], how='inner')
    df_merged = pd.merge(df_merged, df_200, on=['조사지', '조사일', '반복'], how='inner')
    df_merged = pd.merge(df_merged, df_gyeong, on=['조사지', '조사일', '반복'], how='inner')
    return df_merged


def preprocess_merge(df_merged, step_name):
    df_merged = df_merged.drop(columns='조사일')
    df_merged.columns = [col + f'_{step_name}' if '반복' not in col and '조사지' not in col else col for col in df_merged.columns]
    return df_merged

def preprocess_tillering_pro(filename, sheet_name='23.03.26(분얼전기', check_date = '3월 26일',  step_name = '분얼전기'):
    df_height = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=3).iloc[:17, :]
    df_length = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=24).iloc[:12, :]
    df_spad = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=40).iloc[:12, :]
    df_lai = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=56).iloc[:12, :]
    df_fresh = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=3).iloc[:5, :]
    df_fresh.columns = [col.split('.')[0] for col in df_fresh.columns]
    df_dry = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=11).iloc[:5, :]
    df_dryrate = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=19).iloc[:5, :]


    df_merged = preprocess_tilering(df_height, df_length, df_spad, df_lai, df_fresh, df_dry, df_dryrate, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged


def preprocess_tillering_telo(filename, sheet_name='23.04.17(분얼후기)', check_date = '4월 17일',  step_name = '분얼후기'):
    df_height = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=3).iloc[:12, :]
    df_length = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=18).iloc[:5, :]
    df_spad = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=26).iloc[:12, :]
    df_lai = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=42).iloc[:12, :]
    df_fresh = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=3).iloc[:5, :]
    df_fresh.columns = [col.split('.')[0] for col in df_fresh.columns]
    df_dry = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=11).iloc[:5, :]
    df_dryrate = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=19).iloc[:5, :]


    df_merged = preprocess_tilering(df_height, df_length, df_spad, df_lai, df_fresh, df_dry, df_dryrate,  check_date)
    df_merged = preprocess_merge(df_merged, step_name)
    return df_merged

def preprocess_flowering1(filename, sheet_name='23.05.04(개화기)',  check_date = '5월 4일',  step_name = '개화기'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 10:]

    df_growth = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_yield = preprocess_flowering_cols(df_yield, check_date, 'Unnamed')

    df_merged = pd.merge(df_growth, df_yield, on=['조사지', '조사일', '반복'], how='inner')
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged

def preprocess_flowering2(filename, sheet_name='23.05.19(개화후2주)', check_date = '5월 18일',  step_name = '개화후2주'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:G')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 9:]
    df_200 = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=[0, 1]).iloc[:32, 9:15]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=0).iloc[1:, 16:21]

    df_merged = preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged

def preprocess_flowering4(filename, sheet_name='23.06.01(개화후4주)', check_date = '6월 2일',  step_name = '개화후4주'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:G')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 8:]
    df_200 = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=[0, 1]).iloc[:32, 8:14]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=0).iloc[1:40, 15:20]

    df_merged = preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged

def preprocess_harvesting(filename, sheet_name='23.06.12(수확)', check_date = '6월 13일',  step_name = '수확기'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:J')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 11:]
    df_200 = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=[0, 1]).iloc[:32, 11:17]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=0).iloc[1:49, 18:23]

    df_merged = preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date)
    df_merged = preprocess_merge(df_merged, step_name)


    df_actual = pd.read_excel(filename, sheet_name=sheet_name, skiprows=72, usecols='L:N').iloc[1:9, :]

    return df_merged

def generate_data(filename):
    tillering_pro = preprocess_tillering_pro(filename)
    tillering_telo = preprocess_tillering_telo(filename)
    flowering1 = preprocess_flowering1(filename)
    flowering2 = preprocess_flowering2(filename)
    flowering4 = preprocess_flowering4(filename)
    harvesting = preprocess_harvesting(filename)

    df_all = pd.merge(tillering_pro, tillering_telo, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, flowering1, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, flowering2, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, flowering4, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, harvesting, on=['반복', '조사지'], how='inner')

    return df_all

def main():
    filename = '../input/iksan/생육조사결과.xlsx'

    output_dir = '../output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_filename = os.path.join(output_dir, 'iksan_data.csv')

    df_all = generate_data(filename)
    df_all.to_csv(output_filename, index=False)

if __name__ == '__main__':
    main()
