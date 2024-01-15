import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import altair as alt
from datetime import datetime as dt, datetime
import seaborn as sns
import os

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

def draw_scatter_plot(df):
    st.subheader\
        ("변수 선택에 따른 산점도")

    df = df[~df['lo2'].isna()]
    # mean = df[df['item'] != 0]['item'].mean()
    # df['item'] = df['value'].astype()
    Q1 = df['value'].quantile(.25)
    Q2 = df['value'].quantile(.5)
    Q3 = df['value'].quantile(.75)
    Q4 = df['value'].quantile(1)


    df['label'] = df['value'].apply(lambda x: 'Q1' if x <= Q1 else('Q2' if x <= Q2 else ('Q3' if x <= Q3 else 'Q4')))

    c_list = df.filter(regex='sunshine|rainfall|humid|wind|tmax|tmin|tavg|value').columns.to_list()

    op_x = st.selectbox("x",
                 c_list[::-1]
                 )

    op_y = st.selectbox("y",
                 c_list
                 )

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

def main():
    data_dir = "C:\code\Wheat-Yield-Estimation\output\kosis_report\model_input"
    df = pd.read_csv(os.path.join(data_dir, "통계청_전국_기상.csv"))
    draw_scatter_plot(df)

if __name__ == '__main__':
    main()