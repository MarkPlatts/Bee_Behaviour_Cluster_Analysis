# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 08:16:48 2017

@author: Mark
"""

import segment as sg
import matplotlib.pyplot as plt
import math
import pandas as pd

#def plotTrajectories(segment):
#    
#    #Extract the x and y values for the segment
#    print segment
    


df = sg.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df = sg.addColCumulativeDistance(df)

#draw approximate circumference
print("min x:", df[['x']].min())
print("max x:", df[['x']].max())
print("min y:", df[['y']].min())
print("max y:", df[['y']].max())
print("diff min and max x:", df[['x']].max() - df[['x']].min())
print("diff min and max y:", df[['y']].max() - df[['y']].min())
#lets say diameter is rounded up
diameter = math.ceil(df[['y']].max() - df[['y']].min())
print("diameter:", diameter)
radius = diameter/2
centre = [df[['x']].max() - radius, df[['y']].max() - radius]
print centre[1]
#calc x, y as theta goes from 0->360

circumference_x = []
circumference_y = []

for iDegree in range(1, 360+1):
    a = centre[0]
    b = centre[1]
    radians = iDegree/360.0 * 2 * math.pi
    x = a + radius * math.cos(radians)
    y = b + radius * math.sin(radians)
    circumference_x.append(x) 
    circumference_y.append(y)
    
plt.plot(circumference_x, circumference_y)

first_segment, cum_dist_end_segment = sg.getSegment(df, 500, 0, 0)  
plt.plot(first_segment['x'],first_segment['y'])

print "cum_dist_end_segment:", cum_dist_end_segment
second_segment, cum_dist_end_segment = sg.getSegment(df, 500, 0.3, 500.3)
plt.plot(second_segment['x'],second_segment['y'])
