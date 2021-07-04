import sys
sys.path.append('../')
import threading
import traceback
import numpy as np
import pandas
import tksheet
import tkinter as tk
from tkinter.constants import *
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from chartify import config
from chartify.layouts.frame import WindowFrame
from chartify.layouts.insert_window import InsertWindow
from chartify.layouts.delete_window import DeleteWindow
from chartify.layouts.collision_settings_window import CollisionSettings
from chartify.layouts.collision_report_window import CollisionReport
from chartify.processors.timeline_mapper import TimelineMapper
from chartify.tools.collision_detector import CollisionDetector
from chartify.tools.slab import Slab
from chartify.menus.menubar import MenuBarExtended


class ChartifyAppExtended(tk.Tk):
    def __init__(self):
        super().__init__()

        #plt.style.use("ggplot")
        self.axes = None
        self.X = self.Y = self.Z = None
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
        self.current_file_name = ""

        self.kolumna_sala = 'Sala'
        self.kolumna_profesor = 'Profesor'
        self.kolumna_czas_rozpoczecia='Czas rozpoczęcia'
        self.kolumna_czas_zakonczenia='Czas zakończenia'
        self.kolumna_czas_trwania='Czas trwania (min)'


    def open_file(self):
        file_name = filedialog.askopenfilename(initialdir="/",
                                        title="Open a file",
                                        filetype=( ("csv files", "*.csv"), ("xlsx files", "*.xlsx"),("all files", "*.*")))
        if file_name == '':
            return
    
        current_file_name = file_name
        self.load_file(current_file_name)


    def load_file(self, filename):
        if not filename.lower().endswith(".csv"):
            df = pandas.read_excel(filename, engine='openpyxl')
        else:
            df = pandas.read_csv(filename)

        df_rows = df.to_numpy().tolist()  
        self.sheet.headers(df.columns.tolist())
        self.sheet.set_sheet_data(df_rows)
        self.current_file_name = filename


    def save_file(self):
        if self.current_file_name.lower().endswith(".csv"):
            sheet_data = self.sheet.get_sheet_data()
            sheet_headers = self.sheet.headers()
            df = pandas.DataFrame(sheet_data, columns = sheet_headers) 
            df.to_csv(self.current_file_name, index=False)
        else:
            messagebox.showerror("Error","Save possible only for csv")


    def save_file_as(self):
        file_name = filedialog.asksaveasfilename(initialdir="/",
                                        title="Choose file",
                                        filetype=(("csv files", "*.csv"), ("all files", "*.*")))
    
        if file_name == '':
            return
    
        if not file_name.endswith(".csv"):
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
            ax.plot_surface(x,y,z, color=color)


    def wykres(self, tool="draw"):
        sheet_data    = self.sheet.get_sheet_data()
        sheet_headers = self.sheet.headers()
        df = pandas.DataFrame(sheet_data, columns = sheet_headers) 

        self.okno_wybor_kolumn(list(df.columns))

        df[self.kolumna_czas_rozpoczecia] = pandas.to_datetime(df[self.kolumna_czas_rozpoczecia])
        df[self.kolumna_czas_zakonczenia] = pandas.to_datetime(df[self.kolumna_czas_zakonczenia])
        df[self.kolumna_czas_trwania] = pandas.to_numeric(df[self.kolumna_czas_trwania])

        try:
            df.sort_values(by=[self.kolumna_czas_rozpoczecia],inplace=True)
            
            fig = plt.figure(figsize=(6,6))
            fig.canvas.manager.set_window_title('Schedule')
            ax = fig.add_subplot(projection='3d')
            ax.set_xlabel('Timeline', fontweight ='bold',labelpad=30)
            ax.set_ylabel('Object', fontweight ='bold')
            ax.set_zlabel('Space', fontweight ='bold')

            #okreslamy zakres czasowy 
            minvals = df.min()
            min = minvals[self.kolumna_czas_rozpoczecia] #najwczesniejsza data wśród dat rozpoczęcia
            maxvals = df.max()
            max = maxvals[self.kolumna_czas_zakonczenia] #najpóźniejsza data wśród dat zakończenia
            d = max - min # okres
            
            #ile jest minut od pocztku pierwszego do koca ostatniego wykadu
            dminutes = d.components.days * 24*60 + d.components.hours*60 + d.components.minutes

            ax.set_xlim(0,dminutes)
            czasy_rozpoczecia = []
        
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
                czasy_rozpoczecia.append(str(day)+"/"+str(month) + "  "+str(hour)+":00")

            self.X = np.arange(0,dminutes,odstep_min)
            ax.set_xticks(self.X)
            ax.set_xticklabels(czasy_rozpoczecia, rotation='vertical', fontsize=9)

            #lista osób prowadzacych zajęcia
            profesors = df[self.kolumna_profesor].unique()
            ax.set_ylim(0,len(profesors))
            self.Y = np.arange(0,len(profesors),1)
            ax.set_yticks(self.Y)
            ax.set_yticklabels(profesors, fontsize=10)

            #lista sal
            rooms = df[self.kolumna_sala].unique()
            ax.set_zlim(0,len(rooms))
            self.Z = np.arange(0,len(rooms),1)
            ax.set_zticks(self.Z)
            ax.set_zticklabels(rooms, fontsize=10)

            print("X:")
            print(self.X)
            print("Y:")
            print(self.Y)
            print("Z:")
            print(self.Z)

            self.axes = ax
            colors =['blue','red','green','yellow','orange','violet','peru','pink']

            #losuj pozostale kolory
            for i in range(0,60):
                random_color = list(np.random.random(size=3) ) 
                colors.append(random_color)

            try:
                for index, row in df.iterrows():
                    prof     = row[self.kolumna_profesor]
                    room     = row[self.kolumna_sala]
                    start    = row[self.kolumna_czas_rozpoczecia]
                    duration = row[self.kolumna_czas_trwania]

                    d = start - min
                    startmins = d.components.days * 24*60 + d.components.hours*60 + d.components.minutes

                    y = np.where(profesors == prof)[0][0]

                    z = np.where(rooms == room)[0][0]

                    self.plotCubeAt(pos=(startmins+duration/2,y,z),size=(duration,0.1,0.1),color=colors[y], ax=ax)
                       
                plt.title("Schedule")

                if tool == "draw":
                    plt.show()
                elif tool == "cut":
                    #print(czasy_rozpoczecia)
                    #print(self.X)
                    slaby = Slab(self.axes)
                    modx, mody, modz = slaby.insert_slab_by_x(point=1200, X=self.X, Y=self.Y, Z=self.Z)
                    print("PRINTING RETURNED")
                    print(modx)
                    print(mody)
                    print(modz)
                    self.axes.plot_surface(modx, mody, modz, color="RoyalBlue")
                    plt.show()
        
            except Exception as e:
                messagebox.showerror("Błąd","Bład podczas tworzenia wykresu\r\n"+traceback.format_exc())

        except Exception as e:
            messagebox.showerror("Błąd","Bład w obliczeniach do wykresu\r\n"+traceback.format_exc())


    def okno_wybor_kolumn(self, column_names):
        dlg = tk.Toplevel(master=self, bg='light cyan', pady=0)
        dlg.geometry('750x300+100+100')
        dlg.title("Choice of columns")    
        dlg.transient(self)   
        dlg.grab_set()    

        ypos = 60

        label1 = ttk.Label(dlg, text = "Column Object")
        label1.place(x=40,y=ypos)
        combo1 = ttk.Combobox(dlg)
        combo1.set(column_names[0])
        combo1['values'] = column_names
        combo1.place(x=200,y=ypos)
        ypos +=30

        label2 = ttk.Label(dlg, text = "Column Space")
        label2.place(x=40,y=ypos)
        combo2 = ttk.Combobox(dlg)
        combo2.set(column_names[1])
        combo2['values'] = column_names
        combo2.place(x=200,y=ypos)
        ypos +=30

        label3 = ttk.Label(dlg, text = "Column Startring time")
        label3.place(x=40,y=ypos)
        combo3 = ttk.Combobox(dlg)
        combo3.set(column_names[2])
        combo3['values'] = column_names
        combo3.place(x=200,y=ypos)
        ypos +=30

        label4 = ttk.Label(dlg, text = "Column duration (min)")
        label4.place(x=40,y=ypos)
        combo4 = ttk.Combobox(dlg)
        combo4.set(column_names[3])
        combo4['values'] = column_names
        combo4.place(x=200,y=ypos)
        ypos +=30

        label5 = ttk.Label(dlg, text = "Time of stop")
        label5.place(x=40,y=ypos)
        combo5 = ttk.Combobox(dlg)
        combo5.set(column_names[4])
        combo5['values'] = column_names
        combo5.place(x=200,y=ypos)
        ypos +=30


        def zamknij():
            self.kolumna_profesor = combo1.get()
            self.kolumna_sala = combo2.get()
            self.kolumna_czas_rozpoczecia=combo3.get()
            self.kolumna_czas_trwania=combo4.get()
            self.kolumna_czas_zakonczenia=combo5.get()        
            dlg.destroy()


        btn_ok = ttk.Button(dlg, text = "OK", command = zamknij)
        btn_ok.place(x=140,y=250)

        self.wait_window(dlg) 


    def detect_collision(self):
        sheet_data    = self.sheet.get_sheet_data()
        sheet_headers = self.sheet.headers()
        df = pandas.DataFrame(sheet_data, columns=sheet_headers) 
        self.okno_wybor_kolumn(list(df.columns))

        detector = CollisionDetector(time_start=df[self.kolumna_czas_rozpoczecia],
                                     time_end=df[self.kolumna_czas_zakonczenia],
                                     coll_space=df[self.kolumna_sala],
                                     coll_obj=df[self.kolumna_profesor])
        report = detector.detect()
        detector.reset()

        self.report_window = CollisionReport(report, title="Collision Detector Report", size=(750,500))
        self.report_window.start()


    def draw3d_chart(self):
        self.wykres(tool="draw")


    def insert_slab(self):
        self.wykres(tool="cut")


    def start(self):
        self.mainloop()


if __name__ == "__main__":
    obj = ChartifyAppExtended()
    obj.load_file(r"C:\Users\Aquib\Projects\fiverr-projects\augustino\chartify\requirements\3DCHARTS_ENG_DOCS\table1_short.csv")
    obj.start()