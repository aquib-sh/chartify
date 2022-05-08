import re
import numpy as np


class Slab:
    """Inserts slab on specific intevals of an axis
    in 3D Plots.
    """

    def __init__(self, axes):
        self.axes = axes
        self.num_pattern = r"-*(\d+\.?\d*)"

    def extract_num(self, text) -> float:
        """Extracts floating point number from text."""
        r = re.search(self.num_pattern, text)
        extracted = r.group(1)
        is_equal = extracted == text

        return float(extracted) if is_equal else float(extracted) * -1

    def __find_axis_diff__(self, method):
        """Finds the difference between an axis elements."""
        labels = [elem.get_text() for elem in method()]
        first = self.extract_num(labels[0])
        second = self.extract_num(labels[1])
        return second - first

    def __get_label__(self, method, index):
        """Returns the label value for an axis based on index."""
        val = method()[index].get_text()
        return self.extract_num(val)

    def x_diff(self):
        """Finds the difference between X-Axis labels."""
        return self.__find_axis_diff__(method=self.axes.get_xticklabels)

    def y_diff(self):
        """Finds the difference between Y-Axis labels."""
        return self.__find_axis_diff__(method=self.axes.get_yticklabels)

    def z_diff(self):
        """Finds the difference between Z-Axis labels."""
        return self.__find_axis_diff__(method=self.axes.get_zticklabels)

    def get_xlabel(self, index=0):
        """Returns the label on a index for X-Axis"""
        return self.__get_label__(method=self.axes.get_xticklabels, index=index)

    def get_ylabel(self, index=0):
        """Returns the label on a index for Y-Axis"""
        return self.__get_label__(method=self.axes.get_yticklabels, index=index)

    def get_zlabel(self, index=0):
        """Returns the label on a index for Z-Axis"""
        return self.__get_label__(method=self.axes.get_zticklabels, index=index)

    def insert_slab_by_x(self, point: float, **kwargs):
        """Inserts a slab at a specific point on X-axis.

        Parameters
        ----------
        point : float
            point on the X-axis where slab will be inserted.
        """
        xstart = ystart = zstart = None
        xend = yend = zend = None
        xlen = ylen = zlen = None
        xdiff = ydiff = zdiff = lbl_len = None

        if "X" in kwargs and "Y" in kwargs and "Z" in kwargs:
            xstart = kwargs["X"][0]
            ystart = kwargs["Y"][0]
            zstart = kwargs["Z"][0]

            xend = kwargs["X"][-1]
            yend = kwargs["Y"][-1]
            zend = kwargs["Z"][-1]

            xdiff = kwargs["X"][1] - kwargs["X"][0]
            ydiff = kwargs["Y"][1] - kwargs["Y"][0]
            zdiff = kwargs["Z"][1] - kwargs["Z"][0]

            xlen = len(kwargs["X"])
            ylen = len(kwargs["Y"]) + 1
            zlen = len(kwargs["Z"]) + 1

        else:
            xstart = self.get_xlabel()
            ystart = self.get_ylabel()
            zstart = self.get_zlabel()

            xend = self.get_xlabel(index=-1)
            yend = self.get_ylabel(index=-1)
            zend = self.get_zlabel(index=-1)

            xdiff = self.x_diff()
            ydiff = self.y_diff()
            zdiff = self.z_diff()

            xlen = len(self.axes.get_xticklabels())
            ylen = len(self.axes.get_yticklabels())
            zlen = len(self.axes.get_zticklabels())

        X = np.array([[point] * (ylen + 1) for i in range(0, zlen)])
        Y = []
        Z = []

        for i in range(zlen):
            tempy = []
            temp_ystart = ystart
            tempy.append(temp_ystart - 0.1)
            for j in range(0, ylen):
                tempy.append(temp_ystart)
                temp_ystart += ydiff
            Y.append(tempy)
        Y = np.array(Y)

        for i in range(zlen):
            tempz = []
            for j in range(ylen + 1):
                tempz.append(zstart)
            zstart += zdiff
            Z.append(tempz)
        Z = np.array(Z)

        return (X, Y, Z)
