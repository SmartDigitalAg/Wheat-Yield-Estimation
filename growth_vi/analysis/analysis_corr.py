import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
# rc('font', family='AppleGothic')
# plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='HANDotumExt')
plt.rcParams['axes.unicode_minus'] = False

def main():
    df = pd.read_csv('../output/2324_growth.csv')
    # df = df[df['ID'] <= 10]
    # print(df.columns)
    for stage in df['생육단계'].unique():
        each = df[df['생육단계'] == stage]
        each = each.dropna(axis=1, how='all')
        cols = [col for col in each.columns if 'ID' not in col and '생육단계' not in col and 'date' not in col and '생육단계' not in col]
        corr = each[cols].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title(f'{stage} 생육단계 상관관계')
        plt.show()

    df = df.dropna(axis=1, how='all')
    cols = [col for col in df.columns if
            'ID' not in col and '생육단계' not in col and 'date' not in col and '생육단계' not in col]

    corr = df[cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f'생육단계 상관관계')
    plt.show()



if __name__ == '__main__':
    main()