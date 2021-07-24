#Author : Shaikh Aquib
#Date : June 2021

from datetime import datetime
import sys
import tkinter as tk
from tkinter import Scrollbar, ttk
from tkinter import messagebox
from tkinter.constants import BOTTOM, CENTER, E, LEFT, END, RIGHT, W, Y
sys.path.append('../')
from tkinter import Label, Button, Text


class Application(tk.Tk):
    """A class for main window of the application.

    This class serves as main tkinter window which can contain menus, submenus, charts, etc.

    Methods
    -------

    """
    def __init__(self, title:str, size:tuple):
        """
        Parameters
        ----------
        title : str
            Title of the window

        size : tuple
            Size of window (x:int, y:int) where x is width and y is height.
        """
        super().__init__()
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.title(title)
        self.pack_propagate(0)


    def start(self):
        """Displays the window by starting the mainloop."""
        self.mainloop()

    def exit_window(self):
        self.destroy()



class TopLevelWindow(tk.Toplevel):
    """A class for top level window of the application.

    This class serves as main tkinter window which can contain menus, submenus, charts, etc.

    Methods
    -------
    """
    def __init__(self, title: str, size: tuple):
        """
        Parameters
        ----------
        title : str
            Title of the window

        size : tuple
            Size of window (x:int, y:int) where x is width and y is height.
        """
        super().__init__()
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.title(title)

    def start(self):
        """Displays the window by starting the mainloop."""
        self.mainloop()

    def exit_window(self):
        self.quit()
        self.destroy()



class InsertWindow(TopLevelWindow):
    """Insert window which inserts column and rows to the spreadsheet.

    Parameters
    ----------
    adapter : chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    _key : str
        Key for the return value of textbox.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.

    _type : str
        Type of window (column or row)
    """
    def __init__(self, adapter, _key, title:str, size:tuple, _type:str):
        super(InsertWindow, self).__init__(title=title, size=size)

        # If _type is not column or row then raise exception
        if _type.lower() not in ["column", "row"]:
            raise Exception(f"Invalid Type:\n_type={_type}\nType must be _type=column or _type=row")

        self.adapter = adapter
        self.adapter_key = _key

        label = Label(self, text=f"{_type.capitalize()} Name:")
        self.text_box = ttk.Entry(self)
        self.insert_btn = Button(self, text="Apply", command=self.transfer_value_and_destroy)

        label.pack()
        Label(self, text="").pack() #empty space
        self.text_box.pack()
        Label(self, text="").pack() #empty space
        self.insert_btn.pack()


    def transfer_value_and_destroy(self) -> str:
        """Returns the textbox value."""
        self.adapter.insert(self.adapter_key, self.text_box.get())
        self.exit_window()


class InsertRowWindow(TopLevelWindow):
    """Insert window which inserts rows to the spreadsheet.

    Parameters
    ----------
    adapter : chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    columns : list
        columns of the current dataframe, adapter values will also be returned with these names.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.

    """
    def __init__(self, adapter, columns: list, title: str, size: tuple):
        super(InsertRowWindow, self).__init__(title=title, size=size)

        self.adapter = adapter
        self.columns = columns
        self.register = {}

        r=0 # row index
        for col in self.columns:
            Label(self, text=f"{col} : ").grid(row=r, column=0)
            entry = ttk.Entry(self)
            self.register[col] = entry
            entry.grid(row=r, column=1)
            # Register the entry boxes to retrieve further by col names.
            r += 1

        self.insert_btn = Button(self, text="Apply", command=self.transfer_value_and_destroy)
        self.insert_btn.grid(row=r, column=0, padx=(150, 0), pady=(100, 100))


    def transfer_value_and_destroy(self) -> str:
        """Returns the textbox value."""
        for col in self.columns:
            self.adapter.insert(col, self.register[col].get())
        self.exit_window()




