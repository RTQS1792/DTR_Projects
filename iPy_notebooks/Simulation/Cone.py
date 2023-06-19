'''
Author       : Hanqing Qi
Date         : 2023-06-19 14:15:34
LastEditors  : Hanqing Qi
LastEditTime : 2023-06-19 15:18:16
FilePath     : /Simulation/Cone.py
Description  : This is a class to represent a cone
'''

# Packages
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class Cone:
    def __init__(self, center, radius, starting_angle, end_angle, rotate_speed):
        self.center = center  # center is a tuple (x, y)
        self.radius = radius  # radius is a float
        self.starting_angle = starting_angle  # starting angle is a float in degrees
        self.end_angle = end_angle  # end angle is a float in degrees
        self.rotate_speed = rotate_speed  # rotate speed is a float in degrees per second

    def getCenter(self):
        return self.center

    def getRadius(self):
        return self.radius

    def getStartingAngle(self):
        return self.starting_angle

    def getEndAngle(self):
        return self.end_angle
    
    def getRotateSpeed(self):
        return self.rotate_speed

    def rotate(self, angle):
        self.starting_angle += angle
        self.end_angle += angle
        self.starting_angle = self.starting_angle % 360
        self.end_angle = self.end_angle % 360

    def insight(self, point):
        x = point[0] - self.center[0]
        y = point[1] - self.center[1]
        r = math.sqrt(x**2 + y**2)
        theta = math.degrees(math.atan2(y, x))
        if theta < 0:
            theta += 360

        if (
            r <= self.radius
            and theta >= self.starting_angle
            and theta <= self.end_angle
        ):
            return True
        else:
            return False

    def setCenter(self, center):
        self.center = center

    def setRotateSpeed(self, rotate_speed):
        self.rotate_speed = rotate_speed

    def format_out(self):
        ret = (
            str(self.center)
            + ":"
            + str(self.radius)
            + ":"
            + str(self.starting_angle)
            + ":"
            + str(self.end_angle)
        )
        return ret

    def Draw_Cone(self, ax, my_color):
        wedge = patches.Wedge(
            self.center,
            self.radius,
            self.starting_angle,
            self.end_angle,
            color=my_color,
            alpha=0.5,
        )
        ax.add_patch(wedge)  # add the wedge to the plot
