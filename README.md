# Chartify
## Draws 3D graphs based on 4 data points taken from a CSV or XLSX file. 
![plain figure](https://imgur.com/a/IXFshrK)
#### x-start, x-duration, y, z

## Features:
- Import, Edit and Export CSV, Excel sheets in the application.
![sheet](https://imgur.com/WwNrOdI)
- Copy paste, Cut data into cells.
- Insert, Delete, Clear rows and columns.
- Create multiple 3D charts based on Timedata and Numerical data by selecting different columns.
- Cut the chart on a specific point on X axis, auxillary lines are drawn showing the position of the intersection with a plane cutting the chart and diamond shaped marker on the point of intersection.
![cut chart](https://imgur.com/a/29aWnw8)
- Detect if there is a collision in data, that if two objects collide with their timeline.
- Customize the application by changing fonts, colors, line colors, chart colors, font sizes, etc from Settings menu.
![settings](https://imgur.com/a/QkJKWBm)
![after applying settings](https://imgur.com/a/LbhyK2L)

## Installation

### Running executable binary
Download the zip containing .exe file from release
click on chartify_app.exe to run the application.

### Running from source:
You will need Python version > 3.8
Download Python3.9 from https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
Note: Python 3.9.6 was used to write and test this application.
```
pip install numpy pandas matplotlib tksheet openpyxl
```
To run:
```
python chartify_app.py
```

