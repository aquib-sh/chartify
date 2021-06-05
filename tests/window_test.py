import sys
from typing import Sized
sys.path.append('../')
from tkinter.constants import *
from chartify.layouts.window import Application
from chartify.layouts.spreadsheet import Spreadsheet
from chartify.layouts.frame import WindowFrame
from chartify.menus import menubar
from chartify.config import *

app = Application(size=window_size)

app_menubar = menubar.MenuBar(app)

sheet_frame = WindowFrame(app, width=sheetf_width, height=sheetf_height)
sheet = Spreadsheet(sheet_frame)

cols = ('FirstName', 'LastName', 'Area', 'Pincode', 'Job')
data = [
    ('Aquib', 'Shaikh', 'Worli', '400018', 'Python Developer'),
    ('Mustafa', 'Khan Bahadur Al Kurlawi', 'Kurla', '400070', 'Pirated DVD Seller'),
    ('Saif', 'Shaikh', 'Dharavi', '400010', 'Sales Manager'),
]

sheet.set_columns(cols)
sheet.add_rows(data)
sheet_frame.place(width=sheetf_width, height=sheetf_height, x=sheetf_coords[0], y=sheetf_coords[1])
sheet.pack(expand=True, fill=BOTH)
app.config(menu=app_menubar)
app.start()