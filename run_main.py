# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:32:56 2017

@author: Mark
"""

import filehandling
import classArena
import print2csv
import main
import pandas as pd

df_nt = filehandling.loadData(data_file_name_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df_procaine = filehandling.loadData(data_file_name_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_procaine.csv")
df_saline = filehandling.loadData(data_file_name_path = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_saline.csv")
dfs_combined = pd.concat([df_nt, df_procaine, df_saline], axis=0)
arena = classArena.classArena(dfs_combined)

list_segments = []

#print("NT data")
#temp_list_segments = main.segmentIndividualFilenames(df = df_nt, exp_name = "NT", arena = arena)
#list_segments = list_segments + temp_list_segments

print("Procaine data")
temp_list_segments = main.segmentIndividualFilenames(df = df_procaine, exp_name = "Procaine", arena = arena, segment_length = 150, overlap = 0.7)
list_segments = list_segments + temp_list_segments

#print("Saline data")
#temp_list_segments = segmentIndividualFilenames(df = df_saline, exp_name = "Saline", arena = arena)
#list_segments = list_segments + temp_list_segments

filepath = "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/test_removing_duplicates/"

print2csv.output(list_segments, filepath)

print2csv.output_xy(list_segments, filepath)