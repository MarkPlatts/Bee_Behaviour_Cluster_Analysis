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
import math
import loop_tool as lt
#import enumFeature.enumFeature

class Feature:
    __metaclass__ = ABCMeta
    
    index = -1
    
    def __init__(self, segment, enumFeature):

        self.segment = segment
        self.value = self.calculateFeature()
        self.name = self.featureName()
        self.enumFeature = enumFeature
    
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
        median = self.segment.segment_data["DistanceCentre"].median()/(self.segment.arena.diameter/2.0)
        return(median)   
        
class IQRange(Feature):
    
    def featureName(self):
        return "IQRange"
        
    def calculateFeature(self):
        LQ = self.segment.segment_data["DistanceCentre"].quantile(0.25)
        UQ = self.segment.segment_data["DistanceCentre"].quantile(0.75)
        IQRange = (UQ - LQ)/(self.segment.arena.diameter/2.0)
        return(IQRange)
        
class Focus(Feature):
    
    def featureName(self):
        return "Focus"
    
    def calculateFeature(self):
        return(1 - 4 * self.segment.min_enclosing_ellipse_area/(math.pi*self.segment.segment_length**2))

class Eccentricity(Feature):
    
    def featureName(self):
        return "Eccentricity"
        
    def calculateFeature(self):
        return(math.sqrt(1 - (self.segment.ellipse_b_axis**2)/(self.segment.ellipse_a_axis**2)))
        
class MaximumLoop(Feature):
    
    def featureName(self):
        return "MaximumLoop"
        
    def calculateFeature(self):
        max_length = 0
        
        segment_data = self.segment.segment_data
        
        #find out how many points their are
        nPoints = segment_data.shape[0] #This is the number of lines to check for intersection
        #print("nPoints:", nPoints)
        for iLines1 in range(0,nPoints-3):
            
            #create line between current point and next point
            line1 = {'x1': segment_data['x_mm'].iloc[iLines1], 
                     'y1': segment_data['y_mm'].iloc[iLines1],
                     'x2': segment_data['x_mm'].iloc[iLines1+1],
                     'y2': segment_data['y_mm'].iloc[iLines1+1]}
            for iLines2 in range(iLines1+2, nPoints-1): 
            #loop over subsequent lines check if there is a line that intersects and calculating
            #the length between them
                #print("iLines2+1:", iLines2+1)
                line2 = {'x1': segment_data['x_mm'].iloc[iLines2], 
                         'y1': segment_data['y_mm'].iloc[iLines2],
                         'x2': segment_data['x_mm'].iloc[iLines2+1],
                         'y2': segment_data['y_mm'].iloc[iLines2+1]}
                lines_do_intersect, intersection = lt.linesIntersect(line1, line2)
                if(lines_do_intersect):
                    #calculate the distance between the start of line1 and the start of line2
                    #Although this is not precise I believe the error is insignificant and
                    #and that it is a waste of time calculating the length exactly
                    length = segment_data['CumulativeDistance'].iloc[iLines2] - \
                                segment_data['CumulativeDistance'].iloc[iLines1]
#                    TEST to see that it is finding loops correct
#                    fig, ax = plt.subplots( nrows=1, ncols=1 )
#                    ax.plot(self.segment_data['x'].iloc[iLines1:iLines2+2],self.segment_data['y'].iloc[iLines1:iLines2+2])   
#                    filename = "C:/Users/Mark/Desktop/Bees Project/Code/Testing/" + str(iLines1) + ".png"
#                    fig.savefig(filename) 
#                    plt.close(fig)
                    if(length > max_length):
                        #print("length:", length)
                        max_length = length
#                        ax.plot(self.segment_data['x'].iloc[iLines1:iLines2+2],self.segment_data['y'].iloc[iLines1:iLines2+2])   
#                        return(0)
        return(max_length)
        
        
class InnerRadiusVariation(Feature):
    
    def featureName(self):
        return "InnerRadiusVariation"
        
    def calculateFeature(self):
        sg = self.segment
        
        points_distance_centre_ellipse = np.sqrt(np.square(sg.points[:,0]-sg.ellipse.centre[0]) + np.square(sg.points[:,1]-sg.ellipse.centre[1]))
        
        median = np.median(points_distance_centre_ellipse)
        UQ = np.percentile(points_distance_centre_ellipse, 75)   
        LQ =  np.percentile(points_distance_centre_ellipse, 25)
        
        inner_radius_variation = (UQ - LQ)/median
        #print("Inner radius variation:", inner_radius_variation)        
        
        return(inner_radius_variation)
        
