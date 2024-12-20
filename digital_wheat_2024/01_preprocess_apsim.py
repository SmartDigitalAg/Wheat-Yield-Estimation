import pandas as pd
import os


def preprocess_apsim(data_file_name, harvest_date):

    df = pd.read_csv(data_file_name)
    # df = df[['Date', 'plot', 'yield']]

    df['site'] = df['site'].apply(lambda x: x.split('.')[0].replace('plot', '').replace('Plot', '')).astype(int)
    # df = df[df['site'] == df['plot']]
    df = df[df['Date'] == harvest_date]

    df = df[['site', 'yield']]
    df['yield'] = df['yield'].apply(lambda x:(int(x) * 1000) / 10000)
    df = df.rename(columns={'site': '조사지', 'yield': 'yield_apsim'})
    df['조사지'] ="Plot " + df['조사지'].astype(str)

    return df

def main():
    input_dir = "./input"

    df = pd.DataFrame()
    year_harvest = {'2024': '2024-05-24', '2023': '2023-06-15'}
    for year, harvest_date in year_harvest.items():
        data_dir = os.path.join(input_dir, year, 'apsim')
        data_file_name = os.path.join(data_dir, 'apsim_results_long.csv')

        each_df = preprocess_apsim(data_file_name, harvest_date)
        each_df['year'] = year
        df = pd.concat([df, each_df])

        # each_df = pd.read_csv(data_file_name)
        # each_df = each_df[['year', 'site', 'yield']]
        # each_df['yield'] = each_df['yield'].apply(lambda x: (int(x) * 1000) / 10000)
        # each_df['site'] = "Plot " + each_df['site'].apply(
        #     lambda x: x.replace(".out", "").replace("plot", "").replace("Plot", ""))
        # each_df = each_df.rename(columns={'site': '조사지', 'yield': 'yield_apsim'})
    df.to_csv(os.path.join(input_dir, 'apsim_data_new_long.csv'), index=False)


    # df = pd.DataFrame()
    # year_harvest = {'2024': '2024-05-24', '2023':'2023-06-15'}
    # for year, harvest_date in year_harvest.items():
    #     data_dir = os.path.join(input_dir, year, 'apsim')
    #     data_file_name = os.path.join(data_dir, 'apsim_results.csv')
    #     each_df = pd.read_csv(data_file_name)
    #     each_df = each_df[['year', 'site', 'yield']]
    #     each_df['yield'] = each_df['yield'].apply(lambda x: (int(x) * 1000) / 10000)
    #     each_df['site'] = "Plot "+ each_df['site'].apply(lambda x: x.replace(".out", "").replace("plot", "").replace("Plot", ""))
    #     each_df = each_df.rename(columns={'site': '조사지', 'yield': 'yield_apsim'})
    #     df = pd.concat([df, each_df])
    # df.to_csv(os.path.join(input_dir, 'apsim_data_new.csv'), index=False)
    #     each_df = preprocess_apsim(data_file_name, harvest_date)
    #     each_df['year'] = year
    #     df = pd.concat([df, each_df])
    # df.to_csv(os.path.join(input_dir, 'apsim_data.csv'), index=False)






if __name__ == '__main__':
    main()