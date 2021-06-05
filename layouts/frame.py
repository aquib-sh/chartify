#Author : Shaikh Aquib
#Date : June 2021

import tkinter as tk

class WindowFrame(tk.Frame):
    """A class for creating and managing frames.

    This class will be used to place spreadsheet inside it.

    Methods
    -------

    """

    def __init__(self, master, width=100, height=300):
        """
        Parameters
        ----------
        master : tkinter.Tk, optional
            root widget on which frame will be placed.
        """
        super().__init__(master, width=width, height=height)


    # def pack_frames(self, side:tk.constants):
    #     """Used to pack the current frame on a root widget.
    #     Parameters
    #     ----------
    #     side : tk.constants
    #         side at which to pack the frame (TOP, BOTTOM, LEFT, RIGHT)
    #     """
    #     self.pack(side)
