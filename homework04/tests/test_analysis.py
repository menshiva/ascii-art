import os

import numpy as np
import pandas as pd
import pytest
from analysis.homework04 import load_dataset, get_missing_values, \
    substitute_missing_values, \
    get_correlation, get_survived_per_class, get_outliers, create_new_features, \
    determine_survival

data_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def test_loading():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    assert (isinstance(df, pd.DataFrame))
    assert (df.shape == (1309, 10))
    assert (df.index.tolist() == list(range(1309)))
    assert (set(df['Label'].unique().tolist()) == {'Train', 'Test'})
    assert (df.Label.value_counts().Train == 891)


def test_miss_data():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    df_miss = get_missing_values(df)
    miss_mean = df_miss.Total.sum()
    assert (miss_mean == 682)
    assert (df_miss.iloc[0].Total == 418)
    assert (pytest.approx(df_miss.iloc[0].Percent, 0.01) == 31.9328)
    assert (df_miss.iloc[-1].Total == 0)
    assert (pytest.approx(df_miss.iloc[-1].Percent, 0.01) == 0)


def test_substitute_value():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    result = substitute_missing_values(df)
    assert (pytest.approx(result.iloc[17].Age, 0.01) == 29.8811)
    assert (pytest.approx(result.iloc[1043].Fare, 0.01) == 15)


def test_correlation():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    result = get_correlation(df)
    assert (pytest.approx(result, 0.01) == 0.178)


def test_get_survived_per_class():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    survived = get_survived_per_class(df, group_by_column_name="Pclass")
    assert (survived.to_json() ==
            '{"1":0.63,"2":0.47,"3":0.24}')
    survived = get_survived_per_class(df, group_by_column_name="Sex")
    assert (survived.to_json() ==
            '{"female":0.74,"male":0.19}')


def test_outliers():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    n_outliers, outliers = get_outliers(df)
    assert (n_outliers == 171)
    max_fare = outliers.loc[outliers['Fare'].idxmax(), 'Fare']
    assert (pytest.approx(max_fare, 0.01) == 512.3292)


def test_create_new_features():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    df_new_features = create_new_features(df)
    assert (pytest.approx(np.exp(df_new_features.Fare_scaled).mean(),
                          0.01) == 34.5500)
    assert (pytest.approx(df_new_features.Age_log.sum(), 0.01) == 3355.0958)
    assert (df_new_features.Sex.sum() == 466)


def test_determine_survival():
    df = load_dataset(os.path.join(data_dir, 'train.csv'),
                      os.path.join(data_dir, 'test.csv'))
    prob = determine_survival(df, 20, age=33, sex="male")
    assert (pytest.approx(prob, 0.01) == 0.1914)
    prob = determine_survival(df, 20, age=150, sex="male")
    assert np.isnan(prob)
