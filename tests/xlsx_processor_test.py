import sys
from typing import Sized

sys.path.append("../")
from tkinter.constants import *
from chartify.layouts.window import Application
from chartify.layouts.spreadsheet import Spreadsheet
from chartify.layouts.frame import WindowFrame
from chartify.processors.xlsx_processor import XLSXProcessor
from chartify.menus import menubar
from chartify.config import *


processor = XLSXProcessor(r"sample_data\sales.xlsx")
cols = processor.get_columns()
data = processor.get_data()

app = Application(size=window_size)

app_menubar = menubar.MenuBar(app)
sheet_frame = WindowFrame(app, width=sheetf_width, height=sheetf_height)
sheet = Spreadsheet(sheet_frame)

sheet.set_columns(cols)
sheet.add_rows(data)
sheet_frame.place(
    width=sheetf_width, height=sheetf_height, x=sheetf_coords[0], y=sheetf_coords[1]
)
sheet.pack(expand=True, fill=BOTH)
app.config(menu=app_menubar)
app.start()
