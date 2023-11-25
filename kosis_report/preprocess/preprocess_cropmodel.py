import pandas as pd
import os

def dssat_result(info):
    data_dir = '../../input/dssat_results/'
    filenames = [x for x in os.listdir(data_dir) if x.endswith(".OOV.txt")]

    station_info = {}
    for filename in filenames:
        crop_info = {}
        with open(os.path.join(data_dir, filename), 'r') as file:
            for line in file:
                # ---- DSSAT results ----
                if 'STARTING DATE' in line:
                    year = line.split(':')[-1].strip().split(' ')[-1]
                elif 'Wheat YIELD' in line:
                    yield_value = float(line.split(':')[1].split('kg/ha')[0].strip())
                    crop_info.update({f'{year}': f'{yield_value}'})
        # ---- station info ----
        station = info[info['영문명'] == filename.split('.')[0].split('_')[-1]]
        station_nm = station['실제지역'].values[0].split('(')[0]
        station_info.update({station_nm: crop_info})

    df = pd.DataFrame(station_info)
    melted = df.reset_index().melt(id_vars='index', var_name='station', value_name='value')
    melted.columns = ['year', 'station', 'dssat_yield']
    melted['year'] = melted['year'].astype(int) + 1
    melted['dssat_yield'] = melted['dssat_yield'].astype(float) / 10
    melted = melted[melted['year'] != 2023]

    info['station'] = info['실제지역'].str.split('(').str[0]
    merged = pd.merge(info, melted, on='station', how='inner')

    merged = merged[['year', 'dssat_yield', '지점코드', '실제지역']]

    return merged
def aqua_result(info):
    data_dir = '../../input/apsim_results/'
    filenames = [x for x in os.listdir(data_dir) if x.endswith(".csv")]

    station_info = []
    for filename in filenames:
        each = pd.read_csv(os.path.join(data_dir, filename))
        each['year'] = each['Harvest Date (YYYY/MM/DD)']
        each = each[['year', 'Yield (tonne/ha)']]
        each_dict = each.to_dict('records')
        each_df = pd.DataFrame(each_dict)

        station =  info[info['영문명'] == filename.split('.')[0].split('_')[0]]['실제지역'].values[0]
        each_df['station'] = station.split('(')[0]
        station_info.append(each_df)


    all = pd.concat(station_info)
    all.columns = ['year', 'aqua_yield', 'station']
    all['year'] = all['year'].str.split('-').str[0].astype(int)
    all['aqua_yield'] = all['aqua_yield'].astype(float) * 100

    info['station'] = info['실제지역'].str.split('(').str[0]

    merged = pd.merge(info, all, on='station', how='inner')
    merged = merged[['year', 'aqua_yield', '지점코드', '실제지역']]
    return merged

def main():
    output_dir = "../output/cropmodel/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ------------ 맥류작황보고서_정보
    info = pd.read_excel('../input/맥류작황보고서_정보.xlsx')
    info.drop('지역', axis=1, inplace=True)

    # ------------ crop model results merge
    dssat = dssat_result(info)
    aqua = aqua_result(info)
    crop_model = pd.merge(dssat, aqua, on=['지점코드', 'year', '실제지역'], how='inner')
    crop_model.to_csv(os.path.join(output_dir, '작물모델결과.csv'), index=False)

if __name__ == '__main__':
    main()