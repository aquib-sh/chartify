import sys
import threading

sys.path.append("../")
from chartify.layouts.chart_window import ChartWindow
from chartify.processors.data_adapter import DataAdapter

adapter = DataAdapter()


def do_stuff():
    w = ChartWindow(adapter, title="Choice of columns for 3D chart", size=(800, 300))
    values = ("First", "Second", "Third", "Fourth")
    w.update_dropdown(values)
    w.start()


do_stuff()
