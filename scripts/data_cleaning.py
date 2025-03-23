import numpy as np
import pandas as pd

def clean_missing_values(data, fill_value=None, method='mean'):
    """
    Clean missing values in the dataset

    Args:
        data (pd.DataFrame): The input data
        fill_value (any, optional): The value to fill missing entries
        method (str): The imputation method to use ('mean', 'median', 'mode', or 'drop')
    
    """
    if method == 'mean':
        return data.fillna(data.mean())
    elif method == 'median':
        return data.fillna(data.median())
    elif method == 'mode':
        return data.fillna(data.mode().iloc[0])
    elif method == 'drop':
        return data.dropna()
    else:
        return data.fillna(fill_value)

def remove_duplicates(data):
    """
    Remove duplicate rows from the DataFrame.

    Args:
        data (pd.DataFrame): The input data.

    Returns:
        pd.DataFrame: DataFrame without duplicates.
    """
    return data.drop_duplicates()

def remove_outliers(data, column, method='z-score', threshold=3):
    """
    Remove outliers from the specified column.

    Args:
        data (pd.DataFrame): The input data.
        column (str): The column to check for outliers.
        method (str): The method to use ('z-score' or 'IQR').
        threshold (float): The threshold for outlier detection.

    Returns:
        pd.DataFrame: DataFrame without outliers.
    """
    if method == 'z-score':
        z_scores = np.abs((data[column] - data[column].mean()) / data[column].std())
        return data[z_scores < threshold]
    elif method == 'IQR':
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        return data[(data[column] >= (Q1 - 1.5 * IQR)) & (data[column] <= (Q3 + 1.5 * IQR))]
    else:
        raise ValueError("Method must be 'z-score' or 'IQR'.")

def convert_data_types(data, conversions):
    """
    Convert columns to specified data types.

    Args:
        data (pd.DataFrame): The input data.
        conversions (dict): A dictionary mapping column names to data types.

    Returns:
        pd.DataFrame: DataFrame with converted data types.
    """
    for column, dtype in conversions.items():
        data[column] = data[column].astype(dtype)
    return data

def standardize_text(data, column):
    """
    Standardize text data in the specified column.

    Args:
        data (pd.DataFrame): The input data.
        column (str): The column to standardize.

    Returns:
        pd.DataFrame: DataFrame with standardized text.
    """
    data[column] = data[column].str.strip().str.lower()
    return data

def create_features(data):
    """
    Create new features from existing data.

    Args:
        data (pd.DataFrame): The input data.

    Returns:
        pd.DataFrame: DataFrame with new features.
    """
    # Example: Extract year from a date column
    if 'date_column' in data.columns:
        data['year'] = pd.to_datetime(data['date_column']).dt.year
    return data

def encode_categorical(data, columns):
    """
    Encode categorical variables into numerical format.

    Args:
        data (pd.DataFrame): The input data.
        columns (list): List of columns to encode.

    Returns:
        pd.DataFrame: DataFrame with encoded categorical variables.
    """
    return pd.get_dummies(data, columns=columns, drop_first=True)

def normalize_data(data, columns):
    """
    Normalize numerical data in specified columns.

    Args:
        data (pd.DataFrame): The input data.
        columns (list): List of columns to normalize.

    Returns:
        pd.DataFrame: DataFrame with normalized data.
    """
    for column in columns:
        data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
    return data

def group_based_imputation(data, group_column, target_column, method='median'):
    """
    Impute missing values in the target column based on the specified method
    within groups defined by the group column.

    Args:
        data (pd.DataFrame): The input data.
        group_column (str): The column to group by (e.g., 'delivery_person_id').
        target_column (str): The column with missing values to impute (e.g., 'delivery_person_age').
        method (str): The imputation method to use ('median' or 'mode').

    Returns:
        pd.DataFrame: DataFrame with missing values imputed.
    """
    if method not in ['median', 'mode']:
        raise ValueError("Method must be 'median' or 'mode'.")

    # Group by the specified column and calculate the imputation value
    if method == 'median':
        imputation_values = data.groupby(group_column)[target_column].transform('median')
    else:  # method == 'mode'
        imputation_values = data.groupby(group_column)[target_column].transform(lambda x: x.mode()[0] if not x.mode().empty else None)

    # Fill missing values in the target column
    data[target_column] = data[target_column].fillna(imputation_values)

    return data