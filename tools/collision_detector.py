# Author: Shaikh Aquib
# Date: June 2021

import pandas
import datetime


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
        self.inconsis = []
        self.collisions = []

        self.time_start = time_start
        self.time_end = time_end
        self.coll_space = coll_space
        self.coll_obj = coll_obj

    def detect(self) -> str:
        """Detects collisions between different objects.

        Returns
        -------
        report:str
            A text report of all the collisions and inconsistencies found.
        """
        report = ""
        inconsis_report = ""
        collision_report = ""
        for i in range(0, len(self.time_start)):
            for j in range(0, len(self.time_start)):

                if (j in self.inconsis or i in self.inconsis) or (
                    (i, j) in self.collisions or (j, i) in self.collisions
                ):
                    continue

                ftime_sta = self.time_start.iloc[i]
                ftime_end = self.time_end.iloc[i]
                froom = self.coll_space.iloc[i]
                fperson = self.coll_obj.iloc[i]

                stime_sta = self.time_start.iloc[j]
                stime_end = self.time_end.iloc[j]
                sroom = self.coll_space.iloc[j]
                sperson = self.coll_obj.iloc[j]

                if ftime_sta > ftime_end:
                    inconsis_report += f"{'====' * 20}\n"
                    inconsis_report += f"Object {fperson} Enters the Space {froom} at {ftime_sta}\n\tand leaves at {ftime_end}\n"
                    inconsis_report += f"{'====' * 20}\n"
                    self.inconsis.append(i)

                else:
                    if stime_sta > stime_end:
                        inconsis_report += f"{'====' * 15}\n"
                        inconsis_report += f"Object {sperson} Enters the Space {sroom} at {stime_sta}\n\tand leaves at {stime_end}\n"
                        inconsis_report += f"{'====' * 15}\n"
                        self.inconsis.append(j)

                    elif (
                        (fperson != sperson)
                        and (froom == sroom)
                        and (stime_sta < ftime_end)
                        and ((stime_end <= ftime_end) and (stime_end > ftime_sta))
                    ):

                        collision_report += f"{'====' * 15}\n"
                        collision_report += f"Object : {fperson}\nStart : {ftime_sta}\nEnd : {ftime_end}\n\n"
                        collision_report += f"Object : {sperson}\nStart : {stime_sta}\nEnd : {stime_end}\n"
                        collision_report += f"{'====' * 15}\n"
                        self.collisions.append((i, j))

        if len(inconsis_report) == 0:
            inconsis_report = "No inconsistencies in data detected."
        if len(collision_report) == 0:
            collision_report = "No collisions in between object detected."

        report += "$$$$" * 16
        report += "\n\t\tCOLLISION DETECTION REPORT\n"
        report += "$$$$" * 16
        report += "\n\n"
        report += f"Collisions:\n\n{collision_report}\n\nInconsistencies:\n\n{inconsis_report}"

        return report

    def reset(self):
        """Deletes all the presents records of inconsistencies
        and collisions from list."""
        self.inconsis = []
        self.collisons = []


class CollisionDetectorExtended:
    """Detects Collisions Between Different Objects in Data.

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe containing all the information.

    xstart : pandas.Series
        column containing start points of x axis.

    xend : pandas.Series
        column containing end points of x axis.

    space : str
        name of the column containing spaces where collision has to be checked.
        (example: rooms, halls, etc)

    obj : str
        name of the column containing objects which will collided
        if collision occurs in space. (example: person, lecturer, etc)

    _type : str
        type of data, 'time' or 'numeric'

    Attributes
    ----------
    inconsis:list
        indexes of rows where inconsistencies exist in data.

    collisions:list[tuple(int, int)]
        indexes co-ordinates of all the collisions occurred so far,
        where (i, j) in tuples represents the indexes of 2 colliding objects.

    """

    def __init__(self, dataframe, xstart, xend, space, obj):
        self.df = dataframe
        self.xstart = xstart
        self.xend = xend
        self.space_col = space
        self.obj_col = obj

    def detect(self):
        collisions = []
        coll_pos = []
        for i in range(0, len(self.xstart)):
            space1 = self.df.loc[i][self.space_col]
            obj1 = self.df.loc[i][self.obj_col]
            start1 = self.xstart.loc[i]
            end1 = self.xend.loc[i]

            for j in range(0, len(self.xend)):
                space2 = self.df.loc[j][self.space_col]
                obj2 = self.df.loc[j][self.obj_col]
                start2 = self.xstart.loc[j]
                end2 = self.xend.loc[j]

                # Skip if already checked
                if (j, i) in coll_pos:
                    continue

                # Collision Type 1
                # When Person A and Person B are both in the same room
                # And if Tstart of Person A is >= Tstart of Person B
                # And Tend of Person A <= Tend of Person B
                # { This means 2 different people were present at
                # the same time on same location }.

                # Collision Type 2
                # When Person A and Person B are same
                # And Room A and Room B are different
                # And Tstart of Person B >= Tstart of Person A
                # And Tend of Person B <= Tend of Person A
                # {This means same person was present on 2 locations }.

                if (
                    (space1 == space2)
                    and (obj1 != obj2)
                    and (start1 >= start2)
                    and (end1 <= end2)
                ) or (
                    (obj1 == obj2)
                    and (space1 != space2)
                    and (start2 >= start1)
                    and (end2 <= end1)
                ):
                    collisions.append(
                        {
                            "object1": obj1,
                            "object2": obj2,
                            "event1": space1,
                            "event2": space2,
                            "start1": start1,
                            "end1": end1,
                            "start2": start2,
                            "end2": end2,
                        }
                    )
                    coll_pos.append((i, j))

        return collisions

    def generate_report(self, collisions: list) -> list:
        report = ""
        report += "$$$$" * 16
        report += "\n\t\tCOLLISION DETECTION REPORT\n"
        report += "$$$$" * 16
        report += "\n\n"

        for collision in collisions:
            report += f"{'====' * 16}\n"
            report += f"Object:{collision['object1']} Event:{collision['event1']} Start:{collision['start1']}  End:{collision['end1']}\n"
            report += f"Object:{collision['object2']} Event:{collision['event2']} Start:{collision['start2']}  End:{collision['end2']}\n"
            report += f"{'====' * 16}\n"

        return report
