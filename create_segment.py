# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:54:17 2017

@author: Mark
"""

#import numpy as np
#import pandas as pd
#import math
#import pdb
    
def getSegment(traj, lseg, ovlp, cum_dist_end_prev):
    
    #find the beginning of this segment
    if cum_dist_end_prev != 0:
        max_cum_dist_start_second = cum_dist_end_prev - lseg*ovlp
        values_lesser = traj['CumulativeDistance'][traj['CumulativeDistance']<=max_cum_dist_start_second]
        value_just_below = values_lesser.iloc[-1]
        cumdist = traj['CumulativeDistance']
        start_seg_index = cumdist[cumdist==value_just_below].index[0]
    else:
        value_just_below = 0
        start_seg_index = 0
    
    #find the end of this segment
    values_greater = traj['CumulativeDistance'][traj['CumulativeDistance']>=value_just_below+lseg]
    if values_greater.size == 0:
        last_value_segment = None
        segment = traj.loc[start_seg_index:,:].reset_index(drop=True)
        end_of_trajectory = True
    else:
        last_value_segment = values_greater.iloc[0]
        cumdist = traj['CumulativeDistance']
        end_seg_index = cumdist[cumdist==last_value_segment].index[0]
        segment = traj.loc[start_seg_index:end_seg_index,:].reset_index(drop=True)
        end_of_trajectory = False
    
    return segment, last_value_segment, end_of_trajectory
    
def getSegmentLength(segment):
    
    start = segment["CumulativeDistance"].iloc[0]
    end = segment["CumulativeDistance"].iloc[-1]
    
    total_distance = end - start
    
    return total_distance

