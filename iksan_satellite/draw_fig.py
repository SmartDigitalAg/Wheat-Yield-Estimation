import os
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
import platform

import warnings

warnings.filterwarnings("ignore", category=UserWarning)


if platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')

def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

output_dir = make_dir('./output')
fig_dir = make_dir(os.path.join(output_dir, 'fig'))

# satellite_colors = {'drone': 'green', 'sentinel_raw': 'blue', 'landsat8': 'red', 'landsat9': 'orange', 'sentinel_cloud_pre':'purple'}
satellite_colors = {'drone': 'green', 'sentinel2': 'blue', 'landsat8': 'red', 'landsat9': 'orange', 'sentinel_cloud_pre':'purple'}

def preprocess_df(drone_filename, satellite_filename, output_df_filename):
    df_drone = pd.read_csv(drone_filename)
    # df_drone[df_drone.filter(like='RVI').columns] /= 10
    df_drone[df_drone.filter(like='CVI').columns] *= 10
    df_satellite = pd.read_csv(satellite_filename)
    # df_satellite[df_satellite.filter(like='RVI').columns] /= 10
    df_satellite[df_satellite.filter(like='CVI').columns] /= 10
    df = pd.concat([df_drone, df_satellite])
    df[df.filter(like='RVI').columns] /= 10

    df_plot_avg = df[df['Site'].str.contains('seed')].drop(columns=['Site'])
    df_plot_avg = df_plot_avg.groupby(['Step', 'Satellite', 'Date']).mean().reset_index()
    df_plot_avg['Site'] = 'all'

    df = df[~df['Site'].str.contains('seed')]
    df = pd.concat([df, df_plot_avg])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # df.to_csv(output_df_filename, index=False, encoding='utf-8-sig')

    return df

def draw_date_plot(df_dct, output_filename):


    # date_dct = {'230130': '분얼전','230321':'분얼전기', '230417':'분얼후기', '230501':'개화기', '230520':'개화2주후', '230601':'개화4주후',  '230615':'수확'}
    # df.loc[:,'Step'] = pd.Categorical(df['Step'], categories=list(date_dct.values()), ordered=True)

    nrows, ncols = 1, 2
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 5))
    axes = axes.flatten()

    for i, (check_point, df) in enumerate(df_dct.items()):

        df = df[df['Site'] == 'all']
        ax = axes[i]
        ax = sns.lineplot(x="Step", y='Date', hue="Satellite",
                          palette=satellite_colors, marker="o", data=df, ax=ax)
        ax.legend(loc='upper left')
        ax.set_xlabel('Step', size=12)
        ax.set_ylabel('Date', size=12)
        ax.set_title(f'{check_point}', size=15, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    fig.suptitle('Date comparison', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, output_filename))


def draw_tendency_line(df, vi_lst, output_filename):
    df = df[df['Site'] == 'all']

    # nrows, ncols = 2, 3
    nrows, ncols = 1, 5

    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 5))

    handles, labels = [], []

    for i, vi in enumerate(vi_lst):
        # row, col = divmod(i, ncols)  # Calculate row and column index
        # ax = axes[row, col]
        ax = axes[i]
        ax = sns.lineplot(ax=ax, x="Step", y=vi, hue="Satellite",
                          palette=satellite_colors,
                          marker="o",
                          data=df)

        ax.tick_params(axis='x', labelsize=10, rotation=45)
        ax.set_xlabel('Step', size=12)
        ax.set_ylabel(vi, size=12)
        ax.set_title(f'{vi}', size=15)

        if i == 0:
            handles, labels = ax.get_legend_handles_labels()

        ax.legend_.remove()

    # num_plots = len(vi_lst)
    # total_plots = 3 * 2
    # if num_plots < total_plots:
    #     for i in range(num_plots, total_plots):
    #         fig.delaxes(axes.flat[i])

    fig.legend(handles, labels, loc='upper right', fontsize=10)
    fig.suptitle('Tendency of UAV and Satellite Values', fontsize=20, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, output_filename))


