# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 19:52:50 2017

@author: Mark
"""
import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans

#np.set_printoptions(threshold=np.inf)

root_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/"

segment_lengths    = [50,100,150,200,250,300]
number_of_clusters = range(2,11)

#for testing purposes
segment_lengths = 100
number_of_clusters = 2

df_features = pd.read_csv(os.path.join(root_path, "Data/length" + str(segment_lengths) + "/segment_features.csv"))
df_xys      = pd.read_csv(os.path.join(root_path, "Data/length" + str(segment_lengths) + "/segment_xys.csv"))

numpy_features = df_features.iloc[:,4:12].values
#fit kmeans

kmeans = KMeans(n_clusters = 2, random_state = 0).fit(numpy_features)

print kmeans.labels_

#perform voting for each x,y coordinate's cluster membership


#for each new segment calculate the features


#calculate the silhouette score





#select a length of segment
#for iseg_length in segment_lengths:
#  
#  #load data
#  #list.files(here("..", "Data", str_c("length", iseg_length)))
#  df = pd.read_csv(os.path.join(root_path, "Data/"))
#  
#  #select how many clusters
#  for(inum_clusters in number_of_clusters){
#    

#    
#    
#  }
#
#}
#repeat the above and determine the length of segment and number of clusters with the optimum silhouette score
