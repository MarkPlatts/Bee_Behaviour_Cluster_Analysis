# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 16:25:05 2017

@author: Mark
"""

import segment as sg
import preprocess
import calc_features
import ellipse_tool as et
import numpy as np

df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")

df = preprocess.addColCumulativeDistance(df)
df = preprocess.addDistanceCentreCol(df)

first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment)

second_segment_length = sg.getSegmentLength(second_segment)

print "second_segment_length =", second_segment_length

P = np.array([second_segment["x"],second_segment["y"]]).T

ellipse_tool = et.EllipseTool()
center, radii, rotation = ellipse_tool.getMinAreaEllipse(P)

area = ellipse_tool.getEllipseArea(radii)

print("Area: ", area)

#focus = 1 - 4A/(pi*d^2)

#ellipse = calc_features.calcIQRange(second_segment, width)