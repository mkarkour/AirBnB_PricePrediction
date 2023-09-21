from scipy.stats import pearsonr
from geopy.geocoders import Nominatim


# Basic module
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import warnings
warnings.simplefilter('ignore')

sns.set_theme()

# %%%  Initial Functions


def extract_address(lat, lng):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=18&addressdetails=1'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        if 'address' in json_response:
            address_components = json_response['address']
            street = address_components.get('road', '')
            house_number = address_components.get('house_number', '')
            city = address_components.get('city', '')
            country = address_components.get('country', '')
            postcode = json_response['address'].get('postcode', '')
            # print(address_components)

        return (house_number, street, postcode, city, country)


def get_address(lat, lng):
    geolocator = Nominatim(user_agent='my_app')
    location = geolocator.reverse(f'{lat}, {lng}')
    return location.address


def add_address(df):
    df[['house_number', 'street', 'postcode', 'city', 'country']] = df.apply(
        lambda row: extract_address(row['lat'], row['lng']), axis=1, result_type='expand')


def combine_DayWeek(city_name):
    df_weekends = pd.read_csv(
        f'data/{city_name}_weekends.csv', encoding="utf-8").drop(['Unnamed: 0'], axis=1)
    df_days = pd.read_csv(
        f'data/{city_name}_weekdays.csv', encoding="utf-8").drop(['Unnamed: 0'], axis=1)

    df_weekends['week_time'] = 1  # 1 if it's the weekend
    df_days['week_time'] = 0  # 0 otherwise

    # add_address(df_weekends)
    # add_address(df_days)
    df = pd.concat([df_days, df_weekends], ignore_index=True)

    return df


def combine_city(city_name_list):
    df_list = []
    for one_city in city_name_list:
        df_add = combine_DayWeek(one_city)
        df_add['city'] = str(one_city)
        df_list.append(df_add)

    df = pd.concat([i for i in df_list], ignore_index=True)
    return df


def transform_address(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json'}
    response = requests.get(url, params=params)
    result = response.json()
    latitude = float(result[0]['lat'])
    longitude = float(result[0]['lon'])

    return (latitude, longitude)

### Data visualization Function#


def show_dist(df, feature, log=False, multi=False):
    sns.set_theme()
    if multi == False:
        fig, ax = plt.subplots(figsize=(10, 5))
        if log != False:
            ax.set_xscale("log")
        sns.distplot(df[feature], color="red", ax=ax)
        plt.title(
            f"Distribution of the price of a room according to {feature}")
        plt.legend()

    else:
        int_var = (df.dtypes == int)
        float_var = (df.dtypes == float)
        #numeric_col = df.columns[(df.dtypes==np.number)].tolist()
        numeric_col = df.columns[int_var | float_var].tolist()

        num_plots = len(numeric_col)
        num_cols = 3
        num_rows = (num_plots-1) // num_cols + 1

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
        axes = axes.flatten()

        for i, feature in enumerate(numeric_col):
            ax = axes[i]
            sns.distplot(df[feature], ax=ax)
            ax.set_title('{} Distribution'.format(feature), fontsize=20)

        plt.tight_layout()
        plt.show()


def plot_count(df, feature):
    sns.set_theme()
    plt.figure(figsize=(10, 6))
    sns.countplot(x=feature, data=df)
    plt.title(f"{feature}")
    plt.show()


def plot_cat(df, feature, target_feature='realSum'):
    sns.set_theme()
    plt.figure(figsize=(10, 6))
    sns.catplot(x=target_feature, y=feature, data=df,
                kind="bar", ci=None, orient='h')
    plt.xlabel(f"{target_feature}")
    plt.title(f"Proportion of {target_feature} according to {feature}")
    plt.show()


def show_line(df, feature, multi=False):
    sns.set_theme()
    if multi == False:
        rate = df.groupby(feature)['realSum'].mean()
        plt.figure(figsize=(12, 6))
        sns.lineplot(x=rate.index, y=rate.values)
        plt.xlabel(f'{feature}')
        plt.ylabel('Price of the Airbnb room')
        plt.title(f"Evolution of the price according to {feature}")
        plt.show()

    else:
        variables = list(df.drop(columns=['realSum']).columns)
        num_cols = 3
        num_rows = int(np.ceil(len(variables) / num_cols))

        fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, num_rows*5))

        for i, var in enumerate(variables):
            row = i // num_cols
            col = i % num_cols
            ax = axs[row, col] if num_rows > 1 else axs[col]
            rate = df.groupby(var)['realSum'].mean()
            sns.lineplot(x=rate.index, y=rate.values, ax=ax)
            ax.set_xlabel(var)
            ax.set_ylabel('Price of the Airbnb room')
            ax.set_title(f"Evolution of the price according to {var}")

        plt.tight_layout()
        plt.show()