class DeleteWindow(TopLevelWindow):
    """Insert window which inserts column and rows to the spreadsheet.

    Parameters
    ----------
    adapter : chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    _key : str
        Key for the return value of dropdown.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.

    _type : str
        Type of window (column or row)
    """
    def __init__(self, adapter, _key, title:str, size:tuple, _type:str):
        super(DeleteWindow, self).__init__(title=title, size=size)

        # If _type is not column or row then raise exception
        if _type.lower() not in ["column", "row"]:
            raise Exception(f"Invalid Type:\n_type={_type}\nType must be _type=column or _type=row")

        self.adapter = adapter
        self.adapter_key = _key

        self.label = Label(self, text=f"{_type.capitalize()}:")
        self.n = tk.StringVar()
        self.choice = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n)
        self.del_btn = Button(self, text="Delete", command=self.transfer_value_and_destroy)

        # Attach widgets to window using grid layout
        self.label.grid(row=0, column=0)
        self.choice.grid(row=1, column=0)
        self.del_btn.grid(row=2, column=0, padx=(100,100))


    def update_dropdown(self, values):
        self.choice['values'] = values
        self.choice.current(0)


    def transfer_value_and_destroy(self):
        """Returns the textbox value."""
        self.adapter.insert(self.adapter_key, self.choice.get())
        self.exit_window()

    

class CollisionSettings(TopLevelWindow):
    """Allows users to choose the settings/columns for Collision Detection.

    Parameters
    ----------
    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.
    """
    def __init__(self, adapter, title:str, size:tuple):
        super(CollisionSettings, self).__init__(title=title, size=size)
        self.adapter = adapter

        time_start   = Label(self, text="Time Start")
        time_end     = Label(self, text="Time End")
        coll_space   = Label(self, text="Collision Space")
        coll_obj     = Label(self, text="Collision Object")

        time_start.grid(row=1, column=0, padx=(0, 80), pady=10)
        time_end.grid(row=2, column=0, padx=(0, 80), pady=10)
        coll_space.grid(row=3, column=0, padx=(0, 50), pady=10)
        coll_obj.grid(row=4, column=0, padx=(0, 60), pady=10)

        self.n1 = tk.StringVar()
        self.n2 = tk.StringVar()
        self.n3 = tk.StringVar()
        self.n4 = tk.StringVar()

        # ============== Create 4 Dropdowns for choice of 4 points ========================
        self.choice1 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n1)
        self.choice2 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n2)
        self.choice3 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n3)
        self.choice4 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n4)

        self.choice1.grid(row=1, column=1)
        self.choice2.grid(row=2, column=1)
        self.choice3.grid(row=3, column=1)
        self.choice4.grid(row=4, column=1)

        self.dropdowns = (self.choice1, self.choice2, self.choice3, self.choice4)
        self.text_vars = (self.n1, self.n2, self.n3, self.n4)

        build_btn = ttk.Button(self, text="DETECT", command=self.transfer_value_and_destroy)
        Label(self, text="").grid(row=5, column=1)
        Label(self, text="").grid(row=6, column=1)
        build_btn.grid(row=7, column=1, padx=(200, 100))


    def update_dropdown(self, values):
        for i in range(0, len(self.dropdowns)):
            self.dropdowns[i]['values'] = values
            self.dropdowns[i].current(i)


    def transfer_value_and_destroy(self):
        """Returns the textbox value."""
        for i in range(0, len(self.text_vars)):
            val = self.text_vars[i].get()
            _k = f'cd_dropdown_choice{i}'
            self.adapter.insert(_k, val)
        self.exit_window()



class CollisionReport(TopLevelWindow):
    """Displays Collision Report as Text on TopLevelWindow.

    """
    def __init__(self, report:str, title:str, size:tuple):
        super(CollisionReport, self).__init__(title=title, size=size)

        font_tuple = ("Arial", 15)
        self.report = Text(self, yscrollcommand=True, bg="linen", font=font_tuple)
        self.report.insert(END, report)
        self.report.config(state="disabled")
        self.report.pack()