class CentralDisplacement(Feature):
    
    def featureName(self):
        return "CentralDisplacement"
        
    def calculateFeature(self):
        ellipse_centre_x = self.segment.ellipse.centre[0]
        ellipse_centre_y = self.segment.ellipse.centre[1]
        
        x_distance = ellipse_centre_x-self.segment.arena.centre_x
        y_distance = ellipse_centre_y-self.segment.arena.centre_y
        
        central_displacement = np.sqrt(np.square(x_distance) + np.square(y_distance))*2/self.segment.arena.diameter
        
        return(central_displacement)
        

class MeanSpeed(Feature):
    
    def featureName(self):
        return "MeanSpeed"
        
    def calculateFeature(self):
        mean_speed = np.mean(self.segment.segment_data['Speed'].iloc[1:])        
        return(mean_speed)
        
class MedianSpeed(Feature):
    
    def featureName(self):
        return "MedianSpeed"
        
    def calculateFeature(self):
        median_speed = np.median(self.segment.segment_data['Speed'].iloc[1:])        
        return(median_speed)
        
class MinSpeed(Feature):
    
    def featureName(self):
        return "MinSpeed"
        
    def calculateFeature(self):
        min_speed = np.min(self.segment.segment_data['Speed'].iloc[1:])
        return(min_speed)
        
class MaxSpeed(Feature):
    def featureName(self):
        return "MaxSpeed"
        
    def calculateFeature(self):
        max_speed = np.max(self.segment.segment_data['Speed'].iloc[1:])
        return(max_speed)
        
class IQSpeed(Feature):
    def featureName(self):
        return "IQSpeed"
        
    def calculateFeature(self):
        UQ = np.percentile(self.segment.segment_data['Speed'].iloc[1:], 75)   
        LQ =  np.percentile(self.segment.segment_data['Speed'].iloc[1:], 25)
        IQR = (UQ - LQ)
        return(IQR)
        
class MeanRotation(Feature):
    
    def featureName(self):
        return "MeanRotation"

    def calculateFeature(self):
        mean_rotation = np.mean(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(mean_rotation)
        
class MedianRotation(Feature):
    
    def featureName(self):
        return "MedianRotation"

    def calculateFeature(self):
        median_rotation = np.median(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(median_rotation)
        
class MinRotation(Feature):
    
    def featureName(self):
        return "MinRotation"

    def calculateFeature(self):
        min_rotation = np.min(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(min_rotation)

class MaxRotation(Feature):
    
    def featureName(self):
        return "MaxRotation"

    def calculateFeature(self):
        max_rotation = np.max(self.segment.segment_data['Rotation_Corrected'].iloc[1:])
        return(max_rotation)
        
class IQRotation(Feature):
    def featureName(self):
        return "IQRotation"
        
    def calculateFeature(self):
        UQ = np.percentile(self.segment.segment_data['Rotation_Corrected'].iloc[1:], 75)   
        LQ =  np.percentile(self.segment.segment_data['Rotation_Corrected'].iloc[1:], 25)
        IQR = (UQ - LQ)
        return(IQR)
        
class MeanAbsRotation(Feature):
    
    def featureName(self):
        return "MeanAbsRotation"

    def calculateFeature(self):
        mean_rotation = np.mean(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(mean_rotation)
        
class MedianAbsRotation(Feature):
    
    def featureName(self):
        return "MedianAbsRotation"

    def calculateFeature(self):
        median_rotation = np.median(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(median_rotation)

class MinAbsRotation(Feature):
    
    def featureName(self):
        return "MinAbsRotation"

    def calculateFeature(self):
        min_rotation = np.min(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(min_rotation)
        
class MaxAbsRotation(Feature):
    
    def featureName(self):
        return "MaxAbsRotation"

    def calculateFeature(self):
        max_rotation = np.max(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:])
        return(max_rotation)
        
class IQAbsRotation(Feature):
    def featureName(self):
        return "IQAbsRotation"
        
    def calculateFeature(self):
        UQ = np.percentile(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:], 75)   
        LQ =  np.percentile(self.segment.segment_data['Abs_Rotation_Corrected'].iloc[1:], 25)
        IQR = (UQ - LQ)
        return(IQR)
        
#======================================================================================

#class PathEfficiency(Feature):
#    def featureName(self):
#        return "PathEfficiency"
#        
#    def calculateFeature
        

