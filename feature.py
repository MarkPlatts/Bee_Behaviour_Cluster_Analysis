# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 07:59:01 2017

@author: Mark
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 04:12:44 2017

@author: Mark
"""

from abc import ABCMeta, abstractmethod
import numpy as np

class Feature:
    __metaclass__ = ABCMeta
    
    index = -1
    
    def __init__(self, data, seg_length, arena):

        self.segment_data = data
        self.arena = arena
        self.value = self.calculateFeature()
        self.name = self.featureName()
    
    @abstractmethod
    def featureName(self):
        pass
    
    @abstractmethod
    def calculateFeature(self):
        pass

        
class MedianDistanceFromCentre(Feature):
    
    def featureName(self):
        return "MedianDistanceFromCentre"
        
    def calculateFeature(self):
        median = self.segment_data["DistanceCentre"].median()/(self.arena.diameter/2.0)
        return(median)   
        


#simplelist = []
#
#Square.index = 1
#Rectangle.index = 2
#
#simplelist.append(Square(2))
#simplelist.append(Square(4))
#simplelist.append(Rectangle(9))
#
#for i in simplelist:
#    print("featureName:", i.featureName())
#    print("featureIndex:", i.index)
#    print("feature_value:", i.feature_value)
