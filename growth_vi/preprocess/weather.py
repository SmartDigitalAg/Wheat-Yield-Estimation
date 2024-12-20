import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def get_data(data_dir, station_name, start_date, end_date):
    station_dir = os.path.join(data_dir, station_name)

    data_list = [pd.read_csv(os.path.join(station_dir, x)) for x in os.listdir(station_dir)]

    df = pd.concat(data_list, axis=0)
    df['tm'] = pd.to_datetime(df['tm'])
    df = df[['tm', 'avgTa', 'maxTa', 'minTa','sumRn']]
    df = df[(df['tm'] >= pd.to_datetime(start_date)) & (df['tm'] <= pd.to_datetime(end_date))]
    df = df.sort_values(by='tm')

    df = df.reset_index(drop=True)
    df = df.reset_index()
    df['index'] = df['index'] + 1
    df = df.rename(columns={'index': 'DAS'})
    df['sumRn'] = df['sumRn'].fillna(0)
    df['주차'] = (df['DAS'] - 1) // 7 + 1

    return df


def main():
    data_dir = '../input'

    # 익산 = 2022년 11월 4일 ~ 2023년 6월 15일, 부안 = 2023년 10월 29일 ~ 2024년 6월 7일
    df_iksan = get_data(data_dir, '익산', '2022-11-04', '2023-06-15')
    df_iksan['year'] = 2023
    df_iksan.to_csv("./2023.csv", index=False, encoding='utf-8-sig')

    df_buan = get_data(data_dir, '부안', '2023-10-29', '2024-06-07')
    df_buan['year'] = 2024
    df_buan.to_csv("./2024.csv", index=False, encoding='utf-8-sig')

    df = pd.concat([df_iksan, df_buan], axis=0)

    df = df.groupby(['year', '주차']).agg({'avgTa': 'mean', 'sumRn': 'sum',}).reset_index()
    print(df)
    # plt.show()
    fig, ax1 = plt.subplots(figsize=(7, 5))

    # 색상 설정
    line_color = "red"  # 모든 연도의 라인 색상
    rainfall_colors = {2023: "cornflowerblue", 2024: "darkslateblue"}  # 강수량 색상 설정

    # X축 범위 설정용 데이터
    x_min, x_max = df["주차"].min(), df["주차"].max()

    # 온도 라인 플롯
    for year, group in df.groupby("year"):
        linestyle = "--" if year == 2023 else "-"  # 2023: 점선, 2024: 실선
        ax1.plot(
            group["주차"],
            group["avgTa"],
            label=f"Temperature ({year})",
            color=line_color,
            linestyle=linestyle,
            linewidth=1
        )

    ax1.set_xlabel("주차")
    ax1.set_ylabel("Average Temperature (°C)", color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.set_xlim(x_min, x_max)  # X축 범위 설정

    # 강수량 바 차트를 온도 라인 위로 표시
    ax2 = ax1.twinx()
    bar_width = 0.4  # 막대 너비 조정
    for year, group in df.groupby("year"):
        bar_position = group["주차"] - 0.3 if year == 2023 else group["주차"] + 0.3  # 막대 위치 조정
        ax2.bar(
            bar_position,
            group["sumRn"],
            width=bar_width,
            label=f"Rainfall ({year})",
            color=rainfall_colors[year],
            alpha=0.8,
            zorder=5
        )

    ax2.set_ylabel("Rainfall (mm)", color="black")
    ax2.tick_params(axis="y", labelcolor="black")

    # y축 범위를 뒤집기
    ax2.set_ylim(ax2.get_ylim()[1], 0)  #
    # fig.subplots_adjust(top=0.8)  # 상단 여백을 충분히 늘림

    # plt.title("", pad=30)  # 제목과 범례 간 간격을 늘림
    fig.legend(loc='upper center', ncol=2)  # 범례를 위로 더 밀어냄


    # 그래프 출력
    plt.show()


if __name__ == '__main__':
    main()