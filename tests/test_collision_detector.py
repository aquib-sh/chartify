import pandas
import sys

sys.path.append("../")
from chartify.tools.collision_detector import CollisionDetector
from chartify.layouts.collision_report_window import CollisionReport

df = pandas.read_csv(
    r"C:\Users\Aquib\Projects\fiverr-projects\augustino\chartify\requirements\3DCHARTS_ENG_DOCS\table1_short.csv"
)

detector = CollisionDetector(
    time_start=df["Time Start"],
    time_end=df["Time End"],
    coll_space=df["Room"],
    coll_obj=df["Person"],
)

report = detector.detect()
detector.reset()

report_window = CollisionReport(
    report, title="Collision Detector Report", size=(500, 400)
)
report_window.start()
