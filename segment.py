# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:12:31 2017

@author: Mark
"""


import ellipse_tool as et
import math
import numpy as np
import feature
import enums


class Segment:


    #Constructor methods =======================================================================================

    def __init__(self, segment_data, seg_length, arena, index):
        
        self.index = index
        
        #output - features
        self.features = None
        
        #input
        self.segment_length = seg_length
        self.segment_data = segment_data
        self.arena = arena
        
        #segment info
        self.points = None
        self.ellipse = None
        self.min_enclosing_ellipse_area = None
        self.min_enclosing_ellipse_area = None
        self.ellipse_a_axis = None
        self.ellipse_b_axis = None
        
        #calculations
        self.calcFeatures()    
        
    #helper methods =======================================================================================
                
    def findMinEnclosingEllipse(self, points):
        ellipse = et.EllipseTool()
        ellipse.calcMinAreaEllipse(points)
        return(ellipse)
        
    def calcMinEnclosingEllipseArea(self, radii):
        return(radii[0] * radii[1]*math.pi)
        
    def calcAxisMinEnclosingEllipse(self, radii):
        return(max(radii), min(radii))
        
    def extractPointsFromDataTable(self):
        return(np.array([self.segment_data["x_mm"],self.segment_data["y_mm"]]).T) 
        
    def getFeature(self, eFeature):
        return(self.features[eFeature])
        
    #main routine that is called when segment is constructed==============================================
        
    def calcFeatures(self):         
        
        self.points = self.extractPointsFromDataTable()
        self.ellipse = self.findMinEnclosingEllipse(self.points)
        self.min_enclosing_ellipse_area = self.calcMinEnclosingEllipseArea(self.ellipse.radii)
        self.ellipse_a_axis, self.ellipse_b_axis = self.calcAxisMinEnclosingEllipse(self.ellipse.radii)
        
        self.features = [feature.MedianDistanceFromCentre(self, enums.eFeature.MedianDistanceFromCentre),
                         feature.IQRange(self, enums.eFeature.IQRange),
                         feature.Focus(self, enums.eFeature.Focus),
                         feature.Eccentricity(self, enums.eFeature.Eccentricity),
                         feature.MaximumLoop(self, enums.eFeature.MaximumLoop),
                         feature.InnerRadiusVariation(self, enums.eFeature.InnerRadiusVariation),
                         feature.CentralDisplacement(self, enums.eFeature.CentralDisplacement),
                         feature.MeanSpeed(self, enums.eFeature.MeanSpeed),
                         feature.MinSpeed(self, enums.eFeature.MinSpeed),
                         feature.MaxSpeed(self, enums.eFeature.MaxSpeed),
                         feature.MedianSpeed(self, enums.eFeature.MedianSpeed),
                         feature.IQSpeed(self, enums.eFeature.IQSpeed),
                         feature.MeanRotation(self, enums.eFeature.MeanRotation),
                         feature.MedianRotation(self, enums.eFeature.MedianRotation),
                         feature.MinRotation(self, enums.eFeature.MinRotation),
                         feature.MaxRotation(self, enums.eFeature.MaxRotation),
                         feature.IQRotation(self, enums.eFeature.IQRotation),
                         feature.MeanAbsRotation(self, enums.eFeature.MeanAbsRotation),
                         feature.MeanAbsRotation(self, enums.eFeature.MedianAbsRotation),
                         feature.MinAbsRotation(self, enums.eFeature.MinAbsRotation),
                         feature.MaxAbsRotation(self, enums.eFeature.MaxAbsRotation),
                         feature.IQAbsRotation(self, enums.eFeature.IQAbsRotation),
                         feature.PathEfficiency(self, enums.eFeature.PathEfficiency),
                         feature.SumAbsoluteAngles(self, enums.eFeature.SumAbsoluteAngles),
                         feature.LocationDensity(self, enums.eFeature.LocationDensity)]