def show_counts(df, interested_var):
    sns.set_theme()
    num_plots = len(interested_var)
    num_cols = 3
    num_rows = (num_plots-1) // num_cols + 1

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
    axes = axes.flatten()

    for i, feature in enumerate(interested_var):
        ax = axes[i]
        sns.countplot(y=feature, data=df, ax=ax)
        ax.set_title('Counting the number of {}'.format(feature), fontsize=10)

        for p in ax.patches:
            count = p.get_width()
            x_pos = p.get_x() + p.get_width() / 2
            y_pos = p.get_y() + p.get_height() / 2
            ax.text(x_pos, y_pos, count, va='center')

    plt.tight_layout()
    plt.show()


def show_hist(df, bool_feature, log=True):
    sns.set_theme()
    fig, ax = plt.subplots(figsize=(10, 5))
    if log == True:
        ax.set_xscale("log")
    plt.title(f"Distribution of the room price according to {bool_feature}")
    plt.legend(labels=[f"{bool_feature} = 1", f"{bool_feature} = 0"])
    sns.histplot(df.loc[(df[bool_feature] == 1), 'realSum'],
                 color="green", stat='count', element="step", ax=ax,  alpha=0.2)
    sns.histplot(df.loc[(df[bool_feature] == 0), 'realSum'],
                 color="red", stat='count', element="step", ax=ax,  alpha=0.2)

    return ax


def plot_join(df, cond_x, cond_y):
    sns.set(style="ticks", color_codes=True)
    join = sns.jointplot(data=df, x=cond_x,
                         y=cond_y,
                         kind="hex", color='#8E44AD',
                         height=8, marginal_ticks=False)
    join.ax_joint.tick_params(labelsize=14, color='red')
    join.ax_joint.legend(fontsize=14)
    plt.show()


def plot_violin(df, feature=None):
    sns.set_theme()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.violinplot(y=feature, data=df, ax=ax)
    return ax


def PlotByCity_Scatter(df, feature):
    sns.set_theme()
    grid = sns.FacetGrid(df, col='city', col_wrap=3, xlim=(
        0, 2500), ylim=(0, 20), height=3.5, aspect=1.25)
    grid.map(sns.scatterplot, "realSum", feature, color='#8E44AD', alpha=.4)
    grid.refline(y=df[feature].median(), alpha=.4)
    grid.set_axis_labels("Price of Listing", f"{feature}")

    def annotate(data, **kws):
        n = len(data)
        corr, p = pearsonr(data['realSum'], data[feature])
        ax = plt.gca()
        ax.text(.7, .3, f"corr = {round(corr,2)}", transform=ax.transAxes)

    grid.map_dataframe(annotate)
    plt.show()


def show_metrics(metric_df, variableX, variableY):
    metric_df['name'] = metric_df.index.tolist()

    fig, axs = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=variableX, y=variableY, data=metric_df, hue='name')
    plt.xlabel(f'{variableX}')
    plt.ylabel(f'{variableY}')
    plt.title(f'{variableX} vs. {variableY} for Different Models')
    plt.show()

# %% Raw data vizualisation


all_city = ["paris", "rome", "london", 'barcelona', "athens",
            "berlin", "lisbon", "budapest", "vienna", "amsterdam"]

df = combine_city(["paris", "rome", "london", 'barcelona', "athens",
                  "berlin", "lisbon", "budapest", "vienna", "amsterdam"])
df.shape


def raw_data_correlation():
    plt.figure(figsize=(20, 10))
    plt.title('Correlation of Attributes', y=1.05, size=19)
    return sns.heatmap(df.corr(), cmap='rocket_r', annot=True, center=True, mask=np.triu(np.ones_like(df.corr(), dtype=bool)))


def plot_raw_total_price():
    plt.figure(figsize=(15, 10))
    ax = plt.subplot()
    plt.axis([0, 8, 0, 1500])
    sns.set_theme(style='ticks', palette='pastel')
    sns.boxplot(x="city", y="realSum", hue="week_time", palette=['#E8E8E8', '#FC814A'],
                data=df, fliersize=0.5, linewidth=1)

    plt.ylabel('Total price of Airbnb listing')
    plt.grid(axis='y', color='#E8E8E8', linestyle='--', linewidth=.5)
    plt.legend(loc=1)
    plt.show()
    plt.clf()
