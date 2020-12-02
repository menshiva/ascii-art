"""
In this homework, we will use well-known Titanic dataset which contains 
information about passengers of Titanic. The dataset consists of personal 
information about each passenger and indicator whether the passenger 
survived. We will use this data to analyse passenger list and their chance for
survival.

The provided dataset contains the following attributes:
 'Age' - age in years,
 'Fare' - fare ticked price,
 'Name' - passenger name,
 'Parch' - # of parents/children of a person on board,
 'PassengerId' - identifier,
 'Pclass' - travelling class, 1 = 1. class, 2 = 2. class, 3 = 3. class,
 'Sex' - sex,
 'SibSp' - # siblings/spouses on board,
 'Survived' - 0 = died, 1 = survived,
 'Embarked' - boarding port C = Cherbourg, Q = Queenstown, S = Southampton,
 'Cabin' - cabin number
 'Ticket' - ticket number
"""

import numpy as np
import pandas as pd


def load_dataset(train_file_path, test_file_path):
    """
    Write a function which loads CSV from two files to pandas DataFrame and
    performs several data processing steps. Use data provided in `data`
    directory for testing ('data/train.csv' as input parameter
    `train_file_path`, and 'data/test.csv'  as `test_file_path`). Add column
    name "Label" to each DataFrame. The column should contain value "Train"
    for data from `train_file_path` and "Test" from test_file_path.
    
    Perform following operations with DataFrames (keep the order of the
    operations):
        1. Concatenate both DataFrames.
        2. Remove columns  "Ticket", "Embarked", "Cabin" from created DataFrame.
        3. Set the index to unique numbers from zero to the number of rows.

    The return value of the function is processed DataFrame.
    """

    train_data = pd.read_csv(train_file_path)
    test_data = pd.read_csv(test_file_path)
    train_data["Label"] = "Train"
    test_data["Label"] = "Test"

    result_data = pd.concat([train_data, test_data], ignore_index=True)
    del result_data["Ticket"]
    del result_data["Embarked"]
    del result_data["Cabin"]

    return result_data


def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    When working and analysing data, one often needs to deal with missing
    values. For example, some passengers did not fill information about
    family members. In that case, one needs to be aware of it as it may
    introduce bias to the data.

    Write a function which determines the number of missing values in given
    DataFrame. The function should output a new DataFrame. The new DataFrame
    should be indexed by columns of original DataFrame. Columns of returned
    DataFrame will be (keep the order of the columns):
        1. "Total" - contains the number of missing values
        2. "Percent" - contains the percentage of missing values with regard to all
        rows of given DataFrame.

    Sort the resulting DataFrame based on the number of missing values from
    largest to smallest.
    
    Example of output:

               |  Total  |  Percent
    "Column1"  |   34    |    76
    "Column2"  |   0     |    0
    """

    total_missing = df.isnull().sum()
    percent_missing = total_missing / len(df) * 100

    result_frame = pd.DataFrame({"Total": total_missing, "Percent": percent_missing})
    return result_frame.sort_values("Total", ascending=False)


def substitute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    One way how to handle missing data is to substitute missing values with
    some statistic of other rows. We will use this method for two columns:
        1. "Age" - fill missing values with the mean of other rows.
        2. "Fare" - fill missing values with the lowest price of ~$15 (we
        suppose that the majority of unregistered tickets were the cheapest
        ones).

    Do not to modify given DataFrame but create a copy of it.
    """

    result_frame = df.copy()
    result_frame["Age"] = result_frame["Age"].fillna(np.nanmean(df["Age"].to_numpy()))
    result_frame["Fare"] = result_frame["Fare"].fillna(15)

    return result_frame


def get_correlation(df: pd.DataFrame) -> float:
    """
    We want to know whether there is a relationship between the age of a
    passenger and fare ticket price (e.g. younger children have cheaper
    tickets). We will use Pearson correlation coefficient to quantify linear
    relationship between columns "Age" and "Fare".
    The result will be returned as one number.

    Pearson correlation coefficient quantifies linear relationship between
    two random variables. Correlation ranges from -1 to 1. Value around zero
    indicates no linear relationship, -1 indicates strong negative
    relationship, 1 indicates strong relationship.
    """

    return df["Age"].corr(df["Fare"])


