# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:59:35 2017

@author: Mark
"""

import segment as sg
import preprocess
import classArena
import print2csv
import plot_segment as ps
import pandas as pd
import numpy as np
import enums
import filehandling

## plot
#if False:
#    ps.plot_segment(list_segments[14])

   
def createSegments(df, segment_length = 150, overlap = 0.7):
    #generates a list of segments with features for a part of dataset
    
    cum_dist_end_prev = df.iloc[0]['CumulativeDistance']
    temp_segment = sg.Segment(traj = df, lseg = segment_length, ovlp = 0, cum_dist_end_prev = cum_dist_end_prev, arena = arena)
    list_segments = [temp_segment]
    
    iSegment = 0
    while True:
        iSegment = iSegment + 1
        print(iSegment)
        temp_segment = sg.Segment(traj = df, lseg = segment_length, ovlp = overlap, cum_dist_end_prev = temp_segment.last_value_segment, arena = arena)
        list_segments.append(temp_segment)
        #print(temp_segment.getFeature(enums.eFeature.LocationDensity).value)
        if temp_segment.end_of_trajectory: #or iSegment == 2:
            break
    
    return(list_segments)  

def sendSectionDfSegment(df, using_light):
    if using_light: 
        print "using light"
    else: 
        print "no light"
    df_light_selected = df[df['UsingLight'] == using_light]
    list_segments = createSegments(df_light_selected)
    return(list_segments)
    
def createListSegments(df, arena):
    list_segments = []
    
    df = preprocess.addDistanceCentreCol(df, arena)
    #list_segments = list_segments + sendSectionDfSegment(df = df, using_light = False)
    list_segments = list_segments + sendSectionDfSegment(df = df, using_light = True)
    
    return(list_segments)
    
def segmentIndividualFilenames(df, exp_name):
    list_segments = []
    unique_filename = df.filename.unique()
    for iFile in unique_filename:
        print(iFile)
        df_file = df[df['filename'] == iFile]
        df_file.reset_index(drop = True, inplace = True)
        df_file = preprocess.execute(df_file, experiment_name = exp_name)
        temp_list_segments = createListSegments(df = df_file, arena = arena)
        list_segments = list_segments + temp_list_segments
    return list_segments

df_nt = filehandling.loadData(data_file_name_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df_procaine = filehandling.loadData(data_file_name_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_procaine.csv")
df_saline = filehandling.loadData(data_file_name_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_saline.csv")
dfs_combined = pd.concat([df_nt, df_procaine, df_saline], axis=0)
arena = classArena.classArena(dfs_combined)

list_segments = []

print("NT data")
temp_list_segments = segmentIndividualFilenames(df = df_nt, exp_name = "NT")
list_segments = list_segments + temp_list_segments

print("Procaine data")
temp_list_segments = segmentIndividualFilenames(df = df_procaine, exp_name = "Procaine")
list_segments = list_segments + temp_list_segments

print("Saline data")
temp_list_segments = segmentIndividualFilenames(df = df_saline, exp_name = "Saline")
list_segments = list_segments + temp_list_segments

print2csv.output(list_segments)





