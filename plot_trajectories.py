# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 08:16:48 2017

@author: Mark
"""

import segment as sg
import matplotlib.pyplot as plt
import math
import pandas as pd
import shared as sh
import preprocess

#def plotTrajectories(segment):
#    
#    #Extract the x and y values for the segment
#    print segment
    
def drawArena():
    

    df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
    df = preprocess.addColCumulativeDistance(df)
    
    #draw approximate circumference
    print("min x:", df[['x']].min())
    print("max x:", df[['x']].max())
    print("min y:", df[['y']].min())
    print("max y:", df[['y']].max())
    print("diff min and max x:", df[['x']].max() - df[['x']].min())
    print("diff min and max y:", df[['y']].max() - df[['y']].min())
    #lets say diameter is rounded up
    height = df[['y']].max() - df[['y']].min()
    width = df[['x']].max() - df[['x']].min()
    centre = sh.centreArena(df)
    print "height:", height, "  width:", width
    #calc x, y as theta goes from 0->360
    
    circumference_x = []
    circumference_y = []
    
    for iDegree in range(1, 360+1):
        a = centre[0]
        b = centre[1]
        radians = iDegree/360.0 * 2 * math.pi
        x = a + width/2.0*math.cos(radians)
        y = b + height/2.0*math.sin(radians)
        circumference_x.append(x) 
        circumference_y.append(y)
        
    plt.plot(circumference_x, circumference_y)
    
drawArena()
    
df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df = preprocess.addColCumulativeDistance(df)

segment, cum_dist_end_segment = sg.getSegment(df, 500, 0, 0)  
plt.plot(segment['x'],segment['y'])

print "cum_dist_end_segment:", cum_dist_end_segment
for iSeg in range(0):
    segment, cum_dist_end_segment = sg.getSegment(df, 500, 0.3, cum_dist_end_segment)
    plt.plot(segment['x'],segment['y'])
    
#print(df.describe())
