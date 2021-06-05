import sys
sys.path.append("../")
import pandas
from chartify.processors.df_processor import DataFrameProcessor

class XLSXProcessor(DataFrameProcessor):
    """XLSXProcessor

    Used to process dataframes received from .xlsx(excel) file formats.
    Parent Class : DataFrameProcessor
    """
    def __init__(self, filepath:str):
        super().__init__(filepath)
        self.df = pandas.read_excel(self.filepath)