import sys
from typing import Sized
sys.path.append('../')
from chartify.processors.timeline_mapper import TimelineMapper

timeline = [
    '1/5  7:00', '1/5  11:00', 
    '1/5  15:00', '1/5  19:00', 
    '1/5  23:00', '2/5  3:00', 
    '2/5  7:00',  '2/5  11:00', 
    '2/5  15:00', '2/5  19:00', 
    '2/5  23:00', '3/5  3:00', 
    '3/5  7:00',  '3/5  11:00', 
    '3/5  15:00', '3/5  19:00'
]

points = [
    0,    240,
    480,  720,
    960,  1200,
    1440, 1680,
    1920, 2160,
    2400, 2640,
    2880, 3120,
    3360, 3600
    ]

obj = TimelineMapper(timeline, points)
point = obj.get_point('2/5  11:45')
print(point)

