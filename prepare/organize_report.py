import os
import pandas as pd

report_path = r"Z:\Projects\2302_2306_wheat_report\report"

input_dir = '../input'
output_dir = '../output'
report_dir = os.path.join(output_dir, 'report')
if not os.path.exists(report_dir):
    os.makedirs(report_dir)
concated_dir = os.path.join(report_dir, 'concated')
if not os.path.exists(concated_dir):
    os.makedirs(concated_dir)
anova_dir = os.path.join(report_dir, 'anova')
if not os.path.exists(anova_dir):
    os.makedirs(anova_dir)

report_weather_dir = os.path.join(report_dir, 'report_weather')
if not os.path.exists(report_weather_dir):
    os.makedirs(report_weather_dir)

def read_csv():
    lst = []
    dct = {}
    for root_dir, dirs, files in os.walk(report_path):

        if root_dir != report_path:
            basename = os.path.basename(root_dir)
            save_path = os.path.join(concated_dir, f'{basename}.csv')
            all_df = pd.DataFrame()
            if os.path.exists(save_path):
                for file in files:
                    df = pd.read_csv(os.path.join(root_dir, file), encoding='cp949')
                    all_df = pd.concat([all_df, df], ignore_index=True)
                all_df.columns = [col.strip().replace('\n', '').replace(' ', '') for col in all_df.columns]
                all_df = all_df[(all_df['맥종'] == '밀') & (all_df['지역'].notna()) & (all_df['year'] != 2023)]

                if basename == 'stage':
                    common_col = ['맥종', '지역', '재배조건', '품종', 'year']
                    all_df['year'] = all_df['year'] - 1
                    c_df = all_df[all_df['년도'] == '본년'].drop(columns=['출현기'])
                    p_df = all_df[all_df['년도'] == '전년'][common_col + ['출현기']]
                    all_df = pd.merge(c_df, p_df, on=common_col, how='inner')

                elif basename == 'method':
                    all_df = all_df[['맥종', '지역', '재배조건', '품종', '파종기', 'year',]]
                else:
                    all_df = all_df[(all_df['년도'] == '본년')]
                    all_df = all_df.drop(columns=['년도'])

                all_df.to_csv(save_path, index=False)
            else:
                all_df = pd.read_csv(save_path)
            dct[basename] = all_df

            # for column in all_df.columns:
            #     if all_df[column].apply(lambda x: '-' in str(x)).any():
            #         lst.append(column)

    # lst = [element for sublist in lst for element in sublist]
    # print(list(set(lst)))
    # '출현기', '파종기', '출수시', '출수기', '출수전', '최고분얼기', '생육재생기', '성숙기'
    return dct

def merged_dfs():
    dct = read_csv()
    common_col = ['맥종', '지역', '재배조건', '품종', 'year']
    merged = pd.merge(dct['count'], dct['fruitful'], on=common_col, how='inner')
    merged = pd.merge(merged, dct['growth'], on=common_col, how='inner')
    merged = pd.merge(merged, dct['length'], on=common_col, how='inner')
    # merged = pd.merge(merged, dct['method'], on=common_col, how='inner')
    # merged = pd.merge(merged, dct['stage'], on=common_col, how='inner')
    merged = pd.merge(merged, dct['yield'], on=common_col, how='inner')
    merged.to_csv(os.path.join(report_dir, '맥류작황보고서.csv'), index=False)
    return merged

def report_summary_df(list_condition):

    df = merged_dfs()

    for condition, func in list_condition:
        df_condition = df.pivot_table(index='year', columns=condition, values='완전종실중(kg/10a)', aggfunc=func)
        df_condition.to_csv(os.path.join(report_dir, f"맥류작황보고서_{condition}별_생산량.csv"), encoding='utf-8-sig')

def report_r(df):
    '''
    R 통계분석 위한 데이터 생성
    '''
    
    # 완전종실중과 품종
    type = df[['완전종실중(kg/10a)', '품종']]
    type.columns = ['yield', 'type']
    dct = {type: f'type{idx+1}' for idx, type in enumerate(type['type'].unique())}
    type['type'] = type['type'].apply(lambda x: dct[x])
    type.to_csv(os.path.join(anova_dir, f"맥류작황보고서_품종.csv"), index=False, encoding='utf-8-sig')

    #


def main():
    list_condition = [
        ('지역', 'mean'),
        ('품종', 'mean'),
        ('재배조건', 'mean')]
    report_summary_df(list_condition)

    df = pd.read_csv(os.path.join(report_dir, '맥류작황보고서.csv'))
    report_r(df)



if __name__ == '__main__':
    main()