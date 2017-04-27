# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 12:57:14 2017

@author: Mark
"""

import pandas as pd
import numpy as np
import shared


def loadData(data_file_name_path):
#Load the data
    loaded_data = pd.read_csv(data_file_name_path)
    return loaded_data


def addColCumulativeDistance(traj):
#Create a column that gives the cumulative distance from the beginning of the test
    triangle_legs = calcTriangleLegs(traj)

    hyps = np.hypot(triangle_legs[:,0], triangle_legs[:,1])
    
    cumul = np.cumsum(hyps)
    cumul = np.concatenate((np.array([0]), cumul), axis=0)
    
    traj_concat = pd.concat([traj, pd.DataFrame({"CumulativeDistance":cumul})], axis=1)
    
    return traj_concat
    
    
def calcTriangleLegs(traj):
#calculate the triangle legs between two points ready to be used to calc hypo
    previous_points = traj[['x_mm','y_mm']].iloc[1:,:].values
    subsequent_points = traj[['x_mm','y_mm']].iloc[0:-1,:].values
    triangle_legs = subsequent_points - previous_points
    return(triangle_legs)
    

def addDistanceCentreCol(df):
#calc distance between all points and the centre
    #calc centre
    x_centre, y_centre = shared.centreArena(df)
    
    #calc median distance to centre
    x_dif_centre = df['x_mm'] - x_centre
    y_dif_centre = df['y_mm'] - y_centre 
    
    #calc distance from centre for each point in segment
    hyps = np.hypot(x_dif_centre, y_dif_centre)
    
    #add to dataframe and return
    df = pd.concat([df, pd.DataFrame({"DistanceCentre":hyps})], axis=1)
    
    return df 
    