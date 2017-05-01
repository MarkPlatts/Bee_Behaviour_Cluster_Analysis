# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:00:04 2017

@author: Mark
"""
import preprocess
import create_segment as cs
import segment as sg
import classArena

#configuration settings
min_segment_length = 500
min_segment_overlap = 0.3 #Specified as a percentage in decimal format
cum_dist_end_segment = 0

#df = preprocess.loadData()
#df = preprocess.addColCumulativeDistance(df)
#df = preprocess.addDistanceCentreCol(df)
df = preprocess.execute("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")

arena = classArena.classArena(df)

dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, min_segment_length, 0, 0)
length_segment = cs.getSegmentLength(dt_segment)
features_segment = sg.Segment(dt_segment, length_segment, arena)

