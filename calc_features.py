# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:12:31 2017

@author: Mark
"""

import ellipse_tool as et
import segment as sg
import math
import numpy as np



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

def calcFocus(segment):
    
    points = np.array([segment["x"],segment["y"]]).T
    area = areaFormula(points)
    
    seg_length = sg.getSegmentLength(segment)
    focus = 1 - 4*area/(math.pi*seg_length^2)
    return(focus)
    
def calcEccentricity(segment):
    
    
    
    
    
#helper methods
    
def areaFormula(points):
    ellipse_tool = et.EllipseTool()
    center, radii, rotation = ellipse_tool.getMinAreaEllipse(points)
    
    area = radii[0]*radii[1]*math.pi
    return(area)
    
def focusFormula(area, seg_length):
    focus = 1 - 4*area/(math.pi*seg_length^2)
    return(focus)
    