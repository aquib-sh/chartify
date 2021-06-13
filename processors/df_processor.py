import sys
sys.path.append("../")
import pandas
from chartify.processors.processor import DataProcessor

class DataFrameProcessor(DataProcessor):
    """DataFrameProcessor

    Used as a template for processing dataframe
    from various file formats to be inherited form it.
    Parent Class : DataProcessor.
    """
    def __init__(self, filepath:str):
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