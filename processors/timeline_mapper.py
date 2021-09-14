class TimelineMapper:
    """Maps timeline to actual labels on plot."""

    def __init__(self, timeline, ticks):
        self.timeline = timeline
        self.ticks = ticks
        self.map = {}
        self.generate_mappings()

    def dissect_label(self, label) -> tuple:
        """Returns date, hour, minutes info from given label."""
        date = label.split()[0]
        time_parts = label.split()[1].split(":")
        hours = time_parts[0]
        minutes = time_parts[1]

        return (date, int(hours), int(minutes))

    def generate_mappings(self):
        for i in range(0, len(self.timeline)):
            self.map[self.timeline[i]] = self.ticks[i]

    def get_all_dates(self) -> list:
        """Returns all the dates."""
        dates = []
        for i in range(0, len(self.timeline)):
            date, _, _ = self.dissect_label(self.timeline[i])
            dates.append(date)
        return tuple(set(dates))

    def get_point(self, search_time: str) -> int:
        """Returns the axis point for a given time in the timeline.

        Parameters
        ----------
        search_time: str
            Time to search in the mappings for getting axis point.

        """
        stime = self.timeline[0]  # start time of the timeline
        stime_date, stime_hr, stime_min = self.dissect_label(stime)
        search_date, search_hr, search_min = self.dissect_label(search_time)

        map_keys = list(self.map.keys())

        for i in range(0, len(map_keys)):
            map_date, map_hr, map_min = self.dissect_label(map_keys[i])
            if search_date == map_date:
                current_point = int(self.map[map_keys[i]])
                # If the hour and min is same then just return the current point
                # Otherwise calculate the increment in points
                # difference in timeline and map points is 240
                # so 1 point on timeline is equal to 1 min on x-axis timeline
                # we just increment/decreemnt the time with the extra minutes .
                if (search_hr == map_hr) and (search_min == map_min):
                    return current_point
                else:
                    hr_diff = search_hr - map_hr
                    min_diff = search_min - map_min
                    current_point += hr_diff * 60 + min_diff
                    return current_point
