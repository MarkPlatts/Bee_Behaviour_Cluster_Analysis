# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:00:04 2017

@author: Mark
"""
import preprocess
import create_segment as cs
import segment as sg

#configuration settings
min_segment_length = 500
min_segment_overlap = 0.3 #Specified as a percentage in decimal format
cum_dist_end_segment = 0

df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df = preprocess.addColCumulativeDistance(df)
df = preprocess.addDistanceCentreCol(df)

width = df[['x_mm']].max() - df[['x_mm']].min()
height = df[['y_mm']].max() - df[['y_mm']].min()
arena_diameter = max(width.iloc[0], height.iloc[0])

arena_centre_x = (df[['x_mm']].max() + df[['x_mm']].min())/2
arena_centre_y = (df[['y_mm']].max() + df[['y_mm']].min())/2


dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, min_segment_length, 0, 0)
length_segment = cs.getSegmentLength(dt_segment)
features_segment = sg.Segment(dt_segment, length_segment, arena_diameter, arena_centre_x, arena_centre_y)

