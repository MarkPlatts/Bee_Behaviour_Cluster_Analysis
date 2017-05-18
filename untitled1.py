# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:59:35 2017

@author: Mark
"""

import segment as sg
import preprocess
import create_segment as cs
import classArena
import print2csv
import plot_segment as ps
import pandas as pd
import numpy as np

def getSegments(nSegments):
    
    lseg = 100
    ovlp = 0.3
    
    df = preprocess.execute(
    "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
    arena = classArena.classArena(df)
    
    dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, lseg, 0, 0)
    length_segment = cs.getSegmentLength(dt_segment)
    list_segments = [sg.Segment(dt_segment, length_segment, arena, 0)]
    
    for i in range(1,nSegments):
        dt_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, lseg, ovlp, cum_dist_end_segment) 
        length_segment = cs.getSegmentLength(dt_segment)
        list_segments = list_segments + [sg.Segment(dt_segment, length_segment, arena, i)]
        
    return list_segments
    
# calculate segments
if False:
    list_segments = getSegments(20)
    
# write to csv
if False:
    print2csv.output(list_segments)
        
# plot
if False:
    ps.plot_segment(list_segments[14])
    

#load each dataset and chop into lights off part A and lights on part B
def loadData(data_file_name_path):
#Load the data
    loaded_data = pd.read_csv(data_file_name_path)
    return loaded_data
    
df_nt = loadData(
    "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
    
data_frame_name = "NT"

nRecords = df_nt.shape[0]

df_name_vec = [data_frame_name] * nRecords

df_concat = pd.concat([df_nt, pd.DataFrame({"ExperimentName":df_name_vec})], axis=1)
    
#Add label
#    triangle_legs = calcTriangleLegs(traj)
#
#    hyps = np.hypot(triangle_legs[:,0], triangle_legs[:,1])
#    
#    cumul = np.cumsum(hyps)
#    cumul = np.concatenate((np.array([0]), cumul), axis=0)
#    
#    traj_concat = pd.concat([traj, pd.DataFrame({"CumulativeDistance":cumul})], axis=1)
    
df_procaine = loadData(
    "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_procaine.csv")
df_saline = loadData(
    "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_saline.csv")

    

