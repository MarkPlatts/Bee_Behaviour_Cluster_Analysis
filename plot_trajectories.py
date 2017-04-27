# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 08:16:48 2017

@author: Mark
"""

import create_segment as cs
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
    df = preprocess.addDistanceCentreCol(df)
    
    #draw approximate circumference
#    print("min x:", df[['x']].min())
#    print("max x:", df[['x']].max())
#    print("min y:", df[['y']].min())
#    print("max y:", df[['y']].max())
#    print("diff min and max x:", df[['x']].max() - df[['x']].min())
#    print("diff min and max y:", df[['y']].max() - df[['y']].min())
    #lets say diameter is rounded up
    height = df[['y']].max() - df[['y']].min()
    width = df[['x']].max() - df[['x']].min()
    centre = sh.centreArena(df)
    #print "height:", height, "  width:", width
    #calc x, y as theta goes from 0->360
    
    circumference_x = []
    circumference_y = []
    
    for iDegree in range(1, 360+1):
        a = centre[0]
        b = centre[1]
        radians = iDegree/360.0 * 2 * math.pi
        x = a + width.iloc[0]/2.0*math.cos(radians)
        y = b + height.iloc[0]/2.0*math.sin(radians)
        circumference_x.append(x) 
        circumference_y.append(y)
        
    plt.plot(circumference_x, circumference_y)
    

length_of_segment=100
overlap=0.3
cum_dist_end_prev = 600
    
drawArena()

    
df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df = preprocess.addColCumulativeDistance(df)
df = preprocess.addDistanceCentreCol(df)

width = df[['x_mm']].max() - df[['x_mm']].min()
height = df[['y_mm']].max() - df[['y_mm']].min()
arena_diameter = max(width.iloc[0], height.iloc[0])

arena_centre_x = (df[['x_mm']].max() + df[['x_mm']].min())/2
arena_centre_y = (df[['y_mm']].max() + df[['y_mm']].min())/2

                                                            #(traj, lseg, ovlp, cum_dist_end_prev)
segment, cum_dist_end_segment, end_of_trajectory = cs.getSegment(df, length_of_segment, overlap, cum_dist_end_prev)  
plt.plot(segment['x_mm'],segment['y_mm'])

length_segment = cs.getSegmentLength(segment)
seg2 = sg.Segment(segment, length_segment, arena_diameter, arena_centre_x, arena_centre_y)

#print "cum_dist_end_segment:", cum_dist_end_segment
#for iSeg in range(0):
#    segment, cum_dist_end_segment, end_of_trajectory = cs.getSegment(df, length_of_segment, overlap, 300)
#    plt.plot(segment['x'],segment['y'])
    
#print(df.describe())
