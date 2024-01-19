import os
import pandas as pd

output_dir = '../output'
report_dir = os.path.join(output_dir, 'report')
concated_dir = os.path.join(report_dir, 'concated')

def data_concated():
    excel_writer = pd.ExcelWriter(os.path.join(concated_dir, '데이터명세서.xlsx'))
    for root, dirs, files in os.walk(concated_dir):
        for file in files:
            if file.lower().endswith('.csv'):
                df = pd.read_csv(os.path.join(root, file))
                df_datatypes = pd.DataFrame(df.dtypes, columns=['Data Type'])
                sheet_name = os.path.splitext(file)[0]
                df_datatypes['Example Value'] = df.iloc[0]
                df_datatypes.to_excel(excel_writer, sheet_name=sheet_name, index_label='Column Name')

    excel_writer.close()

def main():

    data_concated()



if __name__ == '__main__':
    main()