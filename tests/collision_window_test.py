import sys
import threading
sys.path.append("../")
from chartify.layouts.collision_settings_window import CollisionSettings
from chartify.layouts.collsion_report_window
from chartify.processors.data_adapter import DataAdapter

adapter = DataAdapter()

def do_stuff():
    w = CollisionSettings(adapter, title="Collision Detector Settings", size=(800,300))
    values = ('First', 'Second', 'Third', 'Fourth')
    w.update_dropdown(values)
    w.start()

do_stuff()