# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:12:31 2017

@author: Mark
"""

import shared as sh
import segment as sg
import numpy as np
import pandas as pd

df = sg.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
df = sg.addColCumulativeDistance(df)

#calc centre
x_centre, y_centre = sh.centreArena(df)

#calc median distance to centre
x_dif_centre = df['x'] - x_centre
y_dif_centre = df['y'] - y_centre

#Get a segment
segment, cum_dist_end_segment = sg.getSegment(df, 500, 0, 0) 

#calc distance from centre for each point in segment

hyps = np.hypot(x_dif_centre, y_dif_centre)

df = pd.concat([df, pd.DataFrame({"DistanceCentre":hyps})], axis=1)

print(df)

#calc median distance from centre for all points

#divide it by the width/2

