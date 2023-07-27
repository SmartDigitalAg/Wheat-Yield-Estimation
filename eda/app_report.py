import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns


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

def draw_scatter_plot(report_yield):
    st.title("변수 선택에 따른 산점도")

    df = report_yield
    df = df[~df['지역'].isna()]
    mean = df[df['완전종실중(kg/10a)'] != 0]['완전종실중(kg/10a)'].mean()

    Q1 = df['완전종실중(kg/10a)'].quantile(.25)
    Q2 = df['완전종실중(kg/10a)'].quantile(.5)
    Q3 = df['완전종실중(kg/10a)'].quantile(.75)
    Q4 = df['완전종실중(kg/10a)'].quantile(1)


    df['label'] = df['완전종실중(kg/10a)'].apply(lambda x: 'Q1' if x <= Q1 else('Q2' if x <= Q2 else ('Q3' if x <= Q3 else 'Q4')))

    c_list = [
        '재배조건', '품종', '생체중(g/㎡)', '건물중(g/㎡,%)', '건물중비율(%)',
        '초장(cm)_12월10일', '초장(cm)_2월20일', '초장(cm)_3월20일', '초장(cm)_4월10일',
        '초장(cm)_5월1일', '간장(cm)', '완전종실중(kg/10a)', '설립중(kg/10a)', 'l중(g)',
        '1,000립중(g)', '수장(cm)', '경수(cm)_12월10일', '경수(cm)_2월20일', '경수(cm)_3월20일',
        '경수(cm)_4월10일', '경수(cm)_5월1일', '유효경비율(%)', '수수(개/m2)', '출현기',
        '출현양부(양/부)', '출현일수(일)', '초장(㎝)', '경수(개/㎡)', '주간엽수(매)', '지상부건물중(g/㎡)',
        '토양수분(%)', '병해(0-9)', '충해(0-9)', '기타재해(0-9)', '생육재생기', '초장(cm)',
        '유수장(mm)', '유수분화정도(1-10)', '토양수분(0-15cm)', '토양수분(16-30cm)', '한발해(0-9)',
        '습해(0-9)', '최고분얼기', '최고분얼수(개/㎡)', '도복(0-9)', '출수시', '출수기', '출수전',
        '1수영화수(개)', '간장(cm)', '최고분얼수', '유효경수(개/㎡)', '출수기생체중(g/㎡)',
        '출수기건물중(g/㎡)', '출수기건물중비율(%)', '수수(개/㎡)', '1수립수(개)', '성숙기', '결실률(%)',
        '간중(kg/10a)', '간중종실중비율(%)', '리터중(g)', '천립중(g)', '1수완전립수'
    ]

    op_x = st.selectbox("x",
                 c_list
                 )

    op_y = st.selectbox("y",
                 c_list[::-1]
                 )

    s_list = list(df['지역'].unique())
    s_list.insert(0, '전체')
    op_station = st.selectbox("지역",
                 s_list
    )

    if op_station != '전체':
        df_select = df[df['지역'] == op_station]
    else:
        df_select = df

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)

    df1 = df_select[df_select['label'] == 'Q1']
    df2 = df_select[df_select['label'] == 'Q2']
    df3 = df_select[df_select['label'] == 'Q3']
    df4 = df_select[df_select['label'] == 'Q4']

    df1.plot.scatter(x=op_x, y=op_y, s=120, c="gold", alpha=0.6, ax=ax, label='Q1')
    df2.plot.scatter(x=op_x, y=op_y, s=120, c="dodgerblue", alpha=0.6, ax=ax, label='Q2')
    df3.plot.scatter(x=op_x, y=op_y, s=120, c="green", alpha=0.6, ax=ax, label='Q3')
    df4.plot.scatter(x=op_x, y=op_y, s=120, c="tomato", alpha=0.6, ax=ax, label='Q4')
    st.pyplot(fig)


def items_yield(report_yield, report_item):
    st.title("품종별 생산량")
    st.write("1950년경 육성3호가 보급")
    st.write("본격적인 육종사업은 1960년부터 이루어져 영광·장광·진광·진풍 등이 육성")
    st.write("최근 조숙·다수확성 품종으로 조광·내밀·다홍밀·청계밀·그루밀·올밀·수원215호 등의 품종이 보급")

    df = report_yield

    mean = df.groupby('품종').mean()['완전종실중(kg/10a)'].to_frame()
    mean.rename(columns={'완전종실중(kg/10a)': '완전종실중_평균'}, inplace=True)
    merged = pd.merge(mean, df, on='품종', how='inner')

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    select = st.radio(
        "유형 선택",
        ('boxplot', 'bar'))

    if select == 'bar':
        st.bar_chart(mean)
    else:
        fig = plt.figure(figsize=(20, 8))
        ax = sns.boxplot(data=merged, y="완전종실중(kg/10a)", x="품종", orient="v")
        st.pyplot(fig)

    df2 = report_item

    df2['year'] = pd.to_datetime(df2['year'], format='%Y')
    df2 = df2.set_index(df2['year'])
    df2 = df2.drop('year', axis=1)
    df_rate2 = df2.div(df2.sum(axis=1), axis=0)
    df_rate2.reset_index(inplace=True)
    df_rate2 = df_rate2.rename(columns={'index': 'year'})
    st.bar_chart(df_rate2, x='year')

def method_chart(report_method):
    st.title("재배 조건별 생산량")

    df = report_method

    st.bar_chart(df, x='year')


def main():
    # st.set_page_config(layout="wide")
    data_dir = r"C:\code\Wheat-Yield-Estimation\output\report"

    report_yield = pd.read_csv(data_dir + "\맥류작황보고서.csv")
    report_method = pd.read_csv(data_dir + "\맥류작황보고서_재배조건별_생산량.csv")
    report_item = pd.read_csv(data_dir + "\맥류작황보고서_품종별_생산량.csv")

    items = ('변수 산점도', '품종별 생산량', '재배조건별 생산량')

    select = st.sidebar.radio(
        "선택",
        items)

    if select == ('변수 산점도'):
        draw_scatter_plot(report_yield)
    if select == ('품종별 생산량'):
        items_yield(report_yield, report_item)
    if select == ('재배조건별 생산량'):
        method_chart(report_method)


if __name__ == '__main__':
    main()