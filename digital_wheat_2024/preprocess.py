import pandas as pd


def main():
    input_dir = './input/'

    data_2024 = pd.read_csv(input_dir + '2024_data.csv')
    data_2024['year'] = 2024
    data_2023 = pd.read_csv(input_dir + '2023_data.csv')
    data_2023['year'] = 2023
    cols = []
    for col in data_2023.columns:
        if "엽록소함량" in col:
            col = "SPAD" + "_" + col.split("_")[1]
        elif "군집" in col:
            col = "LAI" + "_" + col.split("_")[1]
        else:
            col = col
        cols.append(col)
    data_2023.columns = cols

    data_2023 = data_2023.drop(columns=['경수(20*20cm2)_개화기', 'drone_yield'])
    data_2024 = data_2024.drop(columns=['LAI_수확기','간장(cm)_수확기', '수장(cm)_수확기','일수립수_수확기', 'SPAD_수확기', '수량(g/(50*50)cm2)_수확기'])

    # diff_values = set(data_2024.columns).symmetric_difference(set(data_2023.columns))
    # print(diff_values)

    df = pd.concat([data_2023, data_2024])

    # drop_cvi = [col for col in df.columns if not 'CVI' in col]
    # df = df[drop_cvi]
    df = df.drop(columns=['반복', '조사지'])
    df.to_csv("./output/data.csv", index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()