def draw_plot_comparison(df, vi_lst, output_filename):
    df = df[df['Site'].str.contains('plot')]
    df_melt = pd.melt(df, id_vars=['Step', 'Satellite', 'Site'], value_vars=vi_lst, var_name='Index', value_name='Value')
    to_plot = df_melt.pivot_table(index=['Step', 'Index', 'Site'], columns='Satellite', values='Value').reset_index()

    # nrows, ncols = 2, 3
    nrows, ncols = 1, 5
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 5))

    axes = axes.flatten()
    handles, labels = [], []

    for i, vi in enumerate(vi_lst):
        subset = to_plot[to_plot['Index'] == vi]
        ax = axes[i]

        g = sns.regplot(x='drone', y='drone', data=subset, scatter=False, label='drone', ci=None, ax=ax, color=satellite_colors['drone'])

        for satellite in df['Satellite'].unique():
            if satellite != 'drone':
                # 점
                # sns.scatterplot(x=subset['drone'], y=subset[satellite], ax=ax, color=satellite_colors[satellite],
                #                 label=satellite)
                # 점 + 회귀선
                sns.regplot(x=subset['drone'], y=subset[satellite], label=satellite, scatter=True, color=satellite_colors[satellite], ax=ax)
        # ylim = ax.get_ylim()
        # ax.set_xlim(ylim)
        # xlim = ax.get_xlim()
        # ax.set_ylim(xlim)
        ax.set_xlabel(f'{vi}$_{{uav}}$', size=12)
        ax.set_ylabel(f'{vi}$_{{sat}}$', size=12)
        ax.set_title(f'{vi}', size=15)
        ax.legend(loc='upper left')

        if i == 0:
            handles, labels = ax.get_legend_handles_labels()

        ax.legend_.remove()

    # num_plots = len(vi_lst)
    # total_plots = 3 * 2
    # if num_plots < total_plots:
    #     for i in range(num_plots, total_plots):
    #         fig.delaxes(axes.flat[i])
    fig.legend(handles, labels, loc='upper right', fontsize=10)
    fig.suptitle('Comparison of UAV and Satellite Values', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, output_filename))

def linear_text(x, y):
    correlation, p_value = pearsonr(x, y)
    # p_value = round(p_value, 2)

    x_fit = x.values.reshape(-1, 1)  # x를 2차원 배열로 변환

    model = LinearRegression()
    model.fit(x_fit, y)
    y_pred = model.predict(x_fit)

    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = r2_score(y, y_pred)

    # if intercept < 0:
    #     return (f'cor:{correlation:.2f}, p:{p_value:.4f}\n'
    #             f'R²: {r_squared:.2f}\n'
    #             f'y = {slope:.2f} * x - {-intercept:.2f}')
    # else:
    #     return (f'correlation:{correlation:.2f}, p:{p_value:.4f}\n'
    #             f'R²: {r_squared:.2f}'
    #             f'\ny = {slope:.2f} * x + {intercept:.2f}')
    return f'correlation:{correlation:.2f}\nR²: {r_squared:.2f}'

