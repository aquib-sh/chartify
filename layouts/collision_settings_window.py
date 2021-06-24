import sys
sys.path.append("../")
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter.constants import END
from chartify.layouts.window import TopLevelWindow

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