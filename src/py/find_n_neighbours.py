# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 10:29:38 2017

@author: Mark
"""

import pandas as pd
import numpy as np
import os
from sklearn import preprocessing
#import pdb
import plot_segment

def findNNearestNeighbours(df, n_nearest, kmean):
    
    n_obs = df.shape[0]
    list_of_sse = []
    
    for iobs in range(0, n_obs):
        sse = 0.0    
        for feature_name, feature_value in kmean.items():
            #print(feature_name, feature_value)
            df_value = df.iloc[iobs][feature_name]
            kmean_value = feature_value
            sse = sse + (df_value - kmean_value)**2
        list_of_sse.append(sse)
        

    df_sort = df
    df_sort['sse'] = np.asarray(list_of_sse)
    df_sort = df_sort.sort_values('sse')   

    df_top_n_value = df_sort.iloc[0:n_nearest,:]
    
    return(df_top_n_value)
    
# end functions ====================================================================
    
# initialisation start =============================================================

#def run():
#    root_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/"
#    df_features = pd.read_csv(os.path.join(root_path, "Data/length200/segment_features.csv"))
#    df_xy = pd.read_csv(os.path.join(root_path, "Data/length200/segment_xys.csv"))
#    
#    kmean = {'MedianDistanceFromCentre': 0.967625,
#             'IQRange': 0.00807833,
#             'Focus': 0.175651,
#             'Eccentricity': 0.871172,
#             'InnerRadiusVariation': 0.16081,
#             'CentralDisplacement': 0.461083,
#             'PathEfficiency': 0.828459,
#             'SumAbsoluteAngles': 0.0111405}
#             
#    #load all the data to estimate dimensions and position of the arena
#    df_nt = pd.read_csv(os.path.join(root_path, "Data/bee-data_NT.csv"))
#    df_procaine = pd.read_csv(os.path.join(root_path, "Data/bee-data_procaine.csv"))
#    df_saline = pd.read_csv(os.path.join(root_path, "Data/bee-data_saline.csv"))
#    df_for_arena_dims = pd.concat([df_nt, df_procaine, df_saline], axis=0)
#    
#    #standardize (5th to 12th columns)
#    x = df_features.iloc[:,4:12]
#    std_scaler = preprocessing.StandardScaler()
#    x_scaled = std_scaler.fit_transform(x)
#    df_features.iloc[:,4:12] = x_scaled
#
#    # initialisation end ================================================================
#    
#    
#    # run and plot ======================================================================
#
#    temp = findNNearestNeighbours(df_features, 10, kmean)
#    for iseg in temp['SegmentID']:
#        df_xy_temp = df_xy[df_xy['SegmentID'] == iseg]
#        plot_segment.plot_all(df_for_arena_dims, df_xy_temp)
