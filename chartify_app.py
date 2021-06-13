import sys
sys.path.append('../')
import asyncio
import threading
import multiprocessing
import tkinter.filedialog as fd
from tkinter.constants import *
from chartify.layouts.window import Application
from chartify.layouts.spreadsheet import Spreadsheet
from chartify.layouts.frame import WindowFrame
from chartify.layouts.insert_window import InsertWindow
from chartify.layouts.delete_window import DeleteWindow
from chartify.layouts.chart_window import ChartWindow
from chartify.processors.csv_processor import CSVProcessor
from chartify.processors.xlsx_processor import XLSXProcessor
from chartify.processors.data_adapter import DataAdapter
from chartify.menus.menubar import MenuBar
from chartify import config


class ChartifyApp(Application):
    """ChartifyApp

    Main window of Chartify App.

    Attributes
    ----------
    processor : NoneType
        Processor is initially null but then will be transformed into XLSXProcessor or CSVProcessor according to need.

    app_menubar : MenuBar
        Menubar of application containing all the menus and submenus.

    sheet_frame : WindowFrame
        Frame of application where spreadsheet is placed.

    sheet : Spreadsheet
        Spreadsheet displaying the data of file.

    curr_file : str
        Path of the currently opened data file.

    Methods
    -------
    open_file()
        Opens up the filedialog and saves the selected filename to the curr_file variable.
    save_file()
        Saves the data to a file specified by the filename chosen from filedialog.
    """
    def __init__(self):
        super().__init__(title=config.title, size=config.window_size)
        self.processor = None
        self.curr_file = None
        self.adapter = DataAdapter()

        self.app_menubar = MenuBar(self)
        self.sheet_frame = WindowFrame(self, width=config.sheetf_width, height=config.sheetf_height)
        self.sheet = Spreadsheet(self.sheet_frame)

        self.sheet_frame.place(width=config.sheetf_width, height=config.sheetf_height,
                               x=config.sheetf_coords[0], y=config.sheetf_coords[1])
        self.sheet.pack(expand=True, fill=BOTH)
        self.config(menu=self.app_menubar)


    def open_file(self):
        """Opens the file and displays the data to spreadsheet after processing."""
        self.curr_file = fd.askopenfilename(title="Select input file",
                                            filetypes=(
                                                ("csv file", "*.csv"),
                                                ("xlsx file", "*.xlsx"),
                                            ))

        extension = self.curr_file.split(".")[-1]

        if extension == "csv":
            self.processor = CSVProcessor(self.curr_file)
        elif extension == "xlsx":
            self.processor = XLSXProcessor(self.curr_file)

        cols = self.processor.get_columns()
        data = self.processor.get_data()

        # Add the data to spreadsheet
        self.sheet.clear_sheet()
        self.sheet.set_columns(cols)
        self.sheet.add_rows(data)


    def __save_file__(self):
        """Saves the spreadsheet data to a file."""
        saved_to = fd.asksaveasfilename(title="Save file",
                             filetypes=(
                                ("csv file", "*.csv"),
                                ("xlsx file", "*.xlsx"),
                            ))
        fileparts = saved_to.split(".")

        if len(fileparts) == 1:
            # NOTE : Send a warning dialog informing that filename is without any extension.
            pass

        extension = fileparts[-1]
        if extension == "csv":
            self.processor.df.to_csv(saved_to, index=False)
        elif extension == "xlsx":
            self.processor.df.to_excel(saved_to, index=False)


    def insert_new_column(self):
        adapter_key = "col_name"
        insert_window = InsertWindow(self.adapter, _key=adapter_key, title="Insert Window",
                                size=config.insert_window_size, _type="column")
        insert_window.start()
        new_col = self.adapter.get(adapter_key).strip()
        self.sheet.insert_column(new_col)
        self.processor.add_new_column(new_col)


    def delete_column(self):
        adapter_key = "column_to_remove"
        delete_window = DeleteWindow(self.adapter, _key=adapter_key, title="Delete Window",
                                     size=config.delete_window_size, _type="column")
        delete_window.update_dropdown(self.processor.get_columns())
        delete_window.start()
        col_to_delete = self.adapter.get(adapter_key).strip()
        self.processor.delete_column(col_to_delete)

        cols = self.processor.get_columns()
        data = self.processor.get_data()

        # Add the updated data to spreadsheet
        self.sheet.clear_sheet()
        self.sheet.set_columns(cols)
        self.sheet.add_rows(data)


    def save_file(self):
        """Threaded version of save_file."""
        t = threading.Thread(target=self.__save_file__)
        t.start()


    def build_chart(self):
        """Opens up Chart Window and builds chart after selecting columns."""
        self.chart_win = ChartWindow(adapter=self.adapter, title="Choice of columns for 3D chart", size=config.build_chart_window_size)
        self.chart_win.update_dropdown(self.processor.get_columns())
        self.chart_win.start()


if __name__ == "__main__":
    app = ChartifyApp()
    app.start()
