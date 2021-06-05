#Author : Shaikh Aquib
#Date : June 2021

class DataProcessor:
    """ DataProcessor

    Used for processing data so it can be easily attached to
    spreadsheet. This is a template which will be used by inherited
    dataframe processors.

    Methods
    -------
    get_data_columns() -> tuple
        returns data column names
    
    get_data() -> list
        returns all the data from each column of data

    """ 
    def __init__ (self, filepath:str):
        """
        Parameters
        ----------
        filepath : str
            path to the file containing data, path can be relative or absolute.
        """
        pass

    def get_columns(self) -> tuple:
        """
        Return
        ------
        tuple containing column names of the data.
        """
        pass

    def get_data(self) -> list:
        """
        Return
        ------
        list[tuple, tuple, tuple...] containing all the data from each column of data.
        """
        pass

