# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:59:35 2017

@author: Mark
"""

import segment as sg
import preprocess
import print2csv
import os.path#
import logging

## plot
#if False:
#    ps.plot_segment(list_segments[14])

   
def createSegments(df, arena, segment_length, overlap):
    #generates a list of segments with features for a part of dataset
    iSegment = 0
    logging.info("Segment: ", iSegment)
    cum_dist_end_prev = df.iloc[0]['CumulativeDistance']
    temp_segment = sg.Segment(traj = df, lseg = segment_length, ovlp = 0, cum_dist_end_prev = cum_dist_end_prev, arena = arena)
    list_segments = [temp_segment]
    

    while True:
        iSegment = iSegment + 1
        logging.info("Segment: ", iSegment)
        temp_segment = sg.Segment(traj = df, lseg = segment_length, ovlp = overlap, cum_dist_end_prev = temp_segment.last_value_segment, arena = arena)
        list_segments.append(temp_segment)
        if temp_segment.end_of_trajectory:
            break
        if iSegment == 3:
            break
    return(list_segments)  

def sendSectionDfSegment(df, using_light, arena, segment_length, overlap):
    if using_light: 
        logging.info("using light")
    else: 
        logging.info("no light")
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
        logging.info("Filename: ", iFile)
        df_file = df[df['filename'] == iFile]
        df_file.reset_index(drop = True, inplace = True)
        df_file = preprocess.execute(df_file, experiment_name = exp_name)
        temp_list_segments = createListSegments(df = df_file, arena = arena, segment_length = segment_length, overlap = overlap)
        list_segments = list_segments + temp_list_segments
        break
    return list_segments

def process_df(experiment_name, df_input, filepath, arena, segment_length, overlap):
    logging.info("Experiment Name: " + experiment_name)
    temp_list_segments = segmentIndividualFilenames(df = df_input, exp_name = experiment_name, arena = arena, segment_length = segment_length, overlap = overlap)
    #list_segments = list_segments + temp_list_segments
    print2csv.output(temp_list_segments, filepath)
    print2csv.output_xy(temp_list_segments, filepath)
    
def process_all_dfs(data_nt, data_procaine, data_saline, data_folder_path, folder_name,
                    seg_length, overlap, arena):
    logging.info("Running for seg_length: " + str(seg_length) + "   Overlap: " + str(overlap))
    path_folder_to_save = os.path.join(data_folder_path, folder_name)
    if not os.path.exists(path_folder_to_save):
        os.makedirs(path_folder_to_save)        
       
    process_df("NT", data_nt, path_folder_to_save, arena, seg_length, overlap = overlap)
    process_df("Procaine", data_procaine, path_folder_to_save, arena, seg_length, overlap = overlap)
    process_df("Saline", data_saline, path_folder_to_save, arena, seg_length, overlap = overlap)






