import pandas as pd
import numpy as np
import seaborn as sns
from raw_data_vizualisation import combine_city, all_city


def data_preparation(df, remove_city=True):
    df = df.drop(columns=["attr_index", "attr_index_norm",
                 "rest_index", "rest_index_norm"])
    df = df.replace([True, False], [1, 0])
    if remove_city == True:
        subset_cat = pd.get_dummies(
            df[df.select_dtypes(include='object').columns.tolist()])
    else:
        subset_cat = pd.get_dummies(df['room_type'])

    subset_cat = subset_cat.rename(columns={
        'room_type_Entire home/apt': 'entire_home_apt',
        'room_type_Private room': 'private_room',
        'room_type_Shared room': 'shared_room'})

    if remove_city == True:
        df = pd.concat([subset_cat, df.drop(
            columns=['city', 'room_type', 'room_private', 'room_shared'])], axis=1)
    else:
        df = pd.concat([subset_cat, df.drop(
            columns=['room_type', 'room_private', 'room_shared'])], axis=1)

    return df


def quartile(df, feature):
    return (pd.DataFrame(np.percentile(df[feature], [0, 25, 50, 75, 100]))).rename(columns={0: f"{feature}_quartile"}, index={0: 'min', 1: '25th', 2: 'median', 3: '75th', 4: 'max'})


def percentile(df, feature):
    return pd.DataFrame(np.percentile(df[feature], np.arange(0, 110, 10))).rename(columns={0: f'{feature}_percentile'}, index={0: 'min', 10: 'max'})


def replace_outlier(df, feature):
    pct_lower = 0.01
    pct_upper = 0.95
    df[feature] = np.clip(df[feature], df[feature].quantile(
        pct_lower), df[feature].quantile(pct_upper))


def remove_outlier(df, feature, condition):
    df = df.loc[df[feature] <= condition]
    return df


sns.set_theme()


def clean_outliers(df):
    df3 = data_preparation(combine_city(all_city), remove_city=False)
    df3 = remove_outlier(df3, 'realSum', 1000)
    return df3


def clean_data(df):
    # only outliers as no duplicate nor missing values after data_preparation
    return clean_outliers(df)
