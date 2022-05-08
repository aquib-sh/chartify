import sys

sys.path.append("../")
import tkinter as tk
from chartify.layouts import spreadsheet

root = tk.Tk()

sheet = spreadsheet.Spreadsheet(root)
cols = ("FirstName", "LastName", "Area", "Pincode")
data = [
    ("Aquib", "Shaikh", "Worli", "400018"),
    ("Mustafa", "Khan Bahadur Al Kurlawi", "Kurla", "400070"),
    ("Saif", "Shaikh", "Dharavi", "400010"),
]

sheet.set_columns(cols)
sheet.add_rows(data)
sheet.display()
root.mainloop()
