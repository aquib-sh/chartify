import os
import sys
from numpy.core.fromnumeric import size
from numpy.lib.function_base import insert
sys.path.append('../')
import datetime
import traceback
import numpy as np
import pandas
import tksheet
import config
import tkinter as tk
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
        self.base_file = None
        self.axes = None
        self.fig  = None
        self.fig_bg = None
        self.df = None
        self.sheet_font  = None
        self.sheet_fsize = None
        self.yaxis_min = None
        self.zaxis_min = None
        self.xaxis_min = None
        self.yaxis_max = None
        self.zaxis_max = None
        self.xaxis_max = None
        self.cache = {'fig_bg':None, 'sheet_font':None, 'sheet_fsize':None}
        self.saver = CacheSaver()
        self.color_cache = CacheProcessor("colors.db", "colors")
        self.retriever = CacheRetriever()

        if self.retriever.cache_exists():
            self.cache = self.retriever.retrieve_cache()
            if self.cache['fig_bg'] != None and len(self.cache['fig_bg']) > 0: 
                self.fig_bg = self.cache['fig_bg']
            
            if self.cache['sheet_font'] != None and len(self.cache['sheet_font']) > 0: 
                self.sheet_font = self.cache['sheet_font']
            
            if self.cache['sheet_fsize'] != None: 
                self.sheet_fsize = self.cache['sheet_fsize']

        self.adapter = DataAdapter()
        self.X = self.Y = self.Z = None
        self.choice_is_null = True
        self.geometry('1000x600+50+50')
        self.pack_propagate(0)

        self.menubar = MenuBarExtended(self)
        self.sheet_frame = WindowFrame(self, width=config.sheetf_width, height=config.sheetf_height)

        self.config(menu=self.menubar)

        self.sheet = tksheet.Sheet(self.sheet_frame)
        self.sheet_frame.place(width=config.sheetf_width, 
            height=config.sheetf_height,
            x=config.sheetf_coords[0], 
            y=config.sheetf_coords[1])

        self.sheet.enable_bindings(("all"))
        self.sheet.pack(expand=True,fill='both')
        if self.sheet_font:
            styler = ChartifyStyler(self, self.sheet, figure=self.fig)
            styler.set_sheet_font(self.sheet_font)

        self.current_file_name = ""

        self.zaxis_column = 'Sala'
        self.yaxis_column = 'Profesor'
        self.xaxis_column='Czas rozpoczęcia'
        self.end_column='Czas zakończenia'
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
        file_name = filedialog.askopenfilename(initialdir="/",
                                        title="Open a file",
                                        filetype=( ("csv files", "*.csv"), ("xlsx files", "*.xlsx"),("all files", "*.*")))
        if file_name == '':
            return
    
        current_file_name = file_name
        self.load_file(current_file_name)
        self.choice_is_null = True


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
            print(color)
            ax.plot_surface(x,y,z, color=color)


    def plot_chart(self, tool="draw", fig_present=False):
        sheet_data    = self.sheet.get_sheet_data()
        sheet_headers = self.sheet.headers()
        df = pandas.DataFrame(sheet_data, columns = sheet_headers) 

        # Open column choice window only if it hasn't been chosen already.
        if self.choice_is_null : self.open_column_selection()
        df[self.duration_column] = pandas.to_numeric(df[self.duration_column])

        try:
            if not fig_present:
                fig = plt.figure(figsize=(6,6))
                self.fig = fig

                self.fig.canvas.manager.set_window_title(self.base_file)
                ax = fig.add_subplot(projection='3d')
                self.axes = ax

            ax = self.axes

            ax.set_xlabel(self.xaxis_column, fontweight ='bold',labelpad=30)
            ax.set_ylabel(self.yaxis_column, fontweight ='bold')
            ax.set_zlabel(self.zaxis_column, fontweight ='bold')

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
                    max = pandas.to_datetime(self.xaxis_max)+datetime.timedelta(minutes=int(maxvals[self.duration_column]))
                else:
                    max = maxvals[self.xaxis_column]+datetime.timedelta(minutes=int(maxvals[self.duration_column]))
                
                # If date
                d = max - min # okres

                #ile jest minut od pocztku pierwszego do koca ostatniego wykadu
                dminutes = d.components.days * 24*60 + d.components.hours*60 + d.components.minutes

                ax.set_xlim(0,dminutes)
                start_times = []

                odstep_min = 60
                if dminutes > 2000:
                    odstep_min = 120
                if dminutes > 3000:
                    odstep_min = 240

                for m in range(0,dminutes,odstep_min):
                    hour = int(min.hour + m/60 ) % 24
                    ddd = min.hour*60 + min.minute + m
                    day = int(min.day + ddd/60/24 )
                    month = min.month
                    start_times.append(str(day)+"/"+str(month) + "  "+str(hour)+":00")

                self.X = np.arange(0,dminutes,odstep_min)
                ax.set_xticks(self.X)
                ax.set_xticklabels(start_times, rotation='vertical', fontsize=9)

                #lista osób prowadzacych zajęcia
                profesors = df[self.yaxis_column].unique()

                if self.yaxis_min != None and self.yaxis_max != None:
                     profesors = [prof for prof in profesors if (prof >= self.yaxis_min) and (prof <= self.yaxis_max)]

                ax.set_ylim(0,len(profesors))
                self.Y = np.arange(0,len(profesors),1)
                ax.set_yticks(self.Y)
                ax.set_yticklabels(profesors, fontsize=10)

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
                        startmins = d.components.days * 24*60 + d.components.hours*60 + d.components.minutes

                        y = np.where(np.array(profesors) == prof)[0][0]
                        z = np.where(np.array(rooms) == room)[0][0]
                        self.plotCubeAt(pos=(startmins+duration/2,y,z),size=(duration,0.1,0.1),color=self.colors[y], ax=ax)
                        
                    plt.title("Schedule")
                    if self.fig_bg : self.fig.patch.set_facecolor(self.fig_bg)

                    if tool == "draw":
                        plt.show()
                    elif tool == "cut":
                        tmap = TimelineMapper(start_times, self.X)
                        dates = tmap.get_all_dates()
                        
                        settings = CutChartSettings(self.adapter, dates)
                        settings.start()
                        selected_date = self.adapter.get('cut-chart-setting-date')
                        selected_time = self.adapter.get('cut-chart-setting-time')

                        point = tmap.get_point(f"{selected_date} {selected_time}")
                        slaby = Slab(self.axes)
                        modx, mody, modz = slaby.insert_slab_by_x(point=point, X=self.X, Y=self.Y, Z=self.Z)
                        self.axes.plot_surface(modx, mody, modz, color="red", alpha=0.4)

                        if fig_present : plt.draw()
                        else : plt.show()
            
                except Exception as e:
                    messagebox.showerror("Błąd","Bład podczas tworzenia plot_chartu\r\n"+traceback.format_exc())


            elif dtype_xaxis in ['float64', 'int64']:

                df.sort_values(by=[self.xaxis_column],inplace=True)
                #okreslamy zakres czasowy 
                minvals = df.min()
                maxvals = df.max()

                if self.xaxis_min : min = float(self.xaxis_min)
                else : min = 0

                if self.xaxis_max : max = float(self.xaxis_max) + maxvals[self.duration_column]/1000
                else : max = maxvals[self.xaxis_column] + maxvals[self.duration_column]/1000

                self.X = []
                for i in range(int(min), int(max), 5):
                    self.X.append(i)

                self.X = np.array(self.X)
            
                ax.set_xticks(self.X)
                ax.set_xticklabels(self.X, rotation='vertical', fontsize=9)
                ax.set_xlim(0, int(max))

                #lista osób prowadzacych zajęcia
                profesors = df[self.yaxis_column].unique()

                if self.yaxis_min != None and self.yaxis_max != None:
                     profesors = [prof for prof in profesors if (prof >= self.yaxis_min) and (prof <= self.yaxis_max)]

                ax.set_ylim(0,len(profesors))
                self.Y = np.arange(0,len(profesors),1)
                ax.set_yticks(self.Y)
                ax.set_yticklabels(profesors, fontsize=10)

                #lista sal
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
                            and (float(start) < float(self.xaxis_min) or (float(start) > float(self.xaxis_max)))
                            )

                            or

                            ((self.zaxis_min != None and self.zaxis_max != None) 
                            and ((room < self.zaxis_min) or (room > self.zaxis_max))
                            )
                            ) : continue
                        
                        _y = np.where(np.array(profesors) == prof)[0]

                        _z = np.where(np.array(rooms) == room)[0]

                        if len(_y) == 0 or len(_z) == 0 : continue

                        y = _y[0]
                        z = _z[0]
                        plot_pos = (start+(duration/1000),y,z)

                        self.plotCubeAt(pos=plot_pos,size=(duration/1000,0.1,0.1),color=self.colors[y], ax=ax)
                        
                    plt.title("Schedule")
                    if self.fig_bg : self.fig.patch.set_facecolor(self.fig_bg)

                    if tool == "draw":
                        plt.show()

                    elif tool == "cut":
                        settings = CutChartNumericalSettings(self.adapter)
                        settings.start()
                        xpoint = float(self.adapter.get('cut-chart-setting-point'))

                        slaby = Slab(self.axes)
                        modx, mody, modz = slaby.insert_slab_by_x(point=xpoint, X=self.X, Y=self.Y, Z=self.Z)
                        self.axes.plot_surface(modx, mody, modz, color="cyan", alpha=0.4)
            
                        if fig_present : plt.draw()
                        else : plt.show()
            
                except Exception as e:
                    messagebox.showerror("Error "," Error while creating the chart \r\n"+traceback.format_exc())

        except Exception as e:
            messagebox.showerror("Error", "Error in calculations for the graph \r \n"+traceback.format_exc())

        self.yaxis_min = None
        self.zaxis_min = None
        self.xaxis_min = None
        self.yaxis_max = None
        self.zaxis_max = None
        self.xaxis_max = None


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

        print(self.adapter)

        tbl_font  = self.adapter.get("table-font")
        tbl_fsize = self.adapter.get("table-font-size")
        graph_bg  = self.adapter.get("graph-background")

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
            print(self.color_cache.retrieve_cache())

    def refresh(self):
        self.plot_chart(fig_present=True)


    def insert_new_column(self):
        """Inserts a new column into spreadsheet."""
        insert_window = InsertWindow(self.adapter, "new_col", title="Insert Column", size=(400,200), _type="column")
        insert_window.start()
        new_col = self.adapter.get("new_col")
        self.df[new_col] = np.array(["" for i in range(0, len(self.df))])
        # Set the newly inserted data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)


    def insert_row(self):
        """Inserts a row into spreadsheet."""
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
        """Deletes a column from spreadsheet."""
        delete_window = InsertWindow(self.adapter, "del_col", title="Delete Column", size=(400,200), _type="column")
        delete_window.start()
        new_col = self.adapter.get("del_col")
        del self.df[new_col]
        # Set the newly modified data.
        df_rows = self.df.to_numpy().tolist()  
        self.sheet.headers(self.df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)
        

    def detect_collision(self):
        sheet_data    = self.sheet.get_sheet_data()
        sheet_headers = self.sheet.headers()
        df = pandas.DataFrame(sheet_data, columns=sheet_headers) 
        self.open_column_selection(list(df.columns))

        detector = CollisionDetector(time_start=df[self.xaxis_column],
                                     time_end=df[self.end_column],
                                     coll_space=df[self.zaxis_column],
                                     coll_obj=df[self.yaxis_column])
        report = detector.detect()
        detector.reset()

        self.report_window = CollisionReport(report, title="Collision Detector Report", size=(750,500))
        self.report_window.start()


    def draw3d_chart(self):
        self.plot_chart(tool="draw")


    def insert_slab(self):
        self.plot_chart(tool="cut")


    def start(self):
        self.mainloop()


if __name__ == "__main__":
    obj = ChartifyAppExtended()
    obj.load_file(r"C:\Users\Aquib\Projects\fiverr-projects\augustino\chartify\requirements\3DCHARTS_ENG_DOCS\time_and_distnace14V.csv")
    obj.start()