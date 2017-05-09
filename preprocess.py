# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 12:57:14 2017

@author: Mark
"""

import pandas as pd
import numpy as np
import shared
import constants
import math

import matplotlib.pyplot as plt
#import plotly.plotly as py

def execute(data_file_name_path):
    df = loadData(data_file_name_path)
    df = addColCumulativeDistance(df)
    df = addDistanceCentreCol(df)    
    df = addDistance(df)
    df = addSpeed(df)
    df = addRotation(df)
    df = addRotationCorrected(df)
    df = addAbsRotationCorrected(df)
    return(df)

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
    subsequent_points = traj[['x_mm','y_mm']].iloc[:-1,:].values
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
    
    return(df)
    
def addDistance(df):
#calc the distance between point and previous point

    distance = df['CumulativeDistance'].iloc[1:].values - df['CumulativeDistance'].iloc[:-1].values
    distance = np.concatenate((np.array([0]), distance), axis=0)
    df = pd.concat([df, pd.DataFrame({"Distance":distance})], axis=1)

    return(df)
    
def addSpeed(df):
#calc the speed between two points

    speed = df['Distance'].iloc[:].values / constants.CONST_TIME_BETWEEN_FRAMES
    df = pd.concat([df, pd.DataFrame({"Speed":speed})], axis=1)
    
    return(df)
    
def addRotation(df):
#calc the amount of rotation between two points

    rotation = df['angle'].iloc[1:].values - df['angle'].iloc[:-1].values
    rotation = np.concatenate((np.array([0]), rotation), axis=0)
    df = pd.concat([df, pd.DataFrame({"Rotation":rotation})], axis=1)

    return(df)
    
#def addAbsRotation(df):
#    #calc the absolute amount of rotation between two points
#
#    abs_rotation = np.abs(df['angle'].iloc[1:].values - df['angle'].iloc[:-1].values)
#    abs_rotation = np.concatenate((np.array([0]), abs_rotation), axis=0)
#    df = pd.concat([df, pd.DataFrame({"AbsRotation":abs_rotation})], axis=1)
#
#    return(df)
    
def addRotationCorrected(df):
    #Correct the rotation for times when going from -pi to +pi or vice versa

    Pos2Neg = df['Rotation']<-4
    Neg2Pos = df['Rotation']>4
    rotation_corrected = df['Rotation'] + Pos2Neg * 2*math.pi  - Neg2Pos * 2*math.pi
    df = pd.concat([df, pd.DataFrame({"Rotation_Corrected":rotation_corrected})], axis=1)
    return(df)
    
def addAbsRotationCorrected(df):
    #calculate absolute rotation

    abs_rotation_corrected = np.abs(df['Rotation_Corrected'])
    df = pd.concat([df, pd.DataFrame({"Abs_Rotation_Corrected":abs_rotation_corrected})], axis=1)

    return(df)