class ColumnSelectionWindow(TopLevelWindow):
    """Insert window which inserts column and rows to the spreadsheet.

    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    dataframe: pandas.DataFrame
        DataFrame used in the functions to display dropdowns.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.
    """
    def __init__(self, adapter, dataframe,  title:str, size:tuple):
        super(ColumnSelectionWindow, self).__init__(title=title, size=size)
        self.adapter = adapter
        self.title   = title
        self.size    = size
        self.df      = dataframe

        col_choice = Label(self, text="Choice of columns")
        type_nos   = Label(self, text="Type of numbers")
 
        axe_y          = Label(self, text="Axe Y (object)")
        axe_z          = Label(self, text="Axe Z (space)")
        axe_x_sp       = Label(self, text="Axe X Start Point")
        axe_x_duration = Label(self, text="Axe X Duration")

        col_choice.grid(row=0, column=1, padx=(100, 30))
        type_nos  .grid(row=0, column=2, padx=(0, 30))
 
        axe_y         .grid(row=1, column=0, padx=(0, 80), pady=10)
        axe_z         .grid(row=2, column=0, padx=(0, 80), pady=10)
        axe_x_sp      .grid(row=3, column=0, padx=(0, 50), pady=10)
        axe_x_duration.grid(row=4, column=0, padx=(0, 60), pady=10)

        self.n1 = tk.StringVar()
        self.n2 = tk.StringVar()
        self.n3 = tk.StringVar()
        self.n4 = tk.StringVar()

        # ============== Create 4 Dropdowns for choice of 4 points ========================
        self.choice1 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n1)
        self.choice2 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n2)
        self.choice3 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n3)
        self.choice4 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n4)

        self.choice1.grid(row=1, column=1)
        self.choice2.grid(row=2, column=1)
        self.choice3.grid(row=3, column=1)
        self.choice4.grid(row=4, column=1)

        # ====================== Create Dropdown for Y-Column =============================
        self.n5 = tk.StringVar()
        # Format of the data choice in dtype_y1 (choose 1 of 3)
        self.dtype_y1 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n5)
        self.dtype_y1['values'] = ('Number',
                                   'Time(yyyy-mm-dd hh:mm:ss)',
                                   'Time(dd/mm/yyyyy hh:mm:ss)',
                                   )
        self.dtype_y1.current(0)

        # ===================== Create Dropdown for Y-Duration =============================
        self.n6 = tk.StringVar()
        # Format of the data choice in dtype_y2 (choose 1 of 4):
        self.dtype_y2 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n6)
        self.dtype_y2['values'] = ('Number',
                                   'Week',
                                   'Day',
                                   'Hour',
                                   'Minute',
                                   'Second',
                                   )
        self.dtype_y2.current(0)

        self.dtype_y1.grid(row=3, column=2)
        self.dtype_y2.grid(row=4, column=2)

        self.dropdowns = (self.choice1, self.choice2, self.choice3, self.choice4)
        self.text_vars = (self.n1, self.n2, self.n3, self.n4)

        build_btn = ttk.Button(self, text="BUILD/APPLY", command=self.transfer_value_and_destroy)
        range_btn = ttk.Button(self, text="SELECT MIN-MAX RANGE", command=self.open_range_window)
        build_btn.grid(row=6, column=0, padx=(100, 0), pady=(150,100))
        range_btn.grid(row=6, column=1, padx=(100, 0), pady=(150,100))


    def open_range_window(self):
        space    = self.n1.get()
        object   = self.n2.get()
        xaxis    = self.n3.get()
        duration = self.n4.get()  

        xaxis_dtype     = self.n5.get()
        duration_dtype  = self.n6.get()

        print(xaxis_dtype)

        range_window = RangeSelectionWindow(self.adapter, 
            dataframe=self.df, 
            title="Range Selection", 
            size=(900, 400), 
            datetime=xaxis_dtype != 'Number')

        range_window.set_min_max(xstart=xaxis, yaxis=object, zaxis=space)
        range_window.start()


    def update_dropdown(self, values):
        for i in range(0, len(self.dropdowns)):
            self.dropdowns[i]['values'] = values
            self.dropdowns[i].current(i)


    def transfer_value_and_destroy(self):
        """Returns the textbox value."""
        space    = self.n1.get()
        _object  = self.n2.get()
        xaxis    = self.n3.get()
        duration = self.n4.get()  

        xaxis_dtype     = self.n5.get()
        duration_dtype  = self.n6.get()

        self.adapter.insert('zaxis', space)
        self.adapter.insert('yaxis', _object)
        self.adapter.insert('xaxis', xaxis)
        self.adapter.insert('duration', duration)
        self.adapter.insert('xaxis_type', xaxis_dtype)
        self.adapter.insert('duration_type', duration_dtype)

        self.exit_window()