def get_survived_per_class(df: pd.DataFrame, group_by_column_name: str) -> pd.DataFrame:
    """
    We want to know how big was the chance of survival for different groups of
    passengers (e.g. for different sexes, classes, etc.). Write a function
    that estimates that. The input of the function is a DataFrame with data
    and name of column (group_by_column_name) which holds group information.
    To increase readability of the result sort values from the highest chance of
    survival to lowest and round the resulting values to 2 decimal places.
    Return result as pandas Series.
    
    Example:

    get_survived_per_class(df, "Sex")

                  Survived
    Female     |      0.82
    Male       |      0.32

    """

    unique_values = df[group_by_column_name].unique()
    coefficients = [
        np.nanmean(df[df[group_by_column_name] == value]["Survived"].to_numpy())
        for value in unique_values
    ]

    result_frame = pd.DataFrame({"Survived": coefficients}, unique_values)
    return result_frame.round(2).sort_values("Survived", ascending=False).squeeze()


def get_outliers(df: pd.DataFrame) -> (int, str):
    """
    We want to explore fare ticket prices. An important part of such
    exploration is exploration of outliers. An outlier may indicate an error
    in the data (somebody entered price incorrectly) or some special group of
    passengers.

    We will use the IQR method for the identification of outliers. IQR method
    considers an outlier any point which does not fulfil:
        Q1 - 1.5*IQR < point_value < Q3 + 1.5*IQR,
    where Q1 and Q3 are the first and the third quartiles respectively
    calculated from all points in data. IQR is the inter-quartile range
    calculate as the difference between Q3 and Q1:
        IQR = Q3 - Q1.

    Return tuple with the number of outliers and all passengers with outlier
    fare ticket price.
    """

    q1 = df["Fare"].quantile(0.25)
    q3 = df["Fare"].quantile(0.75)
    iqr = q3 - q1
    mask = df[df["Fare"].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]

    return df.shape[0] - mask.shape[0] - 1, df[~df.isin(mask)].dropna()


def create_new_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    To analyse data and use them for modeling, it may be convenient to create
    a new columns (features). These new features are usually created
    transformation of original values. For example, if we want to compare
    survivals from Titanic and SS Eastland we will want to scale fare prices
    to the same values for each ship as travelling on Titanic was more
    expensive.

    Create 3 new variables:
        1. "Fare_scaled" - scale "Fare" columns to have zero mean and standard
       deviation equal one.
        2. "Age_log" - is natural logarithm of attribute "Age" (differences
        between age of children are magnified in comparison to adults).
        3. "Sex" -  Replace string values with numerical ones, where "male"
        will be replaced with 0 and "female" with 1. The resulting values
        should have type `int`.

    Do not modify original DataFrame.
    """

    result_frame = df.copy()
    result_frame["Fare_scaled"] = (df["Fare"] - df["Fare"].mean()) / df["Fare"].std()
    result_frame["Age_log"] = np.log(df["Age"].to_numpy())
    result_frame["Sex"] = np.where(result_frame["Sex"].to_numpy() == "male", 0, 1)

    return result_frame


def determine_survival(df: pd.DataFrame, n_interval: int, age: float, sex: str) -> float:
    """
    Determine the probability of survival of a person specified by age and sex.

    Missing values in column "Age" replace with mean value. In order to
    moderate significance of the estimated probability, divide "Age" to
    specified number of intervals and calculate probability from given
    interval. For example if we have values in "Age" column [2, 13, 18, 25] and
    we want 2 intervals, result should be:

    0    (1.977, 13.5]
    1     (13.5, 25.0]

    With division based on "Sex", the categorization should be:

       "AgeInterval" | "Sex"       |   "Survival Probability"
       (1.977, 13.5] | "male"      |            0.21
       (1.977, 13.5] | "female"    |            0.28
       (13.5, 25.0]  | "male"      |            0.10
       (13.5, 25.0]  | "female"    |            0.15

    Output of determine_survival(df, n_interval=2, age = 5, sex = "male")
    should be 0.21. If there is no passenger for some group, return numpy
    NA value.
    """

    df_normal = df.copy()
    df_normal["Age"] = df_normal["Age"].fillna(np.nanmean(df["Age"].to_numpy()))
    df_normal["AgeInterval"] = pd.cut(df_normal["Age"], n_interval).to_numpy()

    categorized_frame = df_normal[["AgeInterval", "Sex"]].drop_duplicates(ignore_index=True)
    categorized_frame["SP"] = categorized_frame.apply(lambda row: np.nanmean(
        df_normal[
            (df_normal["Sex"] == row["Sex"])
            & (df_normal["AgeInterval"] == row["AgeInterval"])
        ]["Survived"].to_numpy()
    ), axis=1)

    interval = df_normal.loc[(df_normal["Age"] == age) & (df_normal["Sex"] == sex)]["AgeInterval"]
    if interval.empty:
        return np.NaN
    interval = interval.iloc[0]

    return categorized_frame[
              (categorized_frame["AgeInterval"] == interval)
              & (categorized_frame["Sex"] == sex)
    ]["SP"].item()
