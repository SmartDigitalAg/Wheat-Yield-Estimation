import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


from matplotlib import font_manager, rc

import platform
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

if platform.system() == "Windows":
    font_path = "C:/Windows/Fonts/NGULIM.TTF"  # 원하는 폰트 경로
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)
elif platform.system() == "Darwin":
    rc('font', family='AppleGothic')

def main():
    # 데이터 로드 및 전처리
    data = pd.read_csv("./output/data.csv")
    df = data
    df['조사지'] = df['조사지'] + '_' + df['year'].astype(str)

    apsim_data = pd.read_csv("./input/apsim_data_new_long.csv")
    apsim_data['조사지'] = apsim_data['조사지'] + '_' + apsim_data['year'].astype(str)

    plt.figure(figsize=(12, 8))
    sns.boxplot(
        x='조사지',
        y='수량(g/m2)_수확기',
        hue='year',
        data=df,
        palette="coolwarm"
    )

    for index, row in apsim_data.iterrows():
        plt.scatter(
            row['조사지'],
            row['yield_apsim'],
            color='red',
            zorder=10,
            label='Simulated Yield' if index == 0 else ""
        )

    plt.title("Box Plot", fontsize=16)
    plt.xlabel("Plot (Year)", fontsize=14)
    plt.ylabel("수확량 (g/m2)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)

    # 범례 표시
    plt.legend(title="Year", fontsize=10)

    # 출력
    plt.show()


if __name__ == '__main__':
    main()