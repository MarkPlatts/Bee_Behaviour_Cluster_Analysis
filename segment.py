# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:12:31 2017

@author: Mark
"""


import ellipse_tool as et
import math
import numpy as np
import loop_tool as lt

class Segment:


    #Constructor methods =======================================================================================

    def __init__(self, dt_segment, seg_length, arena_diameter, arena_centre_x, arena_centre_y):
        
        #constants
        self.CONST_TIME_BETWEEN_FRAMES = 0.02 #seconds - there are 30,000 frames per 10 minutes
        
        #output - features
        self.median_distance_from_centre = 0
        self.IQRange = 0
        self.focus = 0
        self.eccentricity = 0 
        self.maximum_loop_length = 0   
        self.inner_radius_variation = 0
        self.central_displacement = 0
        self.mean_speed = 0
        
        #input
        self.segment_length = seg_length
        self.dt_segment = dt_segment
        self.arena_diameter = arena_diameter
        self.arena_centre_x = arena_centre_x
        self.arena_centre_y = arena_centre_y
        
        #calculations
        self.calcFeatures()        
        
        
    #calculate features methods =======================================================================================

    def calcMedianDistanceFromCentre(self):
        median = self.dt_segment["DistanceCentre"].median()/(self.arena_diameter/2.0)
        return(median)
        
        
    def calcIQRange(self):
        LQ = self.dt_segment["DistanceCentre"].quantile(0.25)
        UQ = self.dt_segment["DistanceCentre"].quantile(0.75)
        IQRange = (UQ - LQ)/(self.arena_diameter/2.0)
        #IQRange = IQRange
        return(IQRange)
    
    
    def calcFocus(self, min_enclosing_ellipse_area):
        return(1 - 4 * min_enclosing_ellipse_area/(math.pi*self.segment_length**2))
        
        
    def calcEccentricity(self, a, b):
         return(math.sqrt(1 - (b**2)/(a**2)))
         
         
    def calcMaximumLoop(self):
        
        max_length = 0
        
        #find out how many points their are
        nPoints = self.dt_segment.shape[0] #This is the number of lines to check for intersection
        #print("nPoints:", nPoints)
        for iLines1 in range(0,nPoints-3):
            
            #create line between current point and next point
            line1 = {'x1': self.dt_segment['x_mm'].iloc[iLines1], 
                     'y1': self.dt_segment['y_mm'].iloc[iLines1],
                     'x2': self.dt_segment['x_mm'].iloc[iLines1+1],
                     'y2': self.dt_segment['y_mm'].iloc[iLines1+1]}
            for iLines2 in range(iLines1+2, nPoints-1): 
            #loop over subsequent lines check if there is a line that intersects and calculating
            #the length between them
                #print("iLines2+1:", iLines2+1)
                line2 = {'x1': self.dt_segment['x_mm'].iloc[iLines2], 
                         'y1': self.dt_segment['y_mm'].iloc[iLines2],
                         'x2': self.dt_segment['x_mm'].iloc[iLines2+1],
                         'y2': self.dt_segment['y_mm'].iloc[iLines2+1]}
                lines_do_intersect, intersection = lt.linesIntersect(line1, line2)
                if(lines_do_intersect):
                    #calculate the distance between the start of line1 and the start of line2
                    #Although this is not precise I believe the error is insignificant and
                    #and that it is a waste of time calculating the length exactly
                    length = self.dt_segment['CumulativeDistance'].iloc[iLines2] - \
                                self.dt_segment['CumulativeDistance'].iloc[iLines1]
#                    TEST to see that it is finding loops correct
#                    fig, ax = plt.subplots( nrows=1, ncols=1 )
#                    ax.plot(self.dt_segment['x'].iloc[iLines1:iLines2+2],self.dt_segment['y'].iloc[iLines1:iLines2+2])   
#                    filename = "C:/Users/Mark/Desktop/Bees Project/Code/Testing/" + str(iLines1) + ".png"
#                    fig.savefig(filename) 
#                    plt.close(fig)
                    if(length > max_length):
                        #print("length:", length)
                        max_length = length
#                        ax.plot(self.dt_segment['x'].iloc[iLines1:iLines2+2],self.dt_segment['y'].iloc[iLines1:iLines2+2])   
#                        return(0)
        return(max_length)
        
        
    def calcInnerRadiusVariation(self, ellipse_centre, points):

        points_distance_centre_ellipse = np.sqrt(np.square(points[:,0]-ellipse_centre[0]) + np.square(points[:,1]-ellipse_centre[1]))
        
        median = np.median(points_distance_centre_ellipse)
        UQ = np.percentile(points_distance_centre_ellipse, 75)   
        LQ =  np.percentile(points_distance_centre_ellipse, 25)
        
        inner_radius_variation = (UQ - LQ)/median
        print("Inner radius variation:", inner_radius_variation)        
        
        return(inner_radius_variation)
        
        
    def calcCentralDisplacement(self, ellipse_centre_x, ellipse_centre_y, arena_centre_x, arena_centre_y):
        
        x_distance = ellipse_centre_x-arena_centre_x
        y_distance = ellipse_centre_y-arena_centre_y
        
        central_displacement = np.sqrt(np.square(x_distance) + np.square(y_distance))*2/self.arena_diameter
        # print("Central displacement:", central_displacement)
        
        return(central_displacement)
        
        
    def calcMeanSpeed(self):

        distance_travelled_segment = self.dt_segment['CumulativeDistance'].iloc[-1] - \
                    self.dt_segment['CumulativeDistance'].iloc[0]
        
        frames_elapsed_segment = self.dt_segment['frames.comb'].iloc[-1] - \
                    self.dt_segment['frames.comb'].iloc[0]
                    
        mean_speed_segment = distance_travelled_segment / (frames_elapsed_segment * self.CONST_TIME_BETWEEN_FRAMES)
        
        return(mean_speed_segment)
        
        
    #helper methods =======================================================================================
                
    def extractPointsFromDataTable(self):
        return(np.array([self.dt_segment["x_mm"],self.dt_segment["y_mm"]]).T)        
        
    def findMinEnclosingEllipse(self, points):
        ellipse_tool = et.EllipseTool()
        return(ellipse_tool.getMinAreaEllipse(points))
        
    def calcMinEnclosingEllipseArea(self, radii):
        return(radii[0] * radii[1]*math.pi)
        
    def calcAxisMinEnclosingEllipse(self, radii):
        return(max(radii), min(radii))
        
        
    #main routine that is called when segment is constructed==============================================
        
    def calcFeatures(self):         
        
        points = self.extractPointsFromDataTable()
        centre, radii, rotation = self.findMinEnclosingEllipse(points)
        min_enclosing_ellipse_area = self.calcMinEnclosingEllipseArea(radii)
        ellipse_a_axis, ellipse_b_axis = self.calcAxisMinEnclosingEllipse(radii)
        
        self.median_distance_from_centre = self.calcMedianDistanceFromCentre()
        self.IQRange = self.calcIQRange()
        self.focus = self.calcFocus(min_enclosing_ellipse_area)
        self.eccentricity = self.calcEccentricity(ellipse_a_axis, ellipse_b_axis)
        self.maximum_loop_length = self.calcMaximumLoop()
        self.inner_radius_variation = self.calcInnerRadiusVariation(centre, points)
        self.central_displacement = self.calcCentralDisplacement(
                                                            centre[0], centre[1],
                                                            self.arena_centre_x.iloc[0], self.arena_centre_y.iloc[0])
        self.mean_speed = self.calcMeanSpeed()