import pandas as pd
import os


def add_stage(x):

    if x <= pd.to_datetime("2024-03-21"):
        return "분얼전기"
    elif pd.to_datetime("2024-03-21") < x <= pd.to_datetime("2024-04-11"):
        return "분얼후기"
    elif pd.to_datetime("2023-04-11") < x <= pd.to_datetime("2024-04-26"):
        return "개화기"
    elif pd.to_datetime("2023-04-26") < x <= pd.to_datetime("2023-05-09"):
        return "개화후2주"
    elif pd.to_datetime("2023-05-09") < x <= pd.to_datetime("2023-05-24"):
        return "개화후4주"
    elif pd.to_datetime("2023-05-24") < x:
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

    result = result[result['ID'] !=0]
    return result

def main():
    data_dir = './input/2024'
    df = concat_vegetation_indices(data_dir)
    df = prerpocess_drone(df)
    print(df)

    # date_dict = {'240321':'분얼전기', '240411':'분얼후기', '240426':'개화기', '240509':'개화후2주', '240524':'개화후4주',  '240607':'수확기'}
    # df.columns = [f'{col.split("_")[1]}_{date_dict[col.split("_")[0]]}' if '_' in col else col for col in df.columns]
    # print(df)



if __name__ == '__main__':
    main()