import os
import pandas as pd

report_path = r"Z:\Projects\2302_2306_wheat_report\report"

input_dir = '../input'
report_dir = '../output/report'

concated_dir = os.path.join(report_dir, 're_concated')
if not os.path.exists(concated_dir):
    os.makedirs(concated_dir)

re_data_dir = os.path.join(report_dir, 're_datas')
if not os.path.exists(re_data_dir):
    os.makedirs(re_data_dir)
# report_weather_dir = os.path.join(report_dir, 'report_weather')
# if not os.path.exists(report_weather_dir):
#     os.makedirs(report_weather_dir)

date_dct = {1: ['출현기', '12월10일'], 2: ['생육재생기', '2월20일'], 3: ['생육재생기', '3월20일'], 4: ['최고분얼기', '4월10일'],
            5: ['출수기', '5월1일'], 6: ['출수기'], 7: ['성숙기']}
search_date = {}

col_dct = {'count': ['맥종', '지역', '재배조건', '품종', '년도', '1수영화수(개)', '결실립수(개)', '간중(kg/10a)', '간중대종실중비율(%)'],
           'fruitful': ['맥종', '지역', '재배조건', '품종', '년도', '경수(cm)_12월10일', '경수(cm)_2월20일', '경수(cm)_3월20일', '경수(cm)_4월10일',
                        '경수(cm)_5월1일', '유효경비율(%)', '수수(개/m2)'],
           'growth': ['맥종', '지역', '재배조건', '품종', '년도', '생체중(g/㎡)', '건물중(g/㎡,%)', '건물중비율(%)'],
           'length': ['맥종', '지역', '재배조건', '품종', '년도', '초장(cm)_12월10일', '초장(cm)_2월20일', '초장(cm)_3월20일', '초장(cm)_4월10일',
                      '초장(cm)_5월1일', '간장(cm)'],
           # 'method': ['시험년도', '지역', '맥종', '품종', '재배조건', '파폭', '시비량_기비_N', '시비량_기비_K20', '시비량_기비_P205', '시비량_추비_N', '파종기', '파종량', '휴폭(cm)'],
           'stage': ['맥종', '지역', '재배조건', '품종', '년도', '출현기', '생육재생기', '최고분얼기', '출수기', '성숙기'],
           'yield': ['맥종', '지역', '재배조건', '품종', '년도', '완전종실중(kg/10a)', '설립중(kg/10a)', 'l중(g)', '1,000립중(g)', '수장(cm)']}
drop_cols = ['병해(0-9)', '충해(0-9)', '도복(0-9)', '한발해(0-9)', '습해(0-9)', '기타재해(0-9)']


def read_csv():
    dct = {}
    for root_dir, dirs, files in os.walk(report_path):

        if root_dir != report_path:
            basename = os.path.basename(root_dir)
            df = pd.concat([pd.read_csv(os.path.join(root_dir, file), encoding='cp949') for file in files if not '2023' in file],
                           ignore_index=True)
            df.columns = [col.strip().replace('\n', '').replace(' ', '') for col in df.columns]
            if 'method_' in basename:
                method_try = int(basename.split('_')[-1])
                df = df.drop(columns='year')
                df = df[(df['품종'] != '평균') & (df['맥종'] == '밀')]
                df['year'] = df[date_dct[method_try][0]].apply(lambda x: x.split('-')[0] if type(x) == str else x)
                df = df[[col for col in df.columns if not col in drop_cols]]


                if method_try < 6:
                    if method_try == 1:
                        df['year'] = (df['year'].astype(int) + 1).astype(str)
                    rename_dct1 = {col: f'초장(cm)_{date_dct[method_try][1]}' for col in df.columns if '초장' in col}
                    rename_dct2 = {col: f'경수(개/㎡)_{date_dct[method_try][1]}' for col in df.columns if '경수' in col}

                    df = df.rename(columns=rename_dct1)
                    df = df.rename(columns=rename_dct2)

                # if method_try >= 6:
                #     df = df.rename(columns={'1수립수(개)': f'1수립수(개)_{method_try}'})
                df = df[df['년도']=='본년']
                df = df.drop(columns='년도')

                df.to_csv(os.path.join(concated_dir, f'{basename}.csv'), index=False, encoding='utf-8-sig')
                dct[method_try] = df
            if basename == 'method':
                df.to_csv(os.path.join(concated_dir, f'{basename}.csv'), index=False, encoding='utf-8-sig')
    return dct


