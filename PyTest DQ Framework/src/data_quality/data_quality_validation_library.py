import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.
    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df, column_names=None):
        if column_names:
            duplicated_rows = df.duplicated(subset=column_names).sum()
            assert duplicated_rows == 0, f"DataFrame contains {duplicated_rows} duplicate rows based on columns: {column_names}"
        else:
            duplicated_rows = df.duplicated().sum()
            assert duplicated_rows == 0, f"DataFrame contains {duplicated_rows} duplicate rows"

    @staticmethod
    def check_count(df1, df2):
        assert len(df1) == len(df2), f"DataFrames have different counts: {len(df1)} vs {len(df2)}"

    @staticmethod
    def check_data_completeness(df1, df2):
        assert df1.equals(df2), "DataFrames are not equal"

    @staticmethod
    def check_dataset_is_not_empty(df):
        assert not df.empty, "DataFrame is empty"

    @staticmethod
    def check_null_values(df, column_names=None):
        for column in column_names:
            null_count = df[column].isnull().sum()
            assert null_count == 0, f"Column '{column}' contains {null_count} null values"

    @staticmethod
    def check_not_negative(df, column_name):
        negative_count = (df[column_name] < 0).sum()
        assert negative_count == 0, f"Column '{column_name}' contains {negative_count} negative values"

    @staticmethod
    def check_regex_pattern(df, column_name, pattern):
        non_matching_count = df[~df[column_name].astype(str).str.match(pattern)].shape[0]
        assert non_matching_count == 0, f"Column '{column_name}' contains {non_matching_count} values that do not match the pattern: {pattern}"

    @staticmethod
    def check_rounding(df, column_name, decimal_places):
        rounded_values = df[column_name].round(decimal_places)
        non_rounded_count = (df[column_name] != rounded_values).sum()
        assert non_rounded_count == 0, f"Column '{column_name}' contains {non_rounded_count} values that are not rounded to {decimal_places} decimal places"

    @staticmethod
    def check_columns_exist(df, column_names):
        missing_columns = [col for col in column_names if col not in df.columns]
        assert not missing_columns, f"DataFrame is missing columns: {missing_columns}"

