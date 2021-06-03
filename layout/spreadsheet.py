import tkinter as tk
from tkinter import ttk


class Spreadsheet(ttk.Treeview):
    """A class used for getting data into spreadsheet view.

    This spreadsheet view then can be placed over a tkinter window

    Methods
    -------
    get_available_themes() -> tuple:
        returns current available themes on system.
        
    set_theme(theme_name:str)
        sets the theme for spreadsheet.
        
    set_columns(columns:tuple)
        sets the columns for spreadsheet.

    display()
        displays the spreadsheet on root window.

    add_rows(data:list)
        adds data to the spreadsheet.

    
    """
    
    def __init__(self, master=None):
        """
        Parameters
        ----------
        master : tkinter.Tk, optional
            root window where spreadsheet will be displayed
        """
        
        super().__init__(master)

        # Set theme for spreadsheet
        self.style = ttk.Style(master)
        self.theme = 'winnative'
        self.style.theme_use(self.theme)


    def get_available_themes(self) -> tuple:
        """Returns available theme names on system."""
        return self.style.theme_names()



    def set_theme(self, theme_name:str):
        """Sets theme of spreadsheet.

        Parameters
        ----------
        theme_name : str
            name of the theme to be used.
        """

        available_themes = self.style.theme_names()
        if theme_name in available_themes:
            self.style.theme_use(theme_name)
            


    def set_columns(self, columns:tuple):
        """Sets the columns of spreadsheet.

        Parameters
        ----------
        columns : tuple
            columns of spreadsheet
        """

        self['columns'] = columns
        self['show'] = 'headings'
        for i in range(0, len(columns)):
            self.column(columns[i], width=100, minwidth=100, anchor=tk.CENTER)
            self.heading(columns[i], text=columns[i])
            

    def add_rows(self, rows:list):
        """Adds row data to the spreadsheet.

        Parameters
        ----------
        rows : list[tuple, tuple, tuple...]
            list of tuples containing the data for rows
        """

        for i in range(0, len(rows)):
            self.insert("", 'end', values=rows[i])


    def display(self):
        """Packs the spreadsheet to display it on parent window."""

        self.pack()
