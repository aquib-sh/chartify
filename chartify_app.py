import os
import sys
import math
from tkinter import font
from matplotlib import colors
from numpy.core.fromnumeric import size, sort
from numpy.lib.function_base import insert
sys.path.append('../')
import datetime
import traceback
import numpy as np
import pandas
import tksheet
import config
import tkinter as tk
from tkinter import N, S, E, W
from tkinter.constants import *
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from menus.menubar import MenuBarExtended
from layouts.frame import WindowFrame
from layouts.window import ColumnSelectionWindow
from layouts.window import InsertWindow
from layouts.window import InsertRowWindow
from layouts.window import DeleteWindow
from layouts.window import CustomColorsWindow
from layouts.window import ChartifyOptions
from layouts.window import CollisionReport
from layouts.window import CollisionSettings
from layouts.window import CutChartSettings
from layouts.window import CutChartNumericalSettings
from processors.data_adapter import DataAdapter
from processors.timeline_mapper import TimelineMapper
from processors.styler import ChartifyStyler
from processors.cache_memory import CacheProcessor
from processors.cache_memory import CacheSaver
from processors.cache_memory import CacheRetriever
from tools.collision_detector import CollisionDetector
from tools.slab import Slab


class ChartifyAppExtended(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(config.title)
        self.base_file            = None
        self.axes                 = None
        self.temp                 = None
        self.fig                  = None
        self.fig_bg               = None
        self.actual_fig_bg        = "white"
        self.df                   = None
        self.sheet_font           = None
        self.sheet_fsize          = None
        self.chart_title_font     = None
        self.chart_title_color    = "black"
        self.chart_title_fsize    = 20
        self.chart_axis_lbl_font  = None
        self.chart_axis_lbl_color = "black"
        self.chart_axis_lbl_fsize = 15
        self.marker_color         = "yellow"
        self.aux_line_color       = "blue"
        self.yaxis_min            = None
        self.zaxis_min            = None
        self.xaxis_min            = None
        self.yaxis_max            = None
        self.zaxis_max            = None
        self.xaxis_max            = None
        self.cache = {'fig_bg':None, 'sheet_font':None, 'sheet_fsize':None}
        self.graph_coords = {'x':[], 'y':[], 'z':[]}
        self.raw_graph_coords = {'x':[], 'y':[], 'z':[]}
        # Keep track of cube start and end positions along with y, z
        self.cubes = {
                'start' : [], 
                'end'   : [],
                'y'     : [],
                'z'     : []
            } 
        self.saver = CacheSaver()
        self.color_cache = CacheProcessor("colors.db", "colors")
        self.retriever = CacheRetriever()

        self.iconbitmap("icon.ico")

        if self.retriever.cache_exists():
            self.cache = self.retriever.retrieve_cache()
            if self.cache['fig_bg'] != None and len(self.cache['fig_bg']) > 0: 
                self.fig_bg = self.cache['fig_bg']
            
            if self.cache['sheet_font'] != None and len(self.cache['sheet_font']) > 0: 
                self.sheet_font = self.cache['sheet_font']
            
            if self.cache['sheet_fsize'] != None: 
                self.sheet_fsize = self.cache['sheet_fsize']

            if "marker_color" in self.cache:
                self.marker_color = self.cache['marker_color']
            else:
                self.marker_color = "orange"

            if "aux_line_color" in self.cache:
                self.aux_line_color = self.cache['aux_line_color']
            else:
                self.aux_line_color = "grey"

            if "axis_label_color" in self.cache:
                self.axis_label_color = self.cache['axis_label_color']
            else:
                self.axis_label_color = "black"

            if "axis_label_fsize" in self.cache:
                self.axis_label_fsize = float(self.cache['axis_label_fsize'])
            else:
                self.axis_label_fsize = 12

            if "chart_title_color" in self.cache:
                self.chart_title_color = self.cache['chart_title_color']
            else:
                self.chart_title_color = "black"

            if "chart_title_fsize" in self.cache:
                self.chart_title_fsize = float(self.cache['chart_title_fsize'])
            else:
                self.chart_title_fsize = 12

            if "chart_title_font" in self.cache:
                self.chart_title_font = self.cache['chart_title_font']

            if "chart_title_color" in self.cache:
                self.chart_title_color = self.cache['chart_title_color']
            else:
                self.chart_title_color = "black"

            if "chart_title_fsize" in self.cache:
                self.chart_title_fsize = float(self.cache['chart_title_fsize'])
            else:
                self.chart_title_fsize = 12

            if "chart_axis_lbl_font" in self.cache:
                self.chart_axis_lbl_font = self.cache['chart_axis_lbl_font']

            if "chart_axis_lbl_color" in self.cache:
                self.chart_axis_lbl_color = self.cache['chart_axis_lbl_color']
            else:
                self.chart_axis_lbl_color = "black"

            if "chart_axis_lbl_fsize" in self.cache:
                self.chart_axis_lbl_fsize = float(self.cache['chart_axis_lbl_fsize'])
            else:
                self.chart_axis_lbl_fsize = 12

            if "actual_fig_bg" in self.cache:
                self.actual_fig_bg = self.cache['actual_fig_bg']
            else:
                self.actual_fig_bg = "white"


        self.adapter = DataAdapter()
        self.X = self.Y = self.Z = None
        self.choice_is_null = True

        self.menubar = MenuBarExtended(self)

        self.config(menu=self.menubar)

        self.sheet = tksheet.Sheet(self, width=1000, height=600)

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=3)
 

        self.sheet.enable_bindings(("all"))
        self.sheet.grid(row=0, column=0, sticky=N+S+W+E)
        self.sheet.columnconfigure(1, weight=3)
        self.sheet.rowconfigure(1, weight=3)
        if self.sheet_font:
            styler = ChartifyStyler(self, self.sheet, figure=self.fig)
            styler.set_sheet_font(self.sheet_font)

        self.current_file_name = ""

        self.zaxis_column = 'Sala'
        self.yaxis_column = 'Profesor'
        self.xaxis_column='Czas rozpoczęcia'
        #self.end_column='Czas zakończenia'
        self.duration_column='Czas trwania (min)'

        self.colors =['blue','red','green','yellow','orange','violet','peru','pink']

        #losuj pozostale kolory
        for i in range(0,60):
            random_color = list(np.random.random(size=3) ) 
            self.colors.append(random_color)

    def open_file(self):
        """Opens up file chooser to select the file
           calls load_file() to import data into spreadsheet.
        """
        start_dir = "/"
        if self.retriever.cache_exists():
            self.cache = self.retriever.retrieve_cache()
            if "recently_opened" in self.cache: start_dir = self.cache["recently_opened"]

        file_name = filedialog.askopenfilename(initialdir=start_dir,
                                        title="Open a file",
                                        filetype=( ("csv files", "*.csv"), ("xlsx files", "*.xlsx"),("all files", "*.*")))
        if file_name == '':
            return
    
        current_file_name = file_name
        self.load_file(current_file_name)
        self.cache['recently_opened'] = os.path.dirname(current_file_name)
        self.saver.save_cache(self.cache)
        self.choice_is_null = True

        self.yaxis_min = None
        self.zaxis_min = None
        self.xaxis_min = None
        self.yaxis_max = None
        self.zaxis_max = None
        self.xaxis_max = None



    def __straighten_list(self, elems: list) -> list:
        out = []
        for elem in elems:
            out += list(elem)
        return out


    def load_file(self, filename):
        """Loads the file into application by placing it into spreadsheet."""

        if not filename.lower().endswith(".csv"):
            self.df = pandas.read_excel(filename, engine='openpyxl')
        else:
            self.df = pandas.read_csv(filename)

        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)
        self.current_file_name = filename
        self.base_file = os.path.basename(filename)
        self.title(f"{self.base_file} - Chartify")


    def save_file(self):
        """Performs tasks for saving the existing spreadsheet data in CSV and XLSX formats."""
        if self.current_file_name.lower().endswith(".csv"):
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_csv(self.current_file_name, index=False)
        
        elif self.current_file_name.lower().endswith(".xlsx"):
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_excel(self.current_file_name, index=False)

        else:
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_csv("Output.csv", index=False)
            messagebox.showerror("No name specified","Data sucessfully saved to Output.csv")


    def save_file_as(self):
        """Performs tasks for saving as file for the existing spreadsheet data in CSV and XLSX formats."""
        file_name = filedialog.asksaveasfilename(initialdir="/",
                                        title="Choose file",
                                        filetype=(("csv files", "*.csv"),("xlsx files", "*.xlsx"),("all files", "*.*")))
    
        if file_name == '':
            return
        if (not file_name.endswith(".csv")) and (not file_name.endswith(".xlsx")):
            file_name += ".csv"
        self.current_file_name = file_name
        self.save_file()


    def cuboid_data(self, pos, size=(1,1,1)):
        o = [a - b / 2 for a, b in zip(pos, size)]
        l, w, h = size
        x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],  
             [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
             [o[0], o[0] + l, o[0] + l, o[0], o[0]],  
             [o[0], o[0] + l, o[0] + l, o[0], o[0]]]  
        y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],  
             [o[1], o[1], o[1] + w, o[1] + w, o[1]],  
             [o[1], o[1], o[1], o[1], o[1]],          
             [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]   
        z = [[o[2], o[2], o[2], o[2], o[2]],                       
             [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],   
             [o[2], o[2], o[2] + h, o[2] + h, o[2]],               
             [o[2], o[2], o[2] + h, o[2] + h, o[2]]]               
        return np.array(x), np.array(y), np.array(z)


    def plotCubeAt(self, pos=(0,0,0),size=(1,1,1),color='b', ax=None):
        if ax !=None:
            x, y, z = self.cuboid_data(pos,size )
            self.temp = x            
            self.raw_graph_coords['x'].append(x.copy())
            self.raw_graph_coords['y'].append(y.copy())
            self.raw_graph_coords['z'].append(z.copy())

            plain_x = self.__straighten_list(list(x))
            plain_y = self.__straighten_list(list(y))
            plain_z = self.__straighten_list(list(z))
            avg_y   = sum(plain_y)/len(plain_y)
            avg_z   = sum(plain_z)/len(plain_z)

            self.graph_coords['x'] += plain_x # Add the x-coords into the tracker
            self.graph_coords['y'] += plain_y # Add the y-coords into the tracker
            self.graph_coords['z'] += plain_z # Add the z-coords into the tracker

            self.cubes['start'].append(min(plain_x))
            self.cubes['end'].append(max(plain_x))
            self.cubes['y'].append(avg_y)
            self.cubes['z'].append(avg_z)
            
            ax.plot_surface(x,y,z, color=color)


    def convert_timeunit(self, d: datetime.datetime) -> int:
        """Converts a variable with components to appropriate unit."""
        if self.duration_dtype == "Week":
            return (d.components.days/7)
        elif self.duration_dtype == "Day":
            return (d.components.days)
        elif self.duration_dtype == "Hour":
            return (d.components.days*24 + d.components.hours)
        elif self.duration_dtype == "Minute":
            return (d.components.days*24*60 + d.components.hours*60 + d.components.minutes)
        elif self.duration_dtype == "Second":
            return (d.components.days*24*60*60 + d.components.hours*60*60 + d.components.minutes*60 + d.components.seconds)


    def generate_timeseries_xaxis(self, end: int, 
        step: int, label_format: str, min: datetime.timedelta) -> list:
        """Generate list for the time data of xaxis.
        
        Parameters
        ----------
        end: int
            Sum total of all the data (minutes or seconds or years...)

        step: int
            Step by which to increment the range.

        format: str
            string containing '{}' and yyyy, mm, dd, hh, _mm, ss symbols to fill using formated strings.
        """
        data = []
        #print(self.duration_dtype)
        weeks_in_a_year: int = 365//7

        for i in range(0, end, step):
            if self.duration_dtype == "Week":
                year   = min.year + (i//weeks_in_a_year)
                month  = int(min.month + (i//4)) % 12
                day    = int(min.day + i*7) % 30
                hour   = min.hour
                minute = min.minute
                second = min.second

            elif self.duration_dtype == "Day":
                year   = min.year   + i//365
                month  = (min.month + i//30)%12
                day    = i%30
                hour   = min.hour
                minute = min.minute
                second = min.second

            elif self.duration_dtype == "Hour":
                year   = min.year  + i//24//365
                month  = min.month + i//24//30
                day    = (min.day  + i//24) % 30
                hour   = (min.hour + i) % 24
                minute = min.minute
                second = min.second

            elif self.duration_dtype == "Minute":
                #print("Entered minutes section")
                year   = min.year    + i//60//24//365
                month  = min.month   + i//60//24//30
                day    = (min.day    + i//60//24) % 30
                hour   = (min.hour   + i//60) % 24
                minute = (min.minute + i) % 60
                #print(f"BASE {min.minute}\tADD {i}\tYIELD {minute}")
                second = min.second
        
            elif self.duration_dtype == "Second":
                year   = min.year    + i//60//60//24//365
                month  = min.month   + i//60//60//24//30
                day    = (min.day    + i//60//60//24) % 30
                hour   = (min.hour   + i//60//60) % 24
                minute = (min.minute + i/60) % 60
                second = (min.second  + i) % 60

            else:
                year = min.year
                hour = int(min.hour + i/60 ) % 24
                minute = min.minute
                second = min.second
                ddd = min.hour*60 + min.minute + i
                day = int(min.day + ddd/60/24)
                month = min.month

            label = label_format.format(yyyy=year, mm=month, dd=day,
                hh=hour, _mm=minute, ss=second)
            #print("LBL", label)
            data.append(label)

        return data

    
    def num_convert_duration(self, duration: float) -> float:
        """Converts the duration value to the appropriate by dtype of duration column."""
        res = float(duration)/1000
        if ((self.xaxis_dtype == "KiloMeter" and self.duration_dtype == "KiloMeter")
            or
            (self.xaxis_dtype == "Meter" and self.duration_dtype == "Meter")
            or
            (self.xaxis_dtype == "Number" and self.duration_dtype == "Number")):
            res = float(duration)

        elif (self.xaxis_dtype == "Meter" and self.duration_dtype == "KiloMeter"):
            res = float(duration)*1000
        return res
        

    def num_add_duration_to_start(self, val: float, duration: float) -> float:
        """Adds value to duration according to the datatype of xaxis and duration columns."""
        res = float(val) + self.num_convert_duration(duration)
        return res
        

    def set_axes_labels(self, axes, xlbl:str, ylbl:str, zlbl:str):
        """Sets the labels for the axis provided."""
        axes.set_xlabel(
            xlbl, 
            fontweight ='bold', 
            labelpad=30, 
            font=self.chart_axis_lbl_font, 
            fontsize=self.chart_axis_lbl_fsize
        )
        axes.set_ylabel(
            ylbl, 
            fontweight='bold', 
            font=self.chart_axis_lbl_font, 
            fontsize=self.chart_axis_lbl_fsize
        )
        axes.set_zlabel(
            zlbl, 
            fontweight='bold', 
            font=self.chart_axis_lbl_font, 
            fontsize=self.chart_axis_lbl_fsize
        )


    def update_rgba_from_cache(self):
        stored_colors = self.color_cache.retrieve_cache()
        if self.chart_axis_lbl_color in stored_colors:
            self.chart_axis_lbl_color = stored_colors[self.chart_axis_lbl_color] 
                
        if self.chart_title_color in stored_colors:
            self.chart_title_color = stored_colors[self.chart_title_color]
        
        if self.fig_bg in stored_colors:
            self.fig_bg = stored_colors[self.fig_bg]

        if self.actual_fig_bg in stored_colors:
            self.actual_fig_bg = stored_colors[self.actual_fig_bg]
        

    def set_axes_label_color(self, axes, xlbl_color, ylbl_color, zlbl_color):
        """Sets the color of axes labels in 3D chart for x, y, z."""
        axes.xaxis.label.set_color(xlbl_color)
        axes.yaxis.label.set_color(ylbl_color)
        axes.zaxis.label.set_color(zlbl_color)
        
        
    def set_actual_fig_bg(self, axes, color):
        """Sets the background of the actual figure."""
        axes.set_facecolor(self.actual_fig_bg)


    def calculate_step_values(self, points) -> int:
        """Decides values to jump/step value of x axis points."""
        jump = 1
        if   points <= 25    : jump = 5
        elif points <= 50    : jump = 10
        elif points <= 100   : jump = 15
        elif points <= 500   : jump = 30
        elif points <= 1000  : jump = 60
        elif points <= 2000  : jump = 120
        elif points <= 3000  : jump = 240
        elif points <= 10000 : jump = 1000
        elif points >  10000 : jump = 10000
        return jump


    def draw_cut_chart(self, datatype:str, 
        timeseries=None, figure_present=False
        ):

        if datatype not in ['time', 'numerical']:
            raise Exception("[!] datatype parameter must be 'time' or 'numerical'")

        # If data is time but the timeseries data is not provided
        if datatype == 'time' and not timeseries:
            raise Exception("[!] 'time' datatype requires timeseries data.")

        self.graph_coords['xplane'] = []
        slab_color  = 'cyan'
        alpha_value = 0.4

        if datatype == "time":
            slab_color = 'red'
            tmap = TimelineMapper(timeseries, self.X)
            dates = tmap.get_all_dates()
            
            settings = CutChartSettings(self.adapter, dates)
            settings.start()
            
            selected_date = self.adapter.get('cut-chart-setting-date')
            selected_time = self.adapter.get('cut-chart-setting-time')
            # Get the cutting point
            xpoint = tmap.get_point(f"{selected_date} {selected_time}")
        
        elif datatype == "numerical":
            settings = CutChartNumericalSettings(self.adapter)
            settings.start()
            # Get the cutting point
            xpoint = float(self.adapter.get('cut-chart-setting-point'))

        print("Reached till slab")
        slaby = Slab(self.axes)
        x, y, z = slaby.insert_slab_by_x(point=xpoint, X=self.X, Y=self.Y, Z=self.Z)
        self.axes.plot_surface(
            x, y, z, 
            color=slab_color, 
            alpha=alpha_value
        )
        # Drawing Auxillary lines and markings on intersections
        intersections = self.detect_intersection(x[0][0])
        
        print("[+] Intersections detection done")

        if len(intersections) == 0:
            print("[+] No intersections found")
        else:
            self.plot_intersections(intersections)

        print("Drawing figure")
        if figure_present : plt.draw()
        else              : plt.show()


    def plot_chart(self, tool="draw", fig_present=False):
        """Plots the chart based on data type."""
        # Empty the coordinates tracker before plotting a new chart
        self.graph_coords['cuboids'] = {'x':[], 'y':[], 'z':[]} 
        self.raw_graph_coords        = {'x':[], 'y':[], 'z':[]}
        self.cubes                   = {'start':[], 'end':[], 'y':[], 'z':[]}

        sheet_data    = self.sheet.get_sheet_data()
        sheet_headers = self.sheet.headers()
        df = pandas.DataFrame(sheet_data, columns = sheet_headers) 

        # Open column choice window only if it hasn't been chosen already.
        if self.choice_is_null : self.open_column_selection()
        df[self.duration_column] = pandas.to_numeric(df[self.duration_column])

        try:
            if not fig_present:
                fig = plt.figure(figsize=(16,9))
                self.fig = fig

                self.fig.canvas.manager.set_window_title(self.base_file)
                ax = fig.add_subplot(projection='3d')
                self.axes = ax

            ax = self.axes

            self.set_axes_labels(
                axes=ax, 
                xlbl=self.xaxis_column, 
                ylbl=self.yaxis_column, 
                zlbl=self.zaxis_column
            )
            self.update_rgba_from_cache()
            self.set_axes_label_color(
                axes=ax,
                xlbl_color=self.chart_axis_lbl_color,
                ylbl_color=self.chart_axis_lbl_color,
                zlbl_color=self.chart_axis_lbl_color
            )   
            self.set_actual_fig_bg(axes=ax, color=self.actual_fig_bg)

            dtype_xaxis = str(df[self.xaxis_column].dtype)

            if dtype_xaxis == 'object':
                df[self.xaxis_column] = pandas.to_datetime(df[self.xaxis_column])
                df.sort_values(by=[self.xaxis_column], inplace=True)
                #okreslamy zakres czasowy 
                minvals = df.min()
                maxvals = df.max()

                if self.xaxis_min != None:
                    min = pandas.to_datetime(self.xaxis_min)
                else:
                    min = minvals[self.xaxis_column] #najwczesniejsza data wśród dat rozpoczęcia
                
                if self.xaxis_max != None:
                    if self.duration_dtype == 'Week':
                        max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(weeks=int(maxvals[self.duration_column]))
                    elif self.duration_dtype == 'Day':
                        max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(days=int(maxvals[self.duration_column]))
                    elif self.duration_dtype == 'Hour':
                        max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(hours=int(maxvals[self.duration_column]))
                    elif self.duration_dtype == 'Minute':
                        max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(minutes=int(maxvals[self.duration_column]))
                    elif self.duration_dtype == 'Second':
                        max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(seconds=int(maxvals[self.duration_column]))
                    else:
                        max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(minutes=int(maxvals[self.duration_column]))

                else:
                    max = maxvals[self.xaxis_column]+datetime.timedelta(minutes=int(maxvals[self.duration_column]))
                
                d = max - min # period

                # how many minutes are there from the beginning 
                # of the first lecture to the end of the last lecture
                dminutes = self.convert_timeunit(d)

                ax.set_xlim(0,dminutes)

                odstep_min = self.calculate_step_values(points=dminutes)

                time_label_format = None

                if self.xaxis_dtype == "Time(yyyy-mm-dd hh:mm:ss)":
                    time_label_format = "{yyyy}-{mm}-{dd} {hh}:{_mm}:{ss}"
                else:
                    time_label_format = "{dd}/{mm}/{yyyy} {hh}:{_mm}:{ss}"

                start_times = self.generate_timeseries_xaxis(
                    end=dminutes, 
                    step=odstep_min, 
                    label_format=time_label_format, 
                    min=min
                )

                self.X = np.arange(0,dminutes,odstep_min)
                #print("X axis coords are", self.X)
                ax.set_xticks(self.X)
                #print("LABELS SET ARE X", start_times)
                ax.set_xticklabels(start_times, rotation='vertical', fontsize=9)

                #lista osób prowadzacych zajęcia
                professors = df[self.yaxis_column].unique()

                if self.yaxis_min != None and self.yaxis_max != None:
                     professors = [prof for prof in professors if (prof >= self.yaxis_min) and (prof <= self.yaxis_max)]

                ax.set_ylim(0,len(professors))
                self.Y = np.arange(0,len(professors),1)
                ax.set_yticks(self.Y)
            
                ax.set_yticklabels(professors, fontsize=10)

                rooms = df[self.zaxis_column].unique()

                if self.zaxis_min != None and self.zaxis_max != None:
                     rooms = [room for room in rooms if (room >= self.zaxis_min) and (room <= self.zaxis_max)]

                ax.set_zlim(0,len(rooms))
                self.Z = np.arange(0,len(rooms),1)
                ax.set_zticks(self.Z)
                ax.set_zticklabels(rooms, fontsize=10)

                self.axes = ax

                try:
                    for index, row in df.iterrows():
                        prof     = row[self.yaxis_column]
                        room     = row[self.zaxis_column]
                        start    = row[self.xaxis_column]
                        duration = row[self.duration_column]

                        # If elements are out of range for any of 3 axis then skip to next.
                        if (
                            ((self.yaxis_min != None and self.yaxis_max != None) 
                            and ((prof < self.yaxis_min) or prof > (self.yaxis_max))
                            )

                            or

                            ((self.xaxis_min != None and self.xaxis_max != None)
                            and (pandas.to_datetime(start) < pandas.to_datetime(self.xaxis_min) or (pandas.to_datetime(start) > pandas.to_datetime(self.xaxis_max)))
                            )

                            or

                            ((self.zaxis_min != None and self.zaxis_max != None) 
                            and ((room < self.zaxis_min) or (room > self.zaxis_max))
                            )
                        ) : continue

                        d = start - min
                        startunits = self.convert_timeunit(d)

                        y = np.where(np.array(professors) == prof)[0][0]
                        z = np.where(np.array(rooms) == room)[0][0]
                        
                        # Get color from database.
                        stored_colors = self.color_cache.retrieve_cache()

                        # Check if the colors are from database or from system.
                        prof = str(prof)
                        obj_color = self.colors[y]
                        # If value if present in adapter for current y-axis value.
                        if self.adapter.ispresent(prof):
                            obj_color = self.adapter.get(prof)
                            # If colorname is from a stored_color db then assign the value.
                            if obj_color in stored_colors : obj_color = stored_colors[obj_color]

                        plot_pos = startunits+duration/2,y,z
                        self.plotCubeAt(pos=(plot_pos),size=(duration,0.1,0.1),color=obj_color, ax=ax)
                        
                    plot_title = plt.title("Schedule", font=self.chart_title_font, fontsize=self.chart_title_fsize)
                    plt.setp(plot_title, color=self.chart_title_color)
                
                    if self.fig_bg : self.fig.patch.set_facecolor(self.fig_bg)

                    if tool == "draw":
                        plt.show()
                        
                    elif tool == "cut":
                        self.draw_cut_chart(
                            datatype='time',
                            timeseries=start_times,
                            figure_present=fig_present
                        )
            
                except Exception as e:
                    messagebox.showerror("Error","Error creating plot\r\n"+traceback.format_exc())

            # ===================================================================================================
            # ===================================== NUMERIC DATA TYPE ===========================================
            # ===================================================================================================
            elif dtype_xaxis in ['float64', 'int64']:

                df.sort_values(by=[self.xaxis_column],inplace=True)
                # time range
                minvals = df.min()
                maxvals = df.max()

                if self.xaxis_min : min = float(self.xaxis_min)
                else : min = 0

                if self.xaxis_max: 
                    max = float(self.xaxis_max)
                else: 
                    max = self.num_add_duration_to_start(
                        maxvals[self.xaxis_column], 
                        maxvals[self.duration_column]
                    )

                jump = self.calculate_step_values(points=max)

                self.X = []

                if max < min:
                    raise Exception("[!] MIN value cannot be greater than MAX")

                # If number is in the fractional part of min
                # example: min=6, max=6.2
                temp = min
                if (int(min) == int(max)) and (max < int(min)+1):
                    while round(temp, 1) < round(max, 1):
                        self.X.append(temp)
                        temp += 0.1
                else:
                    for i in range(int(min), int(max)+1, jump):
                        self.X.append(i)

                self.X = np.array(self.X)

                ax.set_xticks(self.X)
                ax.set_xticklabels(self.X, rotation='vertical', fontsize=9)
                ax.set_xlim(0, int(max))

                # object list
                professors = df[self.yaxis_column].unique()

                if self.yaxis_min != None and self.yaxis_max != None:
                    temp = []
                    for prof in professors:
                        if ((prof >= self.yaxis_min) and (prof <= self.yaxis_max)):
                            temp.append(temp)

                    professors = temp.copy()
                    del temp

                professors.sort()

                ax.set_ylim(0,len(professors))
                self.Y = np.arange(0,len(professors),1)
                ax.set_yticks(self.Y)
                ax.set_yticklabels(professors, fontsize=10)

                #lista sal
                rooms = df[self.zaxis_column].unique()

                if self.zaxis_min != None and self.zaxis_max != None:
                    temp = []
                    for room in rooms:
                        if (room >= self.zaxis_min) and (room <= self.zaxis_max):
                            temp.append(room)

                    rooms = temp.copy()
                    del temp

                rooms.sort()

                ax.set_zlim(0,len(rooms))
                self.Z = np.arange(0,len(rooms),1)
                ax.set_zticks(self.Z)
                ax.set_zticklabels(rooms, fontsize=10)
                self.axes = ax               
                
                try:
                    for index, row in df.iterrows():
 
                        prof     = row[self.yaxis_column]
                        room     = row[self.zaxis_column]
                        start    = row[self.xaxis_column]
                        duration = row[self.duration_column]

                        # If elements are out of range for any of 3 axis then skip to next.
                        if (
                            ((self.yaxis_min != None and self.yaxis_max != None) 
                            and ((prof < self.yaxis_min) or prof > (self.yaxis_max))
                            )

                            or

                            ((self.xaxis_min != None and self.xaxis_max != None)
                            and (float(start) < float(self.xaxis_min) or (float(start) > float(self.xaxis_max)))
                            )

                            or

                            ((self.zaxis_min != None and self.zaxis_max != None) 
                            and ((room < self.zaxis_min) or (room > self.zaxis_max))
                            )
                            ) : continue
                        
                        _y = np.where(np.array(professors) == prof)[0]
                        _z = np.where(np.array(rooms) == room)[0]

                        if len(_y) == 0 or len(_z) == 0 : continue

                        y = _y[0]
                        z = _z[0]

                        xpos = self.num_add_duration_to_start(float(start), float(duration)/2)
                        plot_pos = (xpos,y,z) 

                        # Get color from database.
                        stored_colors = self.color_cache.retrieve_cache()

                        # Check if the colors are from database or from system.
                        prof = str(prof)
                        obj_color = self.colors[y]
                        # If value if present in adapter for current y-axis value.
                        if self.adapter.ispresent(prof):
                            obj_color = self.adapter.get(prof)
                            # If colorname is from a stored_color db then assign the value.
                            if obj_color in stored_colors : obj_color = stored_colors[obj_color]

                        self.plotCubeAt(pos=plot_pos,size=(self.num_convert_duration(duration),0.1,0.1),color=obj_color, ax=ax)

                    plot_title = plt.title("Schedule", font=self.chart_title_font, fontsize=self.chart_title_fsize)
                    plt.setp(plot_title, color=self.chart_title_color)

                    if self.fig_bg : self.fig.patch.set_facecolor(self.fig_bg)

                    if tool == "draw":
                        plt.show()

                    elif tool == "cut":                        
                        self.draw_cut_chart(
                            datatype='numerical',
                            figure_present=fig_present
                        )

                except Exception as e:
                    messagebox.showerror("Error "," Error while creating the chart \r\n"+traceback.format_exc())

        except Exception as e:
            messagebox.showerror("Error", "Error in calculations for the graph \r \n"+traceback.format_exc())


    def plot_intersections(self, intersections):
        # Get color from database.

        stored_colors = self.color_cache.retrieve_cache()
        if self.marker_color in stored_colors   : self.marker_color   = stored_colors[self.marker_color]
        if self.aux_line_color in stored_colors : self.aux_line_color = stored_colors[self.aux_line_color]

        for coords in intersections:
            self.axes.scatter3D(coords[0], coords[1], coords[2],
                marker='D', 
                alpha=1, 
                color=self.marker_color, 
                s=100)

            # ============== lines from y axis ===============
            y = [coords[1]]
            inc = 1
            
            while y[-1] < max(self.Y):
                y.append(coords[1]+inc)
                inc += 1
            
            x = [coords[0]]*len(y)
            z = [coords[2]]*len(y)

            self.axes.plot3D(x, y, z, self.aux_line_color, linestyle="--")
            # ============= lines from z axis ==================
            z1 = [coords[2]]
            inc1 = 1
            while z1[-1] > min(self.Z):
                point = coords[2]-inc1
                z1.append(point)
                inc1 += 1

            x1 = [coords[0]]*len(z1)
            y1 = [coords[1]]*len(z1)
            
            self.axes.plot3D(x1, y1, z1, self.aux_line_color, linestyle="--")

            x=y=z=x1=y1=z1=[]
            #print("==="*10)


    def open_column_selection(self):
        col_selection_window = ColumnSelectionWindow(self.adapter, dataframe=self.df, title="Column Selection", size=(1000,500))
        col_selection_window.update_dropdown(list(self.df.keys()))
        col_selection_window.start()

        self.zaxis_column    = self.adapter.get('zaxis')
        self.yaxis_column    = self.adapter.get('yaxis')
        self.xaxis_column    = self.adapter.get('xaxis')
        self.duration_column = self.adapter.get('duration')
        self.xaxis_dtype     = self.adapter.get('xaxis_type')
        self.duration_dtype  = self.adapter.get('duration_type')

        if self.adapter.ispresent('range_window_opened'):
            self.yaxis_min = self.adapter.get('yaxis_min')
            self.zaxis_min = self.adapter.get('zaxis_min')
            self.xaxis_min = self.adapter.get('xaxis_min')
            self.yaxis_max = self.adapter.get('yaxis_max')
            self.zaxis_max = self.adapter.get('zaxis_max')
            self.xaxis_max = self.adapter.get('xaxis_max')
            self.adapter.delete('range_window_opened')

        self.choice_is_null = False


    def show_options(self):
        styler = ChartifyStyler(self, self.sheet, figure=self.fig)
        fonts = styler.get_all_fonts()
        if self.choice_is_null : self.open_column_selection()
        cols = list(self.df[self.yaxis_column].unique())
        db_colors = self.color_cache.retrieve_cache()

        opts = ChartifyOptions(self.adapter, cols, db_colors)
        opts.add_fonts(fonts)
        opts.start()

        tbl_font             = self.adapter.get("table-font")
        tbl_fsize            = self.adapter.get("table-font-size")
        graph_bg             = self.adapter.get("graph-background")
        marker_color         = self.adapter.get("marker-color")
        aux_line_color       = self.adapter.get("aux-line-color")
        chart_title_font     = self.adapter.get("chart-title-font")
        chart_title_color    = self.adapter.get("chart-title-color")
        chart_title_fsize    = self.adapter.get("chart-title-font-size")
        chart_axis_lbl_font  = self.adapter.get("chart-axis-lbl-font")
        chart_axis_lbl_color = self.adapter.get("chart-axis-lbl-color")
        chart_axis_lbl_fsize = self.adapter.get("chart-axis-lbl-font-size")
        actual_fig_bg        = self.adapter.get("actual-figure-background")

        if tbl_font  != None and tbl_font != '': 
            self.sheet_font = tbl_font
            self.cache['sheet_font'] = self.sheet_font
            styler.set_sheet_font(self.sheet_font)

        if tbl_fsize != None and tbl_fsize != '': 
            self.sheet_fsize = int(tbl_fsize)
            self.cache['sheet_fsize'] = self.sheet_fsize
            styler.set_sheet_font_size(self.sheet_fsize) 
        
        if graph_bg  != None and graph_bg  != '':
            self.fig_bg = graph_bg
            self.cache['fig_bg'] = self.fig_bg

        if marker_color != None and marker_color != '':
            self.marker_color = marker_color
            self.cache['marker_color'] = self.marker_color
        
        if aux_line_color != None and aux_line_color != '':
            self.aux_line_color = aux_line_color
            self.cache['aux_line_color'] = self.aux_line_color

        if chart_title_font != None and chart_title_font != '':
            self.chart_title_font = chart_title_font
            self.cache['chart_title_font'] = self.chart_title_font
        
        if chart_title_color != None and chart_title_color != '':
            self.chart_title_color = chart_title_color
            self.cache['chart_title_color'] = self.chart_title_color
        
        if chart_title_fsize != None and chart_title_fsize != '':
            self.chart_title_fsize = float(chart_title_fsize)
            self.cache['chart_title_fsize'] = self.chart_title_fsize
        
        if chart_axis_lbl_font != None and chart_axis_lbl_font != '':
            self.chart_axis_lbl_font = chart_axis_lbl_font
            self.cache['chart_axis_lbl_font'] = self.chart_axis_lbl_font
        
        if chart_axis_lbl_color != None and chart_axis_lbl_color != '':
            self.chart_axis_lbl_color = chart_axis_lbl_color
            self.cache['chart_axis_lbl_color'] = self.chart_axis_lbl_color
        
        if chart_axis_lbl_fsize != None and chart_axis_lbl_fsize != '':
            self.chart_axis_lbl_fsize = float(chart_axis_lbl_fsize)
            self.cache['chart_axis_lbl_fsize'] = self.chart_axis_lbl_fsize

        if actual_fig_bg != None and actual_fig_bg != '':
            self.actual_fig_bg = actual_fig_bg
            self.cache['actual_fig_bg'] = self.actual_fig_bg

        self.saver.save_cache(self.cache)


    def open_custom_colors_window(self):
        custom_colors_window = CustomColorsWindow(self.adapter)
        custom_colors_window.start()

        if not self.adapter.ispresent('colorname') : pass
        else:
            colorname = self.adapter.get("colorname")
            red = self.adapter.get("red")
            green = self.adapter.get("green")
            blue = self.adapter.get("blue")
            alpha = self.adapter.get("alpha")
            self.color_cache.insert_cache(colorname, (red, green, blue, alpha))
            #print(self.color_cache.retrieve_cache())


    def refresh(self):
        self.plot_chart(fig_present=True)


    def insert_new_column(self):
        """Inserts a new column into spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        insert_window = InsertWindow(self.adapter, "new_col", title="Insert Column", size=(400,200), _type="column")
        insert_window.start()
        new_col = self.adapter.get("new_col")
        self.df[new_col] = np.array(["" for i in range(0, len(self.df))])
        # Set the newly inserted data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)
        self.choice_is_null = True


    def insert_row(self):
        """Inserts a row into spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        df_cols = self.df.columns.tolist()
        df_dtypes = [self.df[col].dtype for col in self.df]

        insert_window = InsertRowWindow(self.adapter, df_cols, 'Insert Row', size=(400, len(df_cols)*50))
        insert_window.start()

        vals = []
        for row in df_cols:
            vals.append(self.adapter.get(row))
        self.df = self.df.append(pandas.DataFrame([vals], columns=df_cols), ignore_index=True)

        for i in range(0, len(df_cols)):
            self.df[df_cols[i]] = self.df[df_cols[i]].astype(df_dtypes[i])

        df_rows = self.df.to_numpy().tolist()
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


    def delete_column(self):
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        """Deletes a column from spreadsheet."""
        delete_window = InsertWindow(self.adapter, "del_col", title="Delete Column", size=(400,200), _type="column")
        delete_window.start()
        new_col = self.adapter.get("del_col")
        del self.df[new_col]
        # Set the newly modified data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)
        self.choice_is_null = True


    def clear_column(self):
        """Clears the value in a column from spreadsheet."""
        self.df = pandas.DataFrame(self.sheet.get_sheet_data(), columns=self.sheet.headers())
        clear_window = InsertWindow(self.adapter, "clr_col", title="Clear Column", size=(400,200), _type="column")
        clear_window.start()
        new_col = self.adapter.get("clr_col")
        # Clear column
        self.df[new_col] = ['' for i in range(0, len(self.df[new_col]))]
        # Set the newly modified data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


    def detect_collision(self):
        if self.choice_is_null : self.open_column_selection()
        
        sheet_data    = self.sheet.get_sheet_data()
        sheet_headers = self.sheet.headers()
        df = pandas.DataFrame(sheet_data, columns=sheet_headers) 

        if self.xaxis_dtype not in ["Number", "KiloMeter", "Meter"]:
            end_time = []
            df[self.xaxis_column] = pandas.to_datetime(df[self.xaxis_column])
            for i in range(0, len(df)):
                row = df.iloc[i]
                start = row[self.xaxis_column]
                duration = row[self.duration_column]
                end = start + datetime.timedelta(minutes=int(duration))
                end_time.append(end)
            df["end"] = end_time

        elif self.xaxis_dtype in ["Number", "KiloMeter", "Meter"]:
            end_nums = []
            df[self.xaxis_column] = pandas.to_numeric(df[self.xaxis_column])
            for i in range(0, len(df)):
                row = df.iloc[i]
                start = row[self.xaxis_column]
                duration = row[self.duration_column]
                end = self.num_add_duration_to_start(val=start, duration=duration)
                end_nums.append(end)
            df["end"] = end_nums

        detector = CollisionDetector(time_start=df[self.xaxis_column],
                                     time_end=df["end"],
                                     coll_space=df[self.zaxis_column],
                                     coll_obj=df[self.yaxis_column])
        report = detector.detect()
        detector.reset()

        self.report_window = CollisionReport(report, title="Collision Detector Report", size=(750,500), font=self.sheet_font)
        self.report_window.start()


    def detect_intersection(self, xpoint_of_plane: float) -> list:
        """Checks if the cutting plane intersects with any point in cuboid.
            if it intersects then return (x,y,z) co-ordinates.

            Parameters
            ----------
            xpoint_of_plane: float
                x co-ordinate of the cutting plane.
        """
        intersections: list[tuple] = [] # list of intersecting x,y,z co-ordinates.
        for i in range(0, len(self.cubes['start'])):
            start  = self.cubes['start'][i]
            end    = self.cubes['end'][i]
            pointy = self.cubes['y'][i]
            pointz = self.cubes['z'][i]

            if (xpoint_of_plane >= start) and (xpoint_of_plane <= end):
                coords = (xpoint_of_plane, pointy, pointz)
                intersections.append(coords)

        return intersections


    def draw3d_chart(self):
        self.plot_chart(tool="draw")


    def insert_slab(self):
        self.plot_chart(tool="cut")


    def start(self):
        self.mainloop()


if __name__ == "__main__":
    obj = ChartifyAppExtended()
    obj.start()
