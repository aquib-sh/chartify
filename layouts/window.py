#Author : Shaikh Aquib
#Date : June 2021

import sys
import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTTOM, CENTER, LEFT, END
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
        self.text_box = Text(self, height=1, width=20)
        self.insert_btn = Button(self, text="Insert", command=self.transfer_value_and_destroy)

        label.pack()
        Label(self, text="").pack() #empty space
        self.text_box.pack()
        Label(self, text="").pack() #empty space
        self.insert_btn.pack()


    def transfer_value_and_destroy(self) -> str:
        """Returns the textbox value."""
        self.adapter.insert(self.adapter_key, self.text_box.get(1.0, END))
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



class ChartWindow(TopLevelWindow):
    """Insert window which inserts column and rows to the spreadsheet.

    Parameters
    ----------
    title : str
        Title of the window

    size : tuple
        Size of window (x:int, y:int) where x is width and y is height.
    """
    def __init__(self, adapter, title:str, size:tuple):
        super(ChartWindow, self).__init__(title=title, size=size)
        self.adapter = adapter

        col_choice = Label(self, text="Choice of columns")
        type_nos = Label(self, text="Type of numbers")
        show_min = Label(self, text="Show min")
        show_max = Label(self, text="Show max")

        axe_x = Label(self, text="Axe X")
        axe_y = Label(self, text="Axe Y")
        axe_x_sp = Label(self, text="Axe X Start Point")
        axe_y_duration = Label(self, text="Axe Y Duration")

        col_choice.grid(row=0, column=1, padx=(100, 30))
        type_nos.grid(row=0, column=2, padx=(0, 30))
        show_min.grid(row=0, column=3, padx=(0, 30))
        show_max.grid(row=0, column=4, padx=(0, 30))

        axe_x.grid(row=1, column=0, padx=(0, 80), pady=10)
        axe_y.grid(row=2, column=0, padx=(0, 80), pady=10)
        axe_x_sp.grid(row=3, column=0, padx=(0, 50), pady=10)
        axe_y_duration.grid(row=4, column=0, padx=(0, 60), pady=10)

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

        build_btn = ttk.Button(self, text="BUILD", command=self.transfer_value_and_destroy)
        Label(self, text="").grid(row=5, column=1)
        build_btn.grid(row=6, column=1, padx=(200, 100))


    def update_dropdown(self, values):
        for i in range(0, len(self.dropdowns)):
            self.dropdowns[i]['values'] = values
            self.dropdowns[i].current(i)


    def transfer_value_and_destroy(self):
        """Returns the textbox value."""
        for i in range(0, len(self.text_vars)):
            val = self.text_vars[i].get()
            _k = f'dropdown_choice{i}'
            self.adapter.insert(_k, val)
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
    """
    def __init__(self, adapter, title="Chartify Options", size=(400,400)):
        super(ChartifyOptions, self).__init__(title=title, size=size)
        self.adapter = adapter
        
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
        close_btn = ttk.Button(self, text="Close", command=self.destroy_window)
        apply_btn.grid(row=5, column=0, padx=(0, 100), pady=(100,0))
        close_btn.grid(row=5, column=1, padx=(100, 0), pady=(100,0))


    def add_fonts(self, fonts: list):
        self.table_font['values'] = fonts


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