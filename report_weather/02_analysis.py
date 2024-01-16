import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc


font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
size = 8
params = {'legend.fontsize': size,
          'axes.labelsize': size * 1.5,
          'axes.titlesize': size * 1.2,
          'xtick.labelsize': size,
          'ytick.labelsize': size,
          'axes.titlepad': 12}
plt.rcParams.update(params)


input_dir = '../input'
output_dir = '../output'
report_dir = os.path.join(output_dir, 'report')
weather_dir = os.path.join(output_dir, 'cache_weather')
concated_dir = os.path.join(report_dir, 'concated')
report_weather_dir = os.path.join(output_dir, 'report_weather')

def draw_pairplot(df, title):
    g = sns.pairplot(df, diag_kind='kde')
    g.fig.suptitle(title)
    plt.show()

def draw_boxplot(df):
    sns.boxplot(x='1,000립중(g)', y='품종', data=df)
    plt.show()

def main():
    # 이삭수: '수수(개/m2)' > winter_temp, vegetative_temp
    # 이삭당립수: '결실립수(개)' > spring_temp, flowering_temp/rain
    # 천립중: '1,000립중(g)' > summer_temp/hrad
    df = pd.read_csv(os.path.join(report_weather_dir, '맥류작황보고서_기상요인분석.csv'))
    df = df[(df['수수(개/m2)']!=0) &(df['결실립수(개)']!=0) &(df['1,000립중(g)']!=0) ]
    # df1 = df[['year', '지역', 'winter_tavg', 'vegetative_tavg', '수수(개/m2)']]
    # df2 = df[['year', '지역', 'spring_tavg', 'flowering_tavg', 'flowering_rain', '결실립수(개)']]
    # df3 = df[['year', '지역', 'summer_tavg', 'summer_hrad', '1,000립중(g)']]

    df1 = df[['winter_tavg', 'vegetative_tavg', '수수(개/m2)']]
    df2 = df[['spring_tavg', 'flowering_tavg', 'flowering_rain', '결실립수(개)']]
    df3 = df[['summer_tavg', 'summer_hrad', '1,000립중(g)']]

    # sns.regplot(x='1,000립중(g)', y='summer_tavg', data=df)
    # sns.lmplot(x='1,000립중(g)', y='summer_tavg', data=df, hue='재배조건')

    draw_pairplot(df1, "수수(개/m2)")
    draw_pairplot(df2, "결실립수(개)")
    draw_pairplot(df3, "1,000립중(g)")
    # draw_boxplot(df)



if __name__ == '__main__':
    main()