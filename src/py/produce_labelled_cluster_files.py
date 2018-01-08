# -*- coding: utf-8 -*-
"""
Created on Sat Jan 06 13:33:57 2018

@author: Mark
"""

import perform_kmeans as pkm
#import matplotlib.pyplot as plt
import os
import pandas as pd
#import plot_segment
#import find_n_neighbours as n_neigh

def create_file_with_cluster_membership(seg_length, n_clusters, root_path):
    
    path = os.path.join(root_path, "Data/length" + str(seg_length))
    
    df_features = pd.read_csv(os.path.join(path, "segment_features.csv"))
    df_xy = pd.read_csv(os.path.join(path, "segment_xys.csv"))
    
    df_features.iloc[:,4:12] = pkm.scale_features(df_features.iloc[:,4:12])
    
    cluster_labels, cluster_centres = pkm.perform_kmeans(df = df_features.iloc[:,4:12], n_clusters = n_clusters)
    
    s1 = pd.Series(cluster_labels, name = 'Cluster')
    
    df_temp = pd.concat([df_features.iloc[:,0], s1], axis = 1)
    
    
    #use the SegmentID to merge the cluster name to the xy dataframe
    df_xy = pd.merge(df_xy, df_temp, on = 'SegmentID')
    
    df_xy.to_csv(path_or_buf = os.path.join(path, 'segment_xys_with_clust_name_' + str(n_clusters) + '_clusters.csv'))
             
root_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/"

create_file_with_cluster_membership(seg_length = 150, n_clusters = 5, root_path = root_path)