import os
import warnings
import pandas as pd
import tqdm

warnings.simplefilter("ignore")

def report_create_df(report_path, dir_name):
    dir_path = os.path.join(report_path, dir_name)
    filenames = os.listdir(dir_path)

    df_all = pd.DataFrame()
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        df_each = pd.read_csv(f"{file_path}", encoding='cp949')
        df_all = pd.concat([df_all, df_each])
    df = df_all[(df_all['맥종'] == '밀') & (df_all['년도'] == '본년')]
    df.drop(['맥종', '년도'], axis=1, inplace=True)
    df.columns = [x.replace('\n ', '') for x in df.columns]

    return df

def report_create_dict(dir_names, report_path):
    dict_dfs = {}

    for dir_name in tqdm.tqdm(dir_names):
        try:
            dict_dfs.update({dir_name: report_create_df(report_path, dir_name)})
        except KeyError:
            dict_dfs.update({dir_name: "KeyError"})  # method

    return dict_dfs

def report_merge(output_dir, site_info, report_path):
    list_item = ["growth", "length", "yield", "fruitful",
                 "method_1", "method_2", "method_3", "method_4",
                 "method_5", "method_6", "method_7"]

    dir_names = os.listdir(report_path)

    dict_dfs = report_create_dict(dir_names, report_path)

    list_dfs = []
    for item in list_item:
        df = dict_dfs[f'{item}'].reset_index().drop('index', axis=1)
        list_dfs.append(df)

    df = pd.concat(list_dfs, axis=1, join='outer')
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df = df[df['품종'] != '평균']

    for idx, row in site_info.iterrows():
        df.loc[df["지역"] == row['지역'], '지역'] = row['실제지역']

    df['station'] = df['지역'].astype(str).apply(lambda x: x.split('(')[0])
    df.to_csv(os.path.join(output_dir, "맥류작황보고서.csv"), index=False, encoding='utf-8-sig')

    return df

def report_summary_df(output_dir, site_info, report_path, list_condition):

    df = report_merge(output_dir, site_info, report_path)

    for condition, func in list_condition:
        df_condition = df.pivot_table(index='year', columns=condition, values='완전종실중(kg/10a)', aggfunc=func)
        df_condition.to_csv(os.path.join(output_dir, f"맥류작황보고서_{condition}별_생산량.csv"), encoding='utf-8-sig')


def main():
    output_dir = "../output/report/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    report_path = r"Z:\Projects\2302_2306_wheat_report\report"

    site_info = pd.read_excel("../input/맥류작황보고서_정보.xlsx")

    list_condition = [
        ('지역', 'sum'),
        ('품종', 'sum'),
        ('재배조건', 'sum')]

    report_merge(output_dir, site_info, report_path)
    report_summary_df(output_dir, site_info, report_path, list_condition)

if __name__ == '__main__':
    main()