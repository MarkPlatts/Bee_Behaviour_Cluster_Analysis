# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:12:31 2017

@author: Mark
"""

def calcMedianDistanceFromCentre(segment, diameter):
    
    median = segment["DistanceCentre"].median()/(diameter/2.0)
    median = median.iloc[0]
    return median
    
    
    
def calcIQRange(segment, diameter):
    
    LQ = segment["DistanceCentre"].quantile(0.25)
    UQ = segment["DistanceCentre"].quantile(0.75)
    IQRange = (UQ - LQ)/(diameter/2.0)
    IQRange = IQRange.iloc[0]
    return(IQRange)