def each_scatter_plot(df, vi_lst, output_filename):
    df = df[df['Site'].str.contains('plot')]
    df_melt = pd.melt(df, id_vars=['Step', 'Satellite', 'Site'], value_vars=vi_lst, var_name='Index',
                      value_name='Value')
    to_plot = df_melt.pivot_table(index=['Step', 'Index', 'Site'], columns='Satellite', values='Value').reset_index()
    nrows, ncols = 3, 5
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 3, nrows * 3))

    axes = axes.flatten()

    handles, labels = [], []

    plot_index = 0
    for i, satellite in enumerate(df['Satellite'].unique()):

        if satellite == 'drone':
            continue
        for j, vi in enumerate(vi_lst):
            if plot_index < len(axes):
                ax = axes[plot_index]
                subset = to_plot[to_plot['Index'] == vi]
                g = sns.regplot(x='drone', y='drone', data=subset, scatter=False, label='drone', ci=None, ax=ax,
                                color=satellite_colors['drone'])
                x = subset['drone']
                y = subset[satellite]
                # x = subset[satellite]
                # y = subset['drone']
                sns.regplot(x=x, y=y, label=satellite, scatter=True,
                            color=satellite_colors[satellite], ax=ax, scatter_kws={'alpha': 0.3})

                ax.text(0.05, 0.75, linear_text(x, y), transform=ax.transAxes)
                ax.set_xlabel(f'', size=12)
                ax.set_ylabel(f'{vi}$_{{sat}}$', size=12)

                if plot_index > 9:
                    ax.set_xlabel(f'{vi}$_{{uav}}$', size=12)
                # ax.set_ylabel(f'{vi}$_{{uav}}$', size=12)
                #
                # if plot_index > 9:
                #     ax.set_xlabel(f'{vi}$_{{sat}}$', size=12)

                if j == 0:
                    handles.append(ax.collections[0])
                    labels.append(satellite)
                plot_index += 1
    fig.legend(handles, labels, loc='upper right', fontsize=10)

    fig.suptitle('Comparison of UAV and Satellite Values', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, output_filename))


def draw_boxplot(df, vi_lst, output_filename):
    df = df[df['Site'].str.contains('plot')]

    # nrows, ncols = 2, 3
    nrows, ncols = 1, 5

    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 5))
    axes = axes.flatten()

    handles, labels = [], []

    for i, vi in enumerate(vi_lst):
        ax = axes[i]
        ax = sns.boxplot(ax=ax, x="Satellite", y=vi, hue="Satellite",
                         palette=satellite_colors, data=df,
                         boxprops=dict(alpha=.7), legend=False)

        ax.tick_params(axis='x', labelsize=10, rotation=45)
        ax.set_xlabel('Satellite', size=12)
        ax.set_ylabel(vi, size=12)
        ax.set_title(f'{vi}', size=15)

        if i == 0:
            handles, labels = ax.get_legend_handles_labels()

        # ax.legend_.remove()
    # num_plots = len(vi_lst)
    # total_plots = 3 * 2
    # if num_plots < total_plots:
    #     for i in range(num_plots, total_plots):
    #         fig.delaxes(axes.flat[i])
    fig.legend(handles, labels, loc='upper right', fontsize=10)
    fig.suptitle('Comparison of UAV and Satellite Values', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, output_filename))

def save_each_fig(df, vi_lst, check_point):
    operations = [
        # (draw_date_plot, f'date_{check_point}.png'),
        (draw_tendency_line, f'tendency_{check_point}.png'),
        (draw_plot_comparison, f'comparison_{check_point}.png'),
        (each_scatter_plot, f'scatter_{check_point}.png'),
        (draw_boxplot, f'boxplot_{check_point}.png')
    ]
    for func, filename_pattern in operations:
        output_filename = filename_pattern.format(check_point=check_point)
        # if func == draw_date_plot:
        #     func(df, output_filename)
        # else:
        func(df, vi_lst, output_filename)



def main():
    vi_lst = ['NDVI', 'CVI', 'NDRE', 'GNDVI', 'RVI']

    drone_filename = os.path.join(output_dir, 'drone.csv')

    # cloud: resamping과 cloud filtering을 거친 satellite 데이터
    # resampled: resampling만 거친 satellite 데이터
    check_point_lst = ['cloud', 'resampled']
    df_dct = {}
    for check_point in check_point_lst:
        satellite_filename = os.path.join(output_dir, f'satellite_{check_point}.csv')
        output_df_filename = os.path.join(output_dir, f'all_{check_point}.csv')

        df = preprocess_df(drone_filename, satellite_filename, output_df_filename)

        save_each_fig(df, vi_lst, check_point)
        df_dct[check_point] = df

    draw_date_plot(df_dct, 'date_plot.png')

if __name__ == '__main__':
    main()