import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
def get_data(data_dir, station_name, start_date, end_date):
    station_dir = os.path.join(data_dir, station_name)

    data_list = [pd.read_csv(os.path.join(station_dir, x)) for x in os.listdir(station_dir)]

    df = pd.concat(data_list, axis=0)
    df['tm'] = pd.to_datetime(df['tm'])
    df = df[['tm', 'avgTa', 'maxTa', 'minTa','sumRn']]
    df = df[(df['tm'] >= start_date) & (df['tm'] <= end_date)]
    df = df.reset_index(drop=True)
    df = df.reset_index()
    df['index'] = df['index'] + 1
    df = df.rename(columns={'index': 'DAS'})
    df['sumRn'] = df['sumRn'].fillna(0)
    print(df[df['sumRn'] > 10]['tm'].count(),
          df[df['sumRn'] > 20]['tm'].count(),
          df[df['sumRn'] > 30]['tm'].count(),
          df[df['sumRn'] > 40]['tm'].count())

    return df


def main():
    data_dir = '../input'

    # 익산 = 2022년 11월 4일 ~ 2023년 6월 15일, 부안 = 2023년 10월 29일 ~ 2024년 6월 7일
    df_iksan = get_data(data_dir, '익산', '2022-11-04', '2023-06-15')
    df_iksan['year'] = 2023
    df_buan = get_data(data_dir, '부안', '2023-10-29', '2024-06-07')
    df_buan['year'] = 2024
    df = pd.concat([df_iksan, df_buan], axis=0)

    stats = df.groupby('year').agg({'avgTa': 'mean', 'sumRn': ['sum', 'count']})
    print(stats)

    # fig, ax1 = plt.subplots(figsize=(7, 5))
    #
    # # 색상 설정
    # colors = {2023: "red", 2024: "orange"}
    #
    # # X축 범위 설정용 데이터
    # x_min, x_max = df["DAS"].min(), df["DAS"].max()
    #
    # # 온도 라인 플롯
    # for year, group in df.groupby("year"):
    #     ax1.plot(group["DAS"], group["avgTa"], label=f"Temperature ({year})", color=colors[year])
    #
    # ax1.set_xlabel("DAS")
    # ax1.set_ylabel("Average Temperature (°C)", color="black")
    # ax1.tick_params(axis="y", labelcolor="black")
    # ax1.set_xlim(x_min, x_max)  # X축 범위 설정
    #
    # # 강수량 바 차트를 온도 라인 위로 표시
    # ax2 = ax1.twinx()
    # for year, group in df.groupby("year"):
    #     ax2.bar(group["DAS"] - 0.2 if year == 2023 else group["DAS"] + 0.2,  # 막대 위치 조정
    #             group["sumRn"], width=0.4, label=f"Rainfall ({year})", color=colors[year], alpha=0.5, zorder=5)
    #
    # ax2.set_ylabel("Rainfall (mm)", color="black")
    # ax2.tick_params(axis="y", labelcolor="black")
    #
    # plt.title("Comparison of Average Temperature and Rainfall (2023 vs 2024)")
    # plt.grid(axis="x", linestyle="--", alpha=0.7)
    # plt.tight_layout()
    # plt.show()
    fig, ax1 = plt.subplots(figsize=(7, 5))

    # 색상 설정
    line_color = "red"  # 모든 연도의 라인 색상
    rainfall_colors = {2023: "lightcoral", 2024: "darkred"}  # 강수량 색상 설정

    # X축 범위 설정용 데이터
    x_min, x_max = df["DAS"].min(), df["DAS"].max()

    # 온도 라인 플롯
    for year, group in df.groupby("year"):
        linestyle = "--" if year == 2023 else "-"  # 2023: 점선, 2024: 실선
        ax1.plot(
            group["DAS"],
            group["avgTa"],
            label=f"Temperature ({year})",
            color=line_color,
            linestyle=linestyle,
            linewidth=1
        )

    ax1.set_xlabel("DAS")
    ax1.set_ylabel("Average Temperature (°C)", color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.set_xlim(x_min, x_max)  # X축 범위 설정

    # 강수량 바 차트를 온도 라인 위로 표시
    ax2 = ax1.twinx()
    bar_width = 0.6  # 막대 너비 조정
    for year, group in df.groupby("year"):
        bar_position = group["DAS"] - 0.3 if year == 2023 else group["DAS"] + 0.3  # 막대 위치 조정
        ax2.bar(
            bar_position,
            group["sumRn"],
            width=bar_width,
            label=f"Rainfall ({year})",
            color=rainfall_colors[year],
            alpha=0.6,
            zorder=5
        )

    ax2.set_ylabel("Rainfall (mm)", color="black")
    ax2.tick_params(axis="y", labelcolor="black")

    plt.title("Comparison of Average Temperature and Rainfall (2023 vs 2024)")
    # fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2)# 범례 상단에 가로로 표시

    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()