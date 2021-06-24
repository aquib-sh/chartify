# Author: Shaikh Aquib
# Date: June 2021

import sys
sys.path.append("../")
import tkinter as tk
from tkinter import ttk
from tkinter import Label
from tkinter import Text
from tkinter.constants import END
from chartify.layouts.window import TopLevelWindow

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
