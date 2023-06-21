import networkx as nx
import numpy as np

class Agent:
    def __init__(self, Center, ID, Radius, Angle_1, Angle_2):
        self.Center = Center
        self.ID = ID
        self.Radius = Radius
        self.Angle_1 = Angle_1
        self.Angle_2 = Angle_2

    def Rotation(self, Degree):
        self.Angle_1 = (self.Angle_1 + Degree) % 360
        self.Angle_2 = (self.Angle_2 + Degree) % 360        

    def output(self):
        String_out = str(self.Center) + " " + str(self.ID) + " " + str(self.Radius) + " " + str(self.Angle_1) + " " + str(self.Angle_2)
        return String_out

    def print_info(self):
        print("Agent ID: ", self.ID)
        print("Agent Center: ", self.Center)
        print("Agent Radius: ", self.Radius)
        print("Agent Angle 1: ", self.Angle_1)
        print("Agent Angle 2: ", self.Angle_2)