class RangeSelectionWindow(TopLevelWindow):
    """Allows users to choose the settings/columns for Collision Detection.

    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    df: pandas.DataFrame
        Pandas DataFrame used for setting min-max.

    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.
    """
    def __init__(self, adapter, dataframe, title:str, size:tuple, datetime=False):
        super(RangeSelectionWindow, self).__init__(title=title, size=size)
        self.adapter = adapter
        self.df = dataframe
        self.isdaterange = datetime

        lbl1_text = 'Y Axis (object):'
        lbl2_text = 'Z Axis (space):'
        lbl3_text = 'X Start Point:'

        Label(self, text="MIN").grid(row=0, column=1)
        Label(self, text="MAX").grid(row=0, column=2)
        Label(self, text=lbl1_text).grid(row=1, column=0, sticky='W')
        Label(self, text=lbl2_text).grid(row=2, column=0, sticky='W')
        Label(self, text=lbl3_text).grid(row=3, column=0, sticky='W')

        self.n1_start = tk.StringVar()
        self.n2_start = tk.StringVar()
        self.n3_start = tk.StringVar()

        self.n1_end = tk.StringVar()
        self.n2_end = tk.StringVar()
        self.n3_end = tk.StringVar()

        # ============================= Create 3 Dropdowns ===============================
        self.choice1_start = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n1_start)
        self.choice2_start = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n2_start)

        if datetime:
            self.choice3_start = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n3_start)
        else:
            self.choice3_start = ttk.Entry(self, width=30)

        self.choice1_end = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n1_end)
        self.choice2_end = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n2_end)
        
        if datetime:
            self.choice3_end = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n3_end)
        else:
            self.choice3_end = ttk.Entry(self, width=30)

        self.choice1_start.grid(row=1, column=1)
        self.choice2_start.grid(row=2, column=1)
        self.choice3_start.grid(row=3, column=1)
        
        self.choice1_end.grid(row=1, column=2)
        self.choice2_end.grid(row=2, column=2)
        self.choice3_end.grid(row=3, column=2)

        build_btn = ttk.Button(self, text="Apply", command=self.transfer_value_and_destroy)
        build_btn.grid(row=4, column=0, padx=(200, 100), pady=(150,100))


    def set_min_max(self, xstart: str, yaxis: str, zaxis: str):
        """Populates Minimum and Maximum dropdowns from the given column names of dataframes.
        
        Parameters
        ----------
        xstart: str
            X Start column name for DataFrame.
        yaxis: str
            Y Axis column name for DataFrame.
        zaxis: str
            Z Start column name for DataFrame.
        """
        self.choice1_start['values'] = self.df[yaxis].sort_values().unique().tolist()
        self.choice1_end['values']   = self.df[yaxis].sort_values(ascending=False).unique().tolist()
        self.choice1_start.current(0)
        self.choice1_end.current(0)

        self.choice2_start['values'] = self.df[zaxis].sort_values().unique().tolist()
        self.choice2_end['values']   = self.df[zaxis].sort_values(ascending=False).unique().tolist()
        self.choice2_start.current(0)
        self.choice2_end.current(0)

        if self.isdaterange:
            self.choice3_start['values'] = self.df[xstart].sort_values().unique().tolist()
            self.choice3_end['values']   = self.df[xstart].sort_values(ascending=False).unique().tolist()
            self.choice3_start.current(0)
            self.choice3_end.current(0)


    def transfer_value_and_destroy(self):
        """Returns the textbox value."""
        self.adapter.insert('range_window_opened', True)
        self.adapter.insert('yaxis_min', self.n1_start.get())
        self.adapter.insert('zaxis_min', self.n2_start.get())
    
        if self.isdaterange:
            self.adapter.insert('xaxis_min', self.n3_start.get())
        else:
            self.adapter.insert('xaxis_min', self.choice3_start.get())

        self.adapter.insert('yaxis_max', self.n1_end.get())
        self.adapter.insert('zaxis_max', self.n2_end.get())
        
        if self.isdaterange:
            self.adapter.insert('xaxis_max', self.n3_end.get())
        else:
            self.adapter.insert('xaxis_max', self.choice3_end.get())

        self.exit_window()



