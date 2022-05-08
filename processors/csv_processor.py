import sys

sys.path.append("../")
import pandas
from chartify.processors.df_processor import DataFrameProcessor


class CSVProcessor(DataFrameProcessor):
    """CSVProcessor

    Used to process dataframes received from .csv file formats.
    Parent Class : DataFrameProcessor
    """

    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.df = pandas.read_csv(self.filepath)
