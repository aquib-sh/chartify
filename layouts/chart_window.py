import sys
sys.path.append("../")
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter.constants import END
from chartify.layouts.window import TopLevelWindow

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