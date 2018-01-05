# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 08:33:59 2017

@author: Mark
"""

#initialisation start ====================================================================

import perform_kmeans as pkm
import matplotlib.pyplot as plt
import os
import pandas as pd
import plot_segment
import find_n_neighbours as n_neigh

#root_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/"
#seg_length = 150
#n_clusters = 5
#n_nearest_neighbours = 6

def plot_n_nearest(seg_length, n_clusters, n_nearest_neighbours, root_path):
    
    #plt.rcParams['figure.figsize'] = [8.0, 4.0]
    
    path = os.path.join(root_path, "Data/length" + str(seg_length))
    
    #load data
    df_features = pd.read_csv(os.path.join(path, "segment_features.csv"))
    df_xy = pd.read_csv(os.path.join(path, "segment_xys.csv"))
    df_for_arena_dims = plot_segment.load_df_for_arena_dims(path = root_path)
    
    df_features.iloc[:,4:12] = pkm.scale_features(df_features.iloc[:,4:12])
    
    cluster_labels, cluster_centres = pkm.perform_kmeans(df = df_features.iloc[:,4:12], n_clusters = n_clusters)
    
    #init plotting
    plot_index = 0 #this is used to specify position in matrix of plots
    #plt.figure(1, figsize=(10,20))
    
    for cluster_id in range(0, n_clusters):
    
        kmean_feature_vals = {'MedianDistanceFromCentre': cluster_centres[cluster_id, 0], 
                              'IQRange': cluster_centres[cluster_id, 1],
                              'Focus': cluster_centres[cluster_id, 2],
                              'Eccentricity': cluster_centres[cluster_id, 3],
                              'InnerRadiusVariation': cluster_centres[cluster_id, 4],
                              'CentralDisplacement': cluster_centres[cluster_id, 5],
                              'PathEfficiency': cluster_centres[cluster_id, 6],
                              'SumAbsoluteAngles': cluster_centres[cluster_id, 7]}
                              
        #print("cluster_id: " + str(cluster_id))
        #print("feature values: ", kmean_feature_vals)
        
        temp = n_neigh.findNNearestNeighbours(df_features, n_nearest_neighbours, kmean_feature_vals)
        
        for iseg in temp['SegmentID']:
            df_xy_temp = df_xy[df_xy['SegmentID'] == iseg]
            plot_index = plot_index + 1
            plot_title = "ClusterID: " + str(cluster_id)
            plot_segment.plot_all(df_plot_arena = df_for_arena_dims,
                                  seg = df_xy_temp,
                                  index = plot_index,
                                  n_rows = n_clusters,
                                  n_cols = n_nearest_neighbours,
                                  title = plot_title)
    
    #plt.savefig(os.path.join(root_path, "Cluster_Analysis/", "figs/", "length" + str(seg_length) + "-clusters" + str(n_clusters) + ".pdf"))