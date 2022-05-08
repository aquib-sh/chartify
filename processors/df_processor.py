import sys

sys.path.append("../")
import pandas
import numpy
from chartify.processors.processor import DataProcessor


class DataFrameProcessor(DataProcessor):
    """DataFrameProcessor

    Used as a template for processing dataframe
    from various file formats to be inherited form it.
    Parent Class : DataProcessor.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = pandas.DataFrame()

    def get_columns(self) -> tuple:
        keys = self.df.keys()
        return tuple(keys)

    def get_data(self) -> list:
        data = []
        for i in range(0, len(self.df)):
            row = self.df.iloc[i]
            data.append(tuple(row))
        return data

    def is_column_present(self, _key) -> bool:
        """Check if column is present in DataFrame"""
        if _key in self.df:
            return True
        return False

    def get_column_series(self, _key) -> pandas.core.series.Series:
        return self.df[_key]

    def add_new_column(self, column):
        self.df[column] = numpy.nan

    def delete_column(self, column):
        del self.df[column]
