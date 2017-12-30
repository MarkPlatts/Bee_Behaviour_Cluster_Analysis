# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:51:44 2017

@author: Mark
"""

import pandas as pd
import os
from sklearn import preprocessing
from sklearn.cluster import KMeans
import find_n_neighbours as n_neigh
import plot_segment
import matplotlib.pyplot as plt

#functions start ====================================================================

def perform_kmeans(df, n_clusters):
    
    clusterer = KMeans(n_clusters = n_clusters, random_state = 0, max_iter = 1000)
    k_means = clusterer.fit(df_features.iloc[:,4:12])
    
    return(k_means.labels_, k_means.cluster_centers_)
    
def scale_features(x):
    std_scaler = preprocessing.StandardScaler()
    x_scaled = std_scaler.fit_transform(x)
    return(x_scaled)

#functions end ====================================================================

#initialisation start ====================================================================

def load_df_for_arena_dims(path):
    df_nt = pd.read_csv(os.path.join(path, "Data/bee-data_NT.csv"))
    df_procaine = pd.read_csv(os.path.join(path, "Data/bee-data_procaine.csv"))
    df_saline = pd.read_csv(os.path.join(path, "Data/bee-data_saline.csv"))
    x = pd.concat([df_nt, df_procaine, df_saline], axis=0)
    return(x)

root_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/"
seg_length = 200
n_clusters = 5
n_nearest_neighbours = 3
path = os.path.join(root_path, "Data/length" + str(seg_length))

#load data
df_features = pd.read_csv(os.path.join(path, "segment_features.csv"))
df_xy = pd.read_csv(os.path.join(path, "segment_xys.csv"))
df_for_arena_dims = load_df_for_arena_dims(path = root_path)


#initialisation end ====================================================================

#run code start ====================================================================

df_features.iloc[:,4:12] = scale_features(df_features.iloc[:,4:12])

cluster_labels, cluster_centres = perform_kmeans(df = df_features, n_clusters = n_clusters)

#init plotting
plot_index = 0 #this is used to specify position in matrix of plots
plt.figure(1)

for cluster_id in range(0, n_clusters):

    kmean_feature_vals = {'MedianDistanceFromCentre': cluster_centres[cluster_id, 0], 
                          'IQRange': cluster_centres[cluster_id, 1],
                          'Focus': cluster_centres[cluster_id, 2],
                          'Eccentricity': cluster_centres[cluster_id, 3],
                          'InnerRadiusVariation': cluster_centres[cluster_id, 4],
                          'CentralDisplacement': cluster_centres[cluster_id, 5],
                          'PathEfficiency': cluster_centres[cluster_id, 6],
                          'SumAbsoluteAngles': cluster_centres[cluster_id, 7]}
    
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

plt.savefig(os.path.join(root_path, "Cluster_Analysis/", "figs/", "length" + str(seg_length) + ".pdf"))

#run code end ====================================================================
