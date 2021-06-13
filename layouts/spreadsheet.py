#Author : Shaikh Aquib
#Date : June 2021

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

    add_rows(data:list)
        adds data to the spreadsheet.
    """
    def __init__(self, master=None):
        """
        Parameters
        ----------
        master : tkinter.Tk, optional
            root widget where spreadsheet will be displayed
        """
        super().__init__(master)

        # Set theme for spreadsheet
        self.style = ttk.Style(master)
        self.theme = 'clam'
        self.style.theme_use(self.theme)

        self.verscrlbar = ttk.Scrollbar(master, 
                           orient ="vertical", 
                           command = self.yview)
        self.verscrlbar.pack(side ='right', fill ='y')

        self.horscrlbar = ttk.Scrollbar(master, 
                           orient ="horizontal", 
                           command = self.xview)
        self.horscrlbar.pack(side ='bottom', fill ='x')

        self.configure(
            yscrollcommand = self.verscrlbar.set,
            xscrollcommand = self.horscrlbar.set
        )


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
            self.column(columns[i], width=300, minwidth=100, anchor=tk.CENTER)
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


    def clear_sheet(self):
        """Clears up everything on the sheet."""
        for item in self.get_children():
            self.delete(item)


    def insert_column(self, column_name:str):
        """Inserts a column into spreadsheet.

        Parameters
        ----------
        column_name : str
            Name of the column to be added.
        """
        new_column_list = []
        for i in range(0, len(self['columns'])):
            new_column_list.append(self['columns'][i])
        new_column_list.append(column_name)
        new_column_tup = tuple(new_column_list)

        # Update the column names
        self.set_columns(new_column_tup)

        return new_column_tup


    def delete_column(self, column_name:str):
        """Deletes a column from spreadsheet.

        Parameters
        ----------
        column_name : str
            Name of the column to be deleted.
        """
        new_column_list = []
        for i in range(0, len(self['columns'])):
            if self['columns'][i] != column_name:
                new_column_list.append(self['columns'][i])
        new_column_tup = tuple(new_column_list)

        # Update the column names
        self.set_columns(new_column_tup)

        return new_column_tup