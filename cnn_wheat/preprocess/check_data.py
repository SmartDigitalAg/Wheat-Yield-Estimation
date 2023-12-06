import numpy as np
import pandas as pd
import os

def check_date(ndvi_dir, evi_dir, lai_dir, lst_dir):
    ndvi_list = os.listdir(ndvi_dir)
    ndvi_list = [x.split('.')[1] for x in ndvi_list if x.endswith('.tif')]
    evi_list = os.listdir(evi_dir)
    evi_list = [x.split('.')[1] for x in evi_list if x.endswith('.tif')]
    lai_list = os.listdir(lai_dir)
    lai_list = [x.split('.')[1] for x in lai_list if x.endswith('.tif')]
    lst_list = os.listdir(lst_dir)
    lst_list = [x.split('.')[1] for x in lst_list if x.endswith('.tif')]



    diff = list(set(lst_list) - set(ndvi_list))
    # ['2015169', '2015329', '2015313', '2015201', '2015361', '2015025', '2015105', '2015089', '2015185', '2015137', '2015009', '2015041',
    # '2015265', '2015057', '2015153', '2015121', '2015217', '2015249', '2015281', '2015233', '2015297', '2015073', '2015345']


    print(diff)
    print(len(ndvi_list)) # 24
    print(len(evi_list)) # 23
    print(len(lai_list))
    print(len(lst_list)) # 48


def list2df(dir_name, col_name):
    files = os.listdir(dir_name)
    files = [x for x in files if x.endswith('.tif')]
    df = pd.DataFrame(files, columns=[col_name])
    df['date'] = df[col_name].apply(lambda x: x.split('.')[1].replace('A', ''))

    return df
    

def files2csv(ndvi_dir, evi_dir, lai_dir, lst_dir):
    date_list = [x.split('.')[1].replace('A', '') for x in os.listdir(ndvi_dir)]
    df = pd.DataFrame(date_list, columns=['date'])
    ndvi_df = list2df(ndvi_dir, 'ndvi')
    evi_df = list2df(evi_dir, 'evi')
    lai_df = list2df(lai_dir, 'lai')
    lst_df = list2df(lst_dir, 'lst')


    df = pd.merge(df, ndvi_df, on='date', how='inner')
    df = pd.merge(df, evi_df, on='date', how='inner')
    df = pd.merge(df, lst_df, on='date', how='inner')
    df = pd.merge(df, lai_df, on='date', how='inner')

    df = df.drop_duplicates()

    df.to_csv('./output/filenames.csv', index=False)



def main():
    data_dir = r'D:\DATA\wheat\1_inputdata'

    # NDVI
    ndvi_dir = os.path.join(data_dir, '1_ndvi')
    # EVI
    evi_dir = os.path.join(data_dir, '2_evi')
    # LAI
    lai_dir = os.path.join(data_dir, '3_lai')
    #lst_day
    lst_dir = os.path.join(data_dir, '4_lst')
    # yield
    yield_filename = os.path.join(data_dir, '2015_rice_yield.tif')

    check_date(ndvi_dir, evi_dir, lai_dir, lst_dir)

    files2csv(ndvi_dir, evi_dir, lai_dir, lst_dir)



#히스토그램 추출과 시계열 융합을 통한 신경망 샘플 구축 과정
if __name__ == '__main__':
    main()