import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)



def draw_correlation(df, output_filename):
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(30, 15))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, annot=True, mask=mask, cmap=cmap)
    fig.tight_layout()
    plt.savefig(output_filename)


def main():
    data_filename = '../output/iksan_data_all.csv'
    fig_output_dir = '../output/corr'
    if not os.path.exists(fig_output_dir):
        os.mkdir(fig_output_dir)

    step_names = ['분얼전기', '분얼후기', '개화기', '개화후2주', '개화후4주']
    df = pd.read_csv(data_filename)
    df['종자_생체중_수확'] = df['종자_생체중_수확'] * 25

    for step in step_names:
        drop_columns = df.filter(like=f'생체중_{step}').columns | df.filter(like=f'건물중_{step}').columns
        selected_columns = df.filter(like=f'{step}').columns | df.filter(like='종자_생체중_수확').columns
        df_step  = df[selected_columns]
        df_step =df_step.drop(columns=drop_columns)
        output_filename = os.path.join(fig_output_dir, f'{step}.png')
        draw_correlation(df_step,  output_filename)


if __name__ == '__main__':
    main()