def merged():
    dct = {}
    common_col = ['맥종', '지역', '재배조건', '품종', 'year']
    for i in range(1, 8):
        i_cols = common_col + [date_dct[i][0]]
        if i <= 4:
            cols = [f'초장(cm)_{date_dct[i][1]}', f'경수(개/㎡)_{date_dct[i][1]}']
        elif i == 5:
            cols = [f'초장(cm)_{date_dct[i][1]}', f'경수(개/㎡)_{date_dct[i][1]}', '유효경비율(%)']
        elif i == 6:
            cols = ['출수기생체중(g/㎡)', '출수기건물중(g/㎡)', '출수기건물중비율(%)', '수수(개/㎡)', '수장(cm)', '1수립수(개)', '간장(cm)']
        else:
            cols = ['완전종실중(kg/10a)', '설립중(kg/10a)', '리터중(g)', '천립중(g)','1수영화수(개)', '간중(kg/10a)', '간중종실중비율(%)']
        method = f'method_{i}'
        df = pd.read_csv(os.path.join(concated_dir, f'{method}.csv'))[i_cols + cols]

        dct[method] = df
    df = pd.merge(dct['method_1'], dct['method_2'], on=common_col, how='left' )
    df = pd.merge(df, dct['method_3'], on=common_col, how='left' )
    df = pd.merge(df, dct['method_4'], on=common_col, how='left' )
    df = pd.merge(df, dct['method_5'], on=common_col, how='left' )
    df = pd.merge(df, dct['method_6'], on=common_col, how='left' )
    df = pd.merge(df, dct['method_7'], on=common_col, how='left' )
    df = df.rename(columns={'1수립수(개)':'결실립수(개)'})
    y_cols = [col for col in df.columns if '_y' in col]
    rename_cols = {col: col.replace('_x', '') for col in df.columns if 'x' in col}
    df = df.drop(columns=y_cols)
    df = df.rename(columns=rename_cols)
    df.to_csv(os.path.join(re_data_dir, '맥류작황보고서.csv'), index=False)
    return df







# def merged():
#     dct = read_csv()
#     df = pd.merge(dct[1], dct[2], on=['맥종', '지역', '재배조건', '품종', 'year'], how='left')
#     df = pd.merge(df, dct[3], on=['맥종', '지역', '재배조건', '품종', 'year'], how='left')
#     df = pd.merge(df, dct[4], on=['맥종', '지역', '재배조건', '품종', 'year'], how='left')
#     df = pd.merge(df, dct[5], on=['맥종', '지역', '재배조건', '품종', 'year'], how='left')
#     df = pd.merge(df, dct[6], on=['맥종', '지역', '재배조건', '품종', 'year'], how='left')
#     df = pd.merge(df, dct[7], on=['맥종', '지역', '재배조건', '품종', 'year'], how='left')
#     # df = df[df['년도'] == '본년']
#     y_cols = [col for col in df.columns if '_y' in col]
#     rename_cols = {col: col.replace('_x', '') for col in df.columns if 'x' in col}
#     df = df.drop(columns=y_cols)
#     df = df.rename(columns=rename_cols)
#     df = df.rename(columns={'1수립수(개)_6': '결실립수(개)'})
#
#     df.to_csv(os.path.join(concated_dir, 'merged.csv'), index=False, encoding='utf-8-sig')
#     df.to_csv(os.path.join(re_data_dir, '맥류작황보고서.csv'), index=False)
#     type = df[df['품종'] == '조품밀']
#     category_order = ['0566', '전주(국립식량과학원)']
#     type['지역'] = pd.Categorical(type['지역'], categories=category_order, ordered=True)
#
#     # 'category' 열을 기준으로 정렬
#     type = type.sort_values(by='지역')
#
#     type.to_csv(os.path.join(re_data_dir, '조품밀.csv'), index=False, encoding='utf-8-sig')
#
#
#     return df


def organize(all_df):
    common_cols = ['맥종', '지역', '재배조건', '품종', 'year']
    title_dct = {'count': common_cols + ['1수영화수(개)', '결실립수(개)', '간중(kg/10a)', '간중종실중비율(%)'],  # , '결실립수(개)'
                 'fruitful': common_cols + ['경수(개/㎡)_12월10일', '경수(개/㎡)_2월20일', '경수(개/㎡)_3월20일', '경수(개/㎡)_4월10일',
                                            '경수(개/㎡)_5월1일', '유효경비율(%)', '수수(개/㎡)'],
                 'growth': common_cols + ['출수기생체중(g/㎡)', '출수기건물중(g/㎡)', '출수기건물중비율(%)'],
                 'length': common_cols + ['초장(cm)_12월10일', '초장(cm)_2월20일', '초장(cm)_3월20일', '초장(cm)_4월10일',
                                          '초장(cm)_5월1일', '간장(cm)'],
                 'stage': common_cols + ['출현기', '생육재생기', '최고분얼기', '출수기', '성숙기'],
                 'yield': common_cols + ['완전종실중(kg/10a)', '설립중(kg/10a)', '리터중(g)', '천립중(g)', '수장(cm)']
                 }


    dct = {}
    for title, cols in title_dct.items():
        df = all_df[cols]
        dct[title] = df
        df.to_csv(os.path.join(concated_dir, f'{title}.csv'), index=False, encoding='utf-8-sig')

        # if title == 'stage':
        #     seed = pd.read_csv(os.path.join(concated_dir, f'method.csv'))
        #     seed['year'] = (seed['시험년도'] + 1).astype(str)
        #     dates = pd.merge(df, seed, on=common_cols, how='inner')
        #     # dates = dates[(dates['year'] != '2023') & (dates['year'] != '2024')]
        #     dates.to_csv(os.path.join(concated_dir, f'dates.csv'), index=False, encoding='utf-8-sig')

    return dct

# def merged_dfs():
#     dct = organize()
#     common_col = ['맥종', '지역', '재배조건', '품종', 'year', '년도']
#     merged = pd.merge(dct['count'], dct['fruitful'], on=common_col, how='inner')
#     print("count+fruitful", merged.shape)
#     merged = pd.merge(merged, dct['growth'], on=common_col, how='inner')
#     merged = pd.merge(merged, dct['length'], on=common_col, how='inner')
#     # merged = pd.merge(merged, dct['method'], on=common_col, how='inner')
#     # merged = pd.merge(merged, dct['stage'], on=common_col, how='inner')
#     merged = pd.merge(merged, dct['yield'], on=common_col, how='inner')
#     merged.to_csv(os.path.join(re_data_dir, '맥류작황보고서.csv'), index=False)
#
#     for col_name in ['count', 'fruitful', 'growth', 'length', 'yield']:
#         print(col_name, dct[col_name].shape)
#     return merged


def report_summary_df(list_condition, df):


    for condition, func in list_condition:
        df_condition = df.pivot_table(index='year', columns=condition, values='완전종실중(kg/10a)', aggfunc=func)
        df_condition.to_csv(os.path.join(re_data_dir, f"맥류작황보고서_{condition}별_생산량.csv"), encoding='utf-8-sig')


def main():
    read_csv()
    df = merged()
    organize(df)

    list_condition = [
        ('지역', 'mean'),
        ('품종', 'mean'),
        ('재배조건', 'mean')]
    report_summary_df(list_condition, df)




if __name__ == '__main__':
    main()