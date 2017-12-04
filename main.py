# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:59:35 2017

@author: Mark
"""

import segment as sg
import preprocess


## plot
#if False:
#    ps.plot_segment(list_segments[14])

   
def createSegments(df, arena, segment_length, overlap):
    #generates a list of segments with features for a part of dataset
    
    cum_dist_end_prev = df.iloc[0]['CumulativeDistance']
    temp_segment = sg.Segment(traj = df, lseg = segment_length, ovlp = 0, cum_dist_end_prev = cum_dist_end_prev, arena = arena)
    list_segments = [temp_segment]
    
    iSegment = 0
    while True:
        iSegment = iSegment + 1
        print("Segment: ", iSegment)
        temp_segment = sg.Segment(traj = df, lseg = segment_length, ovlp = overlap, cum_dist_end_prev = temp_segment.last_value_segment, arena = arena)
        list_segments.append(temp_segment)
        if temp_segment.end_of_trajectory:
            break
    return(list_segments)  

def sendSectionDfSegment(df, using_light, arena, segment_length, overlap):
    if using_light: 
        print "using light"
    else: 
        print "no light"
    df_light_selected = df[df['UsingLight'] == using_light]
    list_segments = createSegments(df_light_selected, arena = arena, segment_length = segment_length, overlap = overlap)
    return(list_segments)
    
def createListSegments(df, arena, segment_length, overlap):
    list_segments = []
    
    df = preprocess.addDistanceCentreCol(df, arena)
    list_segments = list_segments + sendSectionDfSegment(df = df, using_light = True, arena = arena, segment_length = segment_length, overlap = overlap)
    
    return(list_segments)
    
def segmentIndividualFilenames(df, exp_name, arena, segment_length, overlap):
    list_segments = []
    unique_filename = df.filename.unique()
    for iFile in unique_filename:
        print(iFile)
        df_file = df[df['filename'] == iFile]
        df_file.reset_index(drop = True, inplace = True)
        df_file = preprocess.execute(df_file, experiment_name = exp_name)
        temp_list_segments = createListSegments(df = df_file, arena = arena, segment_length = segment_length, overlap = overlap)
        list_segments = list_segments + temp_list_segments
    return list_segments







