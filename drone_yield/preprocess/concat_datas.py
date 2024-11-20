import pandas as pd

def main():
    df1 = pd.read_csv('../output/2023_growth.csv')
    df2 = pd.read_csv('../output/2024_growth.csv')
    df2 = df2.drop(columns=['경수(1m2)'])
    df = pd.concat([df1, df2], axis=0)
    df.loc[df['생육단계'] == '수확', '생육단계'] = '수확기'
    print(df['생육단계'].unique())
    df.to_csv('../output/2324_growth.csv', index=False, encoding='utf-8-sig')



if __name__ == '__main__':
    main()