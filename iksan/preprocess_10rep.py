import os
import re
import pandas as pd

input_dir = '../input/iksan'
output_dir = '../output'
iksan_dir = os.path.join(output_dir, 'iksan')
if not os.path.exists(iksan_dir):
    os.makedirs(iksan_dir)

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
    # df_merged = pd.merge(df_merged, df_fresh, on=['rep', '조사지'], how='inner')
    # df_merged = pd.merge(df_merged, df_dry, on=['rep', '조사지'], how='inner')
    # df_merged = pd.merge(df_merged, df_dryrate, on=['rep', '조사지'], how='inner')
    df_merged = df_merged.rename(columns={'rep': '반복'})
    df_merged['조사일'] = check_date
    df_merged['반복'] = df_merged['반복'].apply(lambda x: '평균' if x == 'avg' else ('표준편차' if x == 'stdev' else x))

    return df_merged


def preprocess_flowering_cols(df, check_date, col_seperator=None):
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
    df_growth = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_yield = preprocess_flowering_cols(df_yield, check_date, 'Unnamed')
    df_200 = preprocess_flowering_cols(df_200, check_date, 'Unnamed')
    df_gyeong = preprocess_flowering_cols(df_gyeong, check_date, '.')

    df_merged = pd.merge(df_growth, df_yield, on=['조사지', '조사일', '반복'], how='inner')
    df_merged = pd.merge(df_merged, df_200, on=['조사지', '조사일', '반복'], how='inner')
    df_merged = pd.merge(df_merged, df_gyeong, on=['조사지', '조사일', '반복'], how='inner')
    return df_growth
    # return df_merged


def preprocess_merge(df_merged, step_name):
    df_merged = df_merged.drop(columns='조사일')
    df_merged.columns = [col + f'_{step_name}' if '반복' not in col and '조사지' not in col else col for col in
                         df_merged.columns]
    return df_merged


def preprocess_tillering_pro(filename, sheet_name='23.03.26(분얼전기', check_date='3월 26일', step_name='분얼전기'):
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


def preprocess_tillering_telo(filename, sheet_name='23.04.17(분얼후기)', check_date='4월 17일', step_name='분얼후기'):
    df_height = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=3).iloc[:12, :]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=18).iloc[:5, :]
    df_spad = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=26).iloc[:12, :]
    df_lai = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I', skiprows=42).iloc[:12, :]
    df_fresh = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=3).iloc[:5, :]
    df_fresh.columns = [col.split('.')[0] for col in df_fresh.columns]
    df_dry = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=11).iloc[:5, :]
    df_dryrate = pd.read_excel(filename, sheet_name=sheet_name, usecols='K:S', skiprows=19).iloc[:5, :]

    # df_merged = preprocess_tilering(df_height, df_gyeong, df_spad, df_lai, df_fresh, df_dry, df_dryrate, check_date)

    df_height = melted(df_height, '초장(cm)')
    # df_gyeong = melted(df_gyeong, '경수(20*20cm2)')
    df_spad = melted(df_spad, 'SPAD')
    df_lai = melted(df_lai, 'LAI')
    df_fresh = melted(df_fresh, '생체중')
    df_dry = melted(df_dry, '건물중')
    df_dryrate = melted(df_dryrate, '건물중비율')

    # df_merged = pd.merge(df_height, df_length, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_height, df_spad, on=['rep', '조사지'], how='inner')
    df_merged = pd.merge(df_merged, df_lai, on=['rep', '조사지'], how='inner')
    # df_merged = pd.merge(df_merged, df_fresh, on=['rep', '조사지'], how='inner')
    # df_merged = pd.merge(df_merged, df_dry, on=['rep', '조사지'], how='inner')
    # df_merged = pd.merge(df_merged, df_dryrate, on=['rep', '조사지'], how='inner')
    df_merged = df_merged.rename(columns={'rep': '반복'})
    df_merged['조사일'] = check_date
    df_merged['반복'] = df_merged['반복'].apply(lambda x: '평균' if x == 'avg' else ('표준편차' if x == 'stdev' else x))

    df_merged = preprocess_merge(df_merged, step_name)
    return df_merged


def preprocess_flowering1(filename, sheet_name='23.05.04(개화기)', check_date='5월 4일', step_name='개화기'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:I')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 10:]

    df_growth = preprocess_flowering_cols(df_growth, check_date, '\n')
    df_yield = preprocess_flowering_cols(df_yield, check_date, 'Unnamed')

    df_merged = pd.merge(df_growth, df_yield, on=['조사지', '조사일', '반복'], how='inner')
    df_merged = preprocess_merge(df_merged, step_name)
    df_growth= preprocess_merge(df_growth, step_name)
    # return df_merged
    return df_growth


def preprocess_flowering2(filename, sheet_name='23.05.19(개화후2주)', check_date='5월 18일', step_name='개화후2주'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:G')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 9:]
    df_200 = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=[0, 1]).iloc[:32, 9:15]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=0).iloc[1:, 16:21]

    df_merged = preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged


def preprocess_flowering4(filename, sheet_name='23.06.01(개화후4주)', check_date='6월 2일', step_name='개화후4주'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:G')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 8:]
    df_200 = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=[0, 1]).iloc[:32, 8:14]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=0).iloc[1:40, 15:20]

    df_merged = preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    return df_merged


def preprocess_harvesting(filename, sheet_name='23.06.12(수확)', check_date='6월 13일', step_name='수확기'):
    df_growth = pd.read_excel(filename, sheet_name=sheet_name, usecols='A:J')
    df_yield = pd.read_excel(filename, sheet_name=sheet_name, header=[0, 1]).iloc[:32, 11:]
    df_200 = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=[0, 1]).iloc[:32, 11:17]
    df_gyeong = pd.read_excel(filename, sheet_name=sheet_name, skiprows=36, header=0).iloc[1:49, 18:23]

    df_merged = preprocess_flowering(df_growth, df_yield, df_200, df_gyeong, check_date)
    df_merged = preprocess_merge(df_merged, step_name)

    df_actual = pd.read_excel(filename, sheet_name=sheet_name, skiprows=72, usecols='L:N').iloc[1:9, :]

    return df_merged


def preprocess_drone():
    drone_filename = '../input/iksan/샘플링위치별_식생지수및수확량.xlsx'
    df = pd.read_excel(drone_filename, sheet_name='샘플링위치별_식생지수및수확량')
    df['조사지'] = df['ID'].apply(lambda x: f'Plot {((x - 1) // 10) + 1}')
    df['반복'] = df.groupby('조사지').cumcount() + 1
    # date_list = [col.split('_')[0] for col in df.columns if '_' in col]
    # ['230501', '230601', '230130', '230321', '230615', '230417', '230520']
    # ['230326', '230417', '230504', '230519', '230601', '230612']
    date_dict = {'230130': '분얼전', '230321': '분얼전기', '230417': '분얼후기', '230501': '개화기', '230520': '개화후2주',
                 '230601': '개화후4주', '230615': '수확기'}
    df.columns = [f'{col.split("_")[1]}_{date_dict[col.split("_")[0]]}' if '_' in col else col for col in df.columns]
    df = df.rename(columns={'yield(kg/10a)': 'drone_yield'})
    df = df.drop(columns=['ID'])
    return df


# Plot1	관행
# Plot2	관행+시비
# Plot3	관행+관개+시비
# Plot4	관행+관개
# Plot5	세조파
# Plot6	세조파+시비
# Plot7	세조파+관개+시비
# Plot8	세조파+관개
# 관행, 시비, 관개, 세조파
# 관개: plot 3, 4, 7, 8
# 파종: plot 5, 6, 7, 8
# 시비: plot 2, 3, 6, 7

def generate_data(filename):
    tillering_pro = preprocess_tillering_pro(filename)
    tillering_telo = preprocess_tillering_telo(filename)
    flowering1 = preprocess_flowering1(filename)
    flowering2 = preprocess_flowering2(filename)
    flowering4 = preprocess_flowering4(filename)
    harvesting = preprocess_harvesting(filename)

    drone = preprocess_drone()

    df_all = pd.merge(tillering_pro, tillering_telo, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, flowering1, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, flowering2, on=['반복', '조사지'], how='inner')
    df_all = pd.merge(df_all, flowering4, on=['반복', '조사지'], how='inner')
    # df_all = pd.merge(df_all, harvesting, on=['반복', '조사지'], how='inner')
    # df_all.to_csv("../output/iksan_data_plant.csv", index=False)
    df_all = pd.merge(df_all, drone, on=['반복', '조사지'], how='inner')
    df_all['관개'] = 0
    df_all['시비'] = 0
    df_all['파종'] = 0
    df_all['관개'] = df_all['조사지'].apply(
        lambda x: 1 if x == 'Plot 3' or x == 'Plot 4' or x == 'Plot 7' or x == 'Plot 8' else 0)
    df_all['시비'] = df_all['조사지'].apply(
        lambda x: 1 if x == 'Plot 2' or x == 'Plot 3' or x == 'Plot 6' or x == 'Plot 7' else 0)
    df_all['파종'] = df_all['조사지'].apply(
        lambda x: 1 if x == 'Plot 5' or x == 'Plot 6' or x == 'Plot 7' or x == 'Plot 8' else 0)
    print(df_all.columns)
    print(df_all.shape)

    # df_drone = pd.merge(drone, harvesting, on=['반복', '조사지'], how='inner')
    # df_drone.to_csv("../output/iksan_data_drone.csv", index=False)

    return df_all


def main():
    filename = os.path.join(input_dir, '생육조사결과.xlsx')

    output_filename = os.path.join(iksan_dir, 'iksan_10data.csv')

    df_all = generate_data(filename)
    # print(df_all[['관개', '시비', '파종']])
    df_all.to_csv(output_filename, index=False)


if __name__ == '__main__':
    main()