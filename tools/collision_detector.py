# Author: Shaikh Aquib
# Date: June 2021

import pandas

class CollisionDetector:
    """Detects Collisions Between Different Objects in Data.

    Parameters
    ----------
    time_start : pandas.core.series.Series
        Time Start column from data.

    time_end : pandas.core.series.Series
        Time End column from data.

    coll_space : pandas.core.series.Series
        Column of the space where collision has to be checked. (example: rooms, halls, etc)

    coll_obj : pandas.core.series.Series
        Column of objects which will collided if collision occurs in space. (example: person, lecturer, etc)

    Attributes
    ----------
    inconsis:list
        indexes of rows where inconsistencies exist in data.

    collisions:list[tuple(int, int)]
        indexes co-ordinates of all the collisions occurred so far,
        where (i, j) in tuples represents the indexes of 2 colliding objects.

    """
    def __init__(self, time_start, time_end, coll_space, coll_obj):
        self.inconsis  = []
        self.collisions = []

        self.time_start = time_start
        self.time_end   = time_end
        self.coll_space = coll_space
        self.coll_obj   = coll_obj


    def detect(self) -> str:
        """Detects collisions between different objects.

        Returns
        -------
        report:str
            A text report of all the collisions and inconsistencies found.
        """
        report = ""
        inconsis_report  = ""
        collision_report = ""
        for i in range(0, len(self.time_start)):
            for j in range(0, len(self.time_start)):

                if ((j in self.inconsis or i in self.inconsis)
                    or ((i, j) in self.collisions or (j, i) in self.collisions)): continue

                ftime_sta = self.time_start.iloc[i]
                ftime_end = self.time_end.iloc[i]
                froom     = self.coll_space.iloc[i]
                fperson   = self.coll_obj.iloc[i]

                stime_sta = self.time_start.iloc[j]
                stime_end = self.time_end.iloc[j]
                sroom     = self.coll_space.iloc[j]
                sperson   = self.coll_obj.iloc[j]

                if (ftime_sta > ftime_end):
                    inconsis_report += f"{'====' * 20}\n"
                    inconsis_report += f"Object {fperson} Enters the Space {froom} at {ftime_sta}\n\tand leaves at {ftime_end}\n"
                    inconsis_report += f"{'====' * 20}\n"
                    self.inconsis.append(i)

                else:
                    if (stime_sta > stime_end):
                        inconsis_report += f"{'====' * 15}\n"
                        inconsis_report += f"Object {sperson} Enters the Space {sroom} at {stime_sta}\n\tand leaves at {stime_end}\n"
                        inconsis_report += f"{'====' * 15}\n"
                        self.inconsis.append(j)

                    elif ((fperson != sperson)
                          and (froom == sroom)
                          and (stime_sta < ftime_end)
                          and ((stime_end <= ftime_end) and (stime_end > ftime_sta))):

                        collision_report += f"{'====' * 15}\n"
                        collision_report += f"Object : {fperson}\nStart : {ftime_sta}\nEnd : {ftime_end}\n\n"
                        collision_report += f"Object : {sperson}\nStart : {stime_sta}\nEnd : {stime_end}\n"
                        collision_report += f"{'====' * 15}\n"
                        self.collisions.append((i, j))

        if len(inconsis_report) == 0:
            inconsis_report = "No inconsistencies in data detected."
        if len(collision_report) == 0:
            collision_report = "No collisions in between object detected."

        report += "$$$$"*16
        report += "\n\t\tCOLLISION DETECTION REPORT\n"
        report += "$$$$" * 16
        report += "\n\n"
        report += f"Collisions:\n\n{collision_report}\n\nInconsistencies:\n\n{inconsis_report}"

        return report


    def reset(self):
        """Deletes all the presents records of inconsistencies and collisions from list."""
        self.inconsis  = []
        self.collisons = []