class CutChartSettings(TopLevelWindow):
    """Takes input settings for building CutChart view.
    
    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    dates: tuple
        Dates which will be placed in dropdown.

    title: str (default="Cut Chart Settings")
        Title for window.

    size: tuple (default=(400, 200))
        Size of the window.
    """
    def __init__(self, adapter, dates:tuple, title="Cut Chart Settings", size=(400,200)):
        super(CutChartSettings, self).__init__(title=title, size=size)
        self.adapter = adapter
        self.n1 = tk.StringVar()

        self.date_label = ttk.Label(self, text="Select date")
        self.date_label.grid(row=0, column=0)

        self.choice1 = ttk.Combobox(self, state="readonly", width=27, textvariable=self.n1)
        self.choice1['values'] = dates
        self.choice1.current(0)
        self.choice1.grid(row=1, column=0)

        build_btn = ttk.Button(self, text="BUILD", command=self.transfer_value_and_destroy)
        build_btn.grid(row=0, column=1, padx=(100, 100))

        self.time_label = ttk.Label(self, text="time in hh:mm")
        self.time = ttk.Entry(self)
        self.time_label.grid(row=2, column=0)
        self.time.grid(row=3, column=0)


    def transfer_value_and_destroy(self):
        """Inserts the textbox value into the adapter."""
        self.adapter.insert('cut-chart-setting-date', self.choice1.get())
        self.adapter.insert('cut-chart-setting-time', self.time.get())
        self.exit_window()



class CutChartNumericalSettings(TopLevelWindow):
    """Takes input settings for building CutChart view.
    
    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    title: str (default="Cut Chart Settings")
        Title for window.

    size: tuple (default=(400, 200))
        Size of the window.
    """
    def __init__(self, adapter, title="Cut Chart Settings", size=(400,200)):
        super(CutChartNumericalSettings, self).__init__(title=title, size=size)
        self.adapter = adapter
    
        self.time_label = ttk.Label(self, text="Value to cut the chart at:")
        self.time = ttk.Entry(self)
        self.time_label.grid(row=0, column=0, padx=(50,50))
        self.time.grid(row=1, column=0, padx=(100,100))

        build_btn = ttk.Button(self, text="BUILD", command=self.transfer_value_and_destroy)
        build_btn.grid(row=2, column=0, padx=(100, 100))

    def transfer_value_and_destroy(self):
        """Inserts the textbox value into the adapter."""
        self.adapter.insert('cut-chart-setting-point', self.time.get())
        self.exit_window()



class ChartifyOptions(TopLevelWindow):
    """Takes input settings for building CutChart view.
    
    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    title: str (default="Chartify Options")
        Title for window.

    size: tuple (default=(400, 400))
        Size of the window.

    yaxis: list | tuple
        unique vals in yaxis, to set the bar color window.
    """
    def __init__(self, adapter, yaxis, saved_colors, title="Chartify Options", size=(400,400)):
        super(ChartifyOptions, self).__init__(title=title, size=size)
        self.adapter = adapter
        self.yaxis_vals = yaxis
        self.saved_colors = saved_colors

        ttk.Label(self, text="Table Font:")      .grid(row=0, column=0, sticky='W', pady=(0, 50))
        ttk.Label(self, text="Graph Background:").grid(row=1, column=0, sticky='W', pady=(0, 50))
        ttk.Label(self, text="Table Font Size:") .grid(row=2, column=0, sticky='W', pady=(0, 50))

        #ttk.Label(self, text="Chart label font size:") .grid(row=4, column=0, sticky='W')
        #ttk.Label(self, text="Table Background:")      .grid(row=1, column=0, sticky='W')

        self.n1 = tk.StringVar()
        self.n2 = tk.StringVar()
        self.n3 = tk.StringVar()
        self.n4 = tk.StringVar()
        self.n5 = tk.StringVar()

        self.table_font      = ttk.Combobox(self, state="readonly", textvariable=self.n1)
        self.graph_bg        = ttk.Combobox(self, state="readonly", textvariable=self.n2)
        self.table_fsize     = ttk.Combobox(self, state="readonly", textvariable=self.n3)
        #self.chart_lbl_fsize = ttk.Combobox(self, state="readonly", textvariable=self.n5)
        #self.table_bg        = ttk.Combobox(self, state="readonly", textvariable=self.n2)

        self.table_font      .grid(row=0, column=1, sticky='E', pady=(0,50))
        self.graph_bg        .grid(row=1, column=1, sticky='E', pady=(0,50))
        self.table_fsize     .grid(row=2, column=1, sticky='E', pady=(0,50))
        #self.chart_lbl_fsize .grid(row=4, column=1, sticky='E')
        #self.table_bg        .grid(row=1, column=1, sticky='E')

        self.graph_bg['values'] = [
            'red',    'black',  'white', 
            'green',  'grey',   'blue', 
            'voilet', 'yellow', 'purple', 
            'pink',   'peru',   'orange'
            ]

        self.table_fsize['values'] = list(i for i in range(10, 30))
        #self.chart_lbl_fsize['values'] = list(i for i in range(10, 20))

        apply_btn = ttk.Button(self, text="Apply", command=self.transfer_value_and_destroy)
        set_bar_colors_btn = ttk.Button(self, text="Set Bar Colors", command=self.open_bar_colors_window)
        close_btn = ttk.Button(self, text="Close", command=self.destroy_window)
        apply_btn.grid(row=5, column=0, padx=(0, 50), pady=(100,0))
        set_bar_colors_btn.grid(row=5, column=1, pady=(100,0))
        close_btn.grid(row=5, column=2, padx=(50, 0), pady=(100,0))
        

    def add_fonts(self, fonts: list):
        self.table_font['values'] = fonts


    def open_bar_colors_window(self):
        bar_settings_window = BarColorSettings(self.adapter, self.yaxis_vals, self.saved_colors)
        bar_settings_window.start()
        

    def transfer_value_and_destroy(self):
        """Inserts the textbox value into the adapter."""
        self.adapter.insert("table-font",            self.table_font.get())
        #self.adapter.insert("table-background" ,     self.table_bg.get())
        self.adapter.insert("graph-background" ,     self.graph_bg.get())
        self.adapter.insert("table-font-size"  ,     self.table_fsize.get())
        #self.adapter.insert("chart-label-font-size", self.chart_lbl_fsize.get())
        self.exit_window()


    def destroy_window(self) -> None:        
        self.adapter.insert("table-font",       None)
        self.adapter.insert("graph-background", None)
        self.adapter.insert("table-font-size",  None)
        self.exit_window()


class BarColorSettings(TopLevelWindow):
    """Sets the color for bars in chart.
    
    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    yaxis: list
        List of Y-Axis columns

    saved_colors: dict
        Dictionary of colors retrieved from database.

    title: str (default="Chartify Options")
        Title for window.

    size: tuple (default=(400, 400))
        Size of the window.

    yaxis: list | tuple
        unique vals in yaxis, to set the bar color window.
    """
    def __init__(self, adapter, yaxis, saved_colors: dict, title="Bar Color Settings", size=(400,400)):
        super(BarColorSettings, self).__init__(title=title, size=size)
        self.adapter = adapter
        self.yaxis_vals: list = yaxis
        self.saved_colors = saved_colors
        self.n_options: int = len(self.yaxis_vals) # total values in yaxis
        self.option_ptrs: list = []

        bars_frame = ttk.Frame(self)
        bars_frame.pack()

        # vscroll = ttk.Scrollbar(bars_frame, orient='vertical')
        # vscroll.grid(row=0, column=2, sticky=E, padx=(100, 0))

        current_row = 0
        colors: list = [
            'red',    'black',  'white', 
            'green',  'grey',   'blue', 
            'violet', 'yellow', 'purple', 
            'pink',   'peru',   'orange'
        ]

        colors += list(self.saved_colors.keys())

        for i in range(0, self.n_options):
            ttk.Label(bars_frame, text=self.yaxis_vals[i]).grid(row=current_row, column=0, pady=(20,0))
            self.option_ptrs.append(tk.StringVar())
            ttk.Combobox(bars_frame, state="readonly", textvariable=self.option_ptrs[i], values=colors).grid(row=current_row, column=1, pady=(20,0))
            current_row += 1

        apply_btn = ttk.Button(self, text="Apply", command=self.transfer_value_and_destroy)
        apply_btn.pack(pady=(20,0))


    def transfer_value_and_destroy(self):
        """Inserts the textbox value into the adapter."""
        for i in range(0, self.n_options):
            self.adapter.insert(self.yaxis_vals[i], self.option_ptrs[i].get())
       
        self.exit_window()



class CustomColorsWindow(TopLevelWindow):
    """Sets the color for bars in chart.
    
    Parameters
    ----------
    adapter: chartify.processors.data_adapter.DataAdapter
        Data Adapter used to exchange values between this window and the main app window.

    title: str (default="Chartify Options")
        Title for window.

    size: tuple (default=(400, 400))
        Size of the window.
    """
    def __init__(self, adapter, title="Define Custom Colors", size=(600,300)):
        super(CustomColorsWindow, self).__init__(title=title, size=size)
        self.adapter = adapter
        ttk.Label(self, text="Title").grid(row=0, column=0)
        
        self.colorname = ttk.Entry(self, width=43)
        self.colorname.grid(row=0, column=1, columnspan=4, padx=(20, 0))
        
        self.red   = ttk.Entry(self, width=10)
        self.green = ttk.Entry(self, width=10)
        self.blue  = ttk.Entry(self, width=10)
        self.alpha = ttk.Entry(self, width=10)

        ttk.Label(self, text="RGBA value").grid(row=1, column=0)
        self.red  .grid(row=1, column=1, padx=(20, 0), sticky=W)
        self.green.grid(row=1, column=2, sticky=W)
        self.blue .grid(row=1, column=3, sticky=W)
        self.alpha.grid(row=1, column=4, sticky=W)

        ttk.Label(self, text="Red")  .grid(row=2, column=1, sticky=W, padx=(20, 0))
        ttk.Label(self, text="Green").grid(row=2, column=2, sticky=W)
        ttk.Label(self, text="Blue") .grid(row=2, column=3, sticky=W)
        ttk.Label(self, text="Alpha").grid(row=2, column=4, sticky=W)

        ttk.Label(self, text="value range = (0-1)\nexample: 0.1, 0.5, 1, 0").grid(row=3, column=0, sticky=W)
    
        add_btn = ttk.Button(self, text="Add", command=self.transfer_value_and_destroy)
        add_btn.grid(row=4, column=0, padx=(100, 0), pady=(100, 0))


    def transfer_value_and_destroy(self):
        """Inserts the textbox value into the adapter."""

        colorname = self.colorname.get()
        red_val = self.red.get()
        green_val = self.green.get()
        blue_val = self.blue.get()
        alpha_val = self.alpha.get()

        li = [colorname, red_val, green_val, blue_val, alpha_val]

        if None in li or '' in li:
            messagebox.showerror("Error", "boxes cannot be left empty.")
        else:
            self.adapter.insert("colorname", colorname)
            self.adapter.insert("red",   float(red_val))
            self.adapter.insert("green", float(green_val))
            self.adapter.insert("blue",  float(blue_val))
            self.adapter.insert("alpha", float(alpha_val))
            self.exit_window()