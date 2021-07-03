#Author : Shaikh Aquib
#Date : June 2021

import tkinter as tk


class MenuBar(tk.Menu):
    """ MenuBar

    MenuBar containing other menus and submenus
    """
    def __init__(self, master:tk.Tk):
        """
        Parameters
        ----------
        master : tk.Tk
            Parent window where menu is to be displayed.
        
        label  : str 
            Label of the current menubar
        """
        super().__init__(master)
        self.master = master

        # Add the first 3 menus
        filemenu  = tk.Menu(self, tearoff=0)
        editmenu  = tk.Menu(self, tearoff=0)
        chartmenu = tk.Menu(self, tearoff=0)
        toolsmenu = tk.Menu(self, tearoff=0)

        # Give names to above menus
        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Edit", menu=editmenu)
        self.add_cascade(label="3D Chart", menu=chartmenu)
        self.add_cascade(label="Tools", menu=toolsmenu)

        # SubMenu inside editmenu
        insertmenu = tk.Menu(editmenu, tearoff=0)
        deletemenu = tk.Menu(editmenu, tearoff=0)
        clearmenu  = tk.Menu(editmenu, tearoff=0)

        # Add labels to the above submenus inside edit menu
        editmenu.add_cascade(label="Insert", menu=insertmenu)
        editmenu.add_cascade(label="Delete", menu=deletemenu)
        editmenu.add_cascade(label="Clear", menu=clearmenu)

        # Row, column options for insert, delete and clear
        insertmenu.add_command(label="Row", command=None)
        insertmenu.add_command(label="Column", command=self.master.insert_new_column)
        
        deletemenu.add_command(label="Row", command=None)
        deletemenu.add_command(label="Column", command=self.master.delete_column)

        clearmenu.add_command(label="Row", command=None)
        clearmenu.add_command(label="Column", command=None)

        filemenu.add_command(label="Open", command=self.master.open_file)
        filemenu.add_command(label="Save", command=self.master.save_file)
        
        draw_chart_menu = tk.Menu(chartmenu, tearoff=0)
        chartmenu.add_cascade(label="Draw Chart", menu=draw_chart_menu)
        
        draw_chart_menu.add_command(label="Select Columns", command=self.master.build_chart)
        draw_chart_menu.add_command(label="Refresh", command=None)

        # Add options to run tools on data in tools menu
        toolsmenu.add_command(label="Detect Collision", command=self.master.detect_collision)
        toolsmenu.add_command(label="Cut Chart", command=None)


class MenuBarExtended(tk.Menu):
    """ MenuBar

    MenuBar containing other menus and submenus
    """
    def __init__(self, master:tk.Tk):
        """
        Parameters
        ----------
        master : tk.Tk
            Parent window where menu is to be displayed.
        
        label  : str 
            Label of the current menubar
        """
        super().__init__(master)
        self.master = master

        # Add the first 3 menus
        filemenu  = tk.Menu(self, tearoff=0)
        editmenu  = tk.Menu(self, tearoff=0)
        chartmenu = tk.Menu(self, tearoff=0)
        toolsmenu = tk.Menu(self, tearoff=0)

        # Give names to above menus
        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Edit", menu=editmenu)
        self.add_cascade(label="3D Chart", menu=chartmenu)
        self.add_cascade(label="Tools", menu=toolsmenu)

        # SubMenu inside editmenu
        # insertmenu = tk.Menu(editmenu, tearoff=0)
        # deletemenu = tk.Menu(editmenu, tearoff=0)
        # clearmenu  = tk.Menu(editmenu, tearoff=0)

        # Add labels to the above submenus inside edit menu
        # editmenu.add_cascade(label="Insert", menu=insertmenu)
        # editmenu.add_cascade(label="Delete", menu=deletemenu)
        # editmenu.add_cascade(label="Clear", menu=clearmenu)

        # Row, column options for insert, delete and clear

        # insertmenu.add_command(label="Row", command=None)
        # insertmenu.add_command(label="Column", command=self.master.insert_new_column)
        
        # deletemenu.add_command(label="Row", command=None)
        # deletemenu.add_command(label="Column", command=self.master.delete_column)

        # clearmenu.add_command(label="Row", command=None)
        # clearmenu.add_command(label="Column", command=None)

        filemenu.add_command(label="Open", command=self.master.open_file)
        filemenu.add_command(label="Save", command=self.master.save_file)
        filemenu.add_command(label="Save As", command=self.master.save_file_as)

        draw_chart_menu = tk.Menu(chartmenu, tearoff=0)
        chartmenu.add_cascade(label="Draw Chart", menu=draw_chart_menu)
        
        draw_chart_menu.add_command(label="Chart3D", command=self.master.wykres)
        draw_chart_menu.add_command(label="Refresh", command=None)

        # Add options to run tools on data in tools menu
        toolsmenu.add_command(label="Detect Collision", command=self.master.detect_collision)
        toolsmenu.add_command(label="Cut Chart", command=self.master.insert_slab)