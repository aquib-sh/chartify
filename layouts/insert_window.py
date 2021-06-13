import sys
sys.path.append("../")
from tkinter import Label
from tkinter import Button
from tkinter import Text
from tkinter.constants import END
from chartify.layouts.window import TopLevelWindow

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
