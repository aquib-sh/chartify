import sys
sys.path.append("../")
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter.constants import END
from chartify.layouts.window import TopLevelWindow

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