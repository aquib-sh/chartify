#Author : Shaikh Aquib
#Date : June 2021

import sys
import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTTOM, CENTER, LEFT
sys.path.append('../')

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
