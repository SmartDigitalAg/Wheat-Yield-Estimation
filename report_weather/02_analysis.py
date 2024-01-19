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

def fig_seaborn():
    # 이삭수: '수수(개/m2)' > winter_temp, vegetative_temp
    # 이삭당립수: '결실립수(개)' > spring_temp, flowering_temp/rain
    # 천립중: '1,000립중(g)' > summer_temp/hrad
    df = pd.read_csv(os.path.join(report_weather_dir, '맥류작황보고서_기상요인분석.csv'))
    df = df[(df['수수(개/m2)']!=0) &(df['결실립수(개)']!=0) &(df['1,000립중(g)']!=0)]
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

def reshape_statics(df, cols_lst):
    s_cols = ['mean', 'max', 'min', 'std']
    s_df = df[cols_lst].describe().reset_index()
    s_df = s_df[s_df['index'].isin(s_cols)]
    s_df = s_df.T.reset_index()
    s_df.columns = s_df.iloc[0]
    s_df = s_df.iloc[1:]

    return s_df

def generate_statics():
    filepath = os.path.join(report_weather_dir, '맥류작황보고서_기상요인분석.csv')

    weather_eng_list = ['winter_tavg', 'vegetative_tavg', 'spring_tavg', 'flowering_tavg', 'flowering_rain',
                        'summer_tavg', 'summer_hrad']
    weather_kor_list = ['파종~월동 전 온도', '월동 후 영양생장기 온도', '수잉기 온도', '출수기 및 개화기 온도', '출수기 및 개화기 강수량', '등숙기 온도', '등숙기 일조시간']
    weather_dct = dict(zip(weather_eng_list, weather_kor_list))
    
    # 기상요인 기초 통계
    df = pd.read_csv(filepath)
    weather_s = reshape_statics(df, weather_eng_list)
    weather_s['index'] = weather_s['index'].apply(lambda x: weather_dct[x])

    # 밀 생산요인 기초 통계
    wheat_list = ["수수(개/m2)", "결실립수(개)", "1,000립중(g)", "완전종실중(kg/10a)"]
    wheat_s = reshape_statics(df, wheat_list)

    weather_s.to_csv(os.path.join(report_weather_dir, '기초통계_기상요인.csv'), index=False, encoding='utf-8-sig')
    wheat_s.to_csv(os.path.join(report_weather_dir, '기초통계_밀생산요인.csv'), index=False, encoding='utf-8-sig')
    print(len(df['품종'].unique()))

def main():

    generate_statics()




if __name__ == '__main__':
    main()