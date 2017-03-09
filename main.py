# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:00:04 2017

@author: Mark
"""
import preprocess

df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df = preprocess.addColCumulativeDistance(df)
df = preprocess.addDistanceCentreCol(df)



