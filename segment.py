# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:54:17 2017

@author: Mark
"""

import numpy as np
import pandas as pd
import math

    
    
#def CalcDistanceBetweenPoints(p1,p2):
#    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])
#    
#    
#def GetPointFromLine(df, line_number):
#    line = df.iloc[line_number,:]
#    point = [line.x, line.y]
#    return point
    
    
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
    
    #find the beginning of this segment
    values_greater = traj['CumulativeDistance'][traj['CumulativeDistance']>=value_just_below+lseg]
    value_just_above = values_greater.iloc[0]
    cumdist = traj['CumulativeDistance']
    end_seg_index = cumdist[cumdist==value_just_above].index[0]
    
    segment = traj.loc[start_seg_index:end_seg_index,:]
    
    #print(segment)
    
    return segment, value_just_above
        

#def trajectory_segmentation_constant_len( traj, lseg, ovlp, count):
#    # SEGMENT_TRAJECTORY Splits the trajectory in segments of length
#    # lseg with an overlap of ovlp %
#    # Returns an array of instances of the same trajectory class (now repesenting segments)
#    n =traj.shape[0]
#    #n = size(traj, 1);
#    
#
#    # compute cumulative distance vector
#
#    #cumdist = zeros(1, n);   
#    cumdist = np.zeros(n)
#    #print("cumdist:", cumdist) 
#    #print(cumdist.shape)
#    for i in range(1,n+1):
#        print(i)
#        p1 = GetPointFromLine(traj,i-1)
#        p2 = GetPointFromLine(traj,i)
#        distance = CalcDistanceBetweenPoints(p1,p2)
#        cumdist[i] = cumdist[i - 1] + distance        
#        
#    print(cumdist)
#
#    % step size
#    off = lseg*(1. - ovlp);
#    % total number of segments - at least 1
#    if cumdist(end) > lseg                
#        nseg = ceil((cumdist(edistancend) - lseg) / off) + 1;
#        off = off + (cumdist(end) - lseg - off*(nseg - 1))/nseg;
#    else
#        nseg = 1;
#    end
#    % segments are trajectories again -> construct empty object
#    segments = trajectories([]);
#
#    for seg = 0:(nseg - 1)
#        starti = 0;
#        seg_off = 0;
#        pts = [];
#        if nseg == 1
#            % special case: only 1 segment, don't discard it
#            pts = traj.points;
#        else
#            for i = 1:n
#               if cumdist(i) >= seg*off                           
#                   if starti == 0
#                       starti = i;
#                   end
#                   if cumdist(i) > (seg*off + lseg)
#                       % done we are
#                       break;
#                   end
#                   if isempty(pts)
#                       seg_off = cumdist(i);
#                   end
#                   % otherwise append point to segment
#                   pts = [pts; traj.points(i, :)];
#               end
#            end
#        end
#
#        segments = segments.append(...
#            trajectory(pts, traj.session, traj.track, traj.group, traj.id, traj.trial, traj.day, seg + 1, seg_off, starti, traj.trial_type, count)...
#            );
#    end            
#end

#a = LoadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
#
##trajectory_segmentation_constant_len(traj=a, lseg=20, ovlp=0.3, count= 10)
#b = AddColCumulativeDistance(a)
#first_segment, cum_dist_end_segment = GetFirstTrajectory(b, 10, 3)
#GetSecondTrajectory(b, 10, 3, cum_dist_end_segment)