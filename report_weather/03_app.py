import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns
import os
import plotly.express as px
import plotly.graph_objects as go

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


# report_dir = r'C:\code\Wheat-Yield-Estimation\output\report'
# concated_dir = os.path.join(report_dir, 'concated')


# i_palette = sns.color_palette("husl", 13)
# item_palette = dict(zip([col for col in report_item.columns if col != 'year'], i_palette))
# m_palette = sns.color_palette('Greens')
# method_palette = dict(zip(['답리작', '전작'], m_palette))


def draw_value_scatter(report_all, key):

    weather_eng_list = ['winter_tavg', 'vegetative_tavg', 'spring_tavg', 'flowering_tavg', 'flowering_rain', 'summer_tavg', 'summer_hrad']
    weather_kor_list = ['파종~월동 전 온도', '월동 후 영양생장기 온도', '수잉기 온도', '출수기 및 개화기 온도', '출수기 및 개화기 강수량', '등숙기 온도', '등숙기 일조시간']
    weather_dct = dict(zip(weather_eng_list, weather_kor_list))

    kor_df = report_all.rename(columns=weather_dct)
    kor_df['지역'] = kor_df['지역'].apply(lambda x: x.split('(')[0])


    y_list = ['천립중(g)', '수수(개/㎡)', '결실립수(개)']

    col1, col2 = st.columns(2)
    with col1:
        x = st.selectbox("x", weather_kor_list, key=f'x_{key}')
    with col2:
        y = st.selectbox("y", y_list, key=f'y_{key}')

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    color = st.radio("색깔 선택", ["품종", "재배조건", "지역"], key=f'scatter_color_{key}')


    fig = px.scatter(data_frame=kor_df, x=x, y=y, color=color, opacity=0.5)

    a, b = 1.6, 30


    fig.add_trace(
        go.Scatter(
            # x=[min(kor_df[x]), max(kor_df[x])],
            # y=[min(kor_df[y]), max(kor_df[y])],
            x=[0, max(kor_df[x])],
            y=[b, a*max(kor_df[x]) + b],
            mode='lines', line=dict(color='black')
        )
    )

    fig.update_layout(width=700, height=600)
    fig.update_traces(marker_size=12)
    # fig.update_traces(trendline="ols")

    st.plotly_chart(fig)





def draw_type_boxplot(box_df, sort_median, type_color_map):

    box_df['품종'] = pd.Categorical(box_df['품종'], categories=sort_median, ordered=True)
    box_df = box_df.sort_values(by='품종')

    fig = px.box(box_df, x="품종", y="완전종실중(kg/10a)", color='품종', color_discrete_map=type_color_map)

    st.plotly_chart(fig)

    # fig = px.bar(box_df, x="품종", y="완전종실중(kg/10a)", color='품종', color_discrete_map=type_color_map)
    # st.plotly_chart(fig)


def draw_type_bar(report_item, sort_median, type_color_map):

    report_item['year'] = pd.to_datetime(report_item['year'], format='%Y')
    report_item = report_item.set_index(report_item['year'])
    report_item = report_item.drop('year', axis=1)
    df_rate2 = report_item.div(report_item.sum(axis=1), axis=0)
    df_rate2.reset_index(inplace=True)
    df_rate2 = df_rate2.rename(columns={'index': 'year'})

    df_rate2['year'] = pd.to_datetime(df_rate2['year'], format='%Y')

    # Create a bar chart using Plotly Express
    fig = px.bar(df_rate2, x='year', y=df_rate2.columns[1:],
                 labels={'value': '생산비율', 'variable': '품종'},
                 color_discrete_map=type_color_map, opacity=0.6,
                 barmode = 'stack',
                 category_orders = {'variable': sort_median}
    )

    # Show the plot using Streamlit
    st.plotly_chart(fig)

    # st.bar_chart(df_rate2, x='year')
    # fig = px.bar(df_rate2, x='year', color= [col for col in df_rate2.columns if col != 'year' or col != 'index'], color_discrete_map=type_color_map)
    # st.plotly_chart(fig)



def col_type(report_all, report_item, type_color_map):
    box_df = report_all[['품종', "완전종실중(kg/10a)"]]
    sort_median = box_df.groupby('품종')["완전종실중(kg/10a)"].median().reset_index()
    sort_median = sort_median.sort_values(by='완전종실중(kg/10a)')
    sort_median = sort_median['품종'].unique()

    draw_type_boxplot(box_df,sort_median, type_color_map)
    draw_type_bar(report_item, sort_median, type_color_map)


def select_tab(select_dir, key):
    report_all = pd.read_csv(os.path.join(select_dir, '맥류작황보고서_기상요인.csv'))
    report_item = pd.read_csv(os.path.join(select_dir, '맥류작황보고서_품종별_생산량.csv'))
    report_static = pd.read_csv(os.path.join(select_dir, '기초통계.csv'))
    color_lst = ['deepskyblue', 'palevioletred', 'navy', 'green', 'orchid', 'orange', 'darkgoldenrod',
                 'steelblue', 'blueviolet', 'saddlebrown', 'grey']
    type_color_map = dict(zip([col for col in report_item.columns if col != 'year'], color_lst))
    print(type_color_map)
    type_color_map = {'금강밀': 'deepskyblue', '농림4호': 'palevioletred', '영광': 'navy', '올밀': 'green', '우리밀': 'orchid', '육성3호': 'orange',
     '장광': 'darkgoldenrod', '조경밀': 'steelblue', '조광': 'blueviolet', '조품밀': 'saddlebrown', '백강': 'yellow', '새금강':'black'}

    draw_value_scatter(report_all, key)

    col_type(report_all, report_item, type_color_map)

    st.write(report_static)

    print(key, report_item.columns)

def main():
    st.set_page_config(layout="wide")
    origin_dir = r'C:\code\Wheat-Yield-Estimation\output\report_weather\origin'
    re_dir = r'C:\code\Wheat-Yield-Estimation\output\report_weather\re'


    col1, col2 = st.columns(2)

    with col1:
        st.subheader('원본 데이터')
        select_tab(origin_dir, 'origin')

    with col2:
        st.subheader('재정리 데이터')
        select_tab(re_dir, 're')
# origin Index(['year',  '백강', '새금강',
#        ' '

# re Index(['year',
#        '조],


if __name__ == '__main__':
    main()