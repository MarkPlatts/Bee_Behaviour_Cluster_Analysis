# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 06:33:50 2017

@author: Mark
"""

import unittest
import segment as sg
import preprocess
import loop_tool as lt
import math
import numpy as np
import create_segment as cs
import classArena

class TestSegmentMethods(unittest.TestCase):
    
#    def loadData(self, path):
#        
#        df = preprocess.loadData(path)
#        df = preprocess.addColCumulativeDistance(df)
#        df = preprocess.addDistanceCentreCol(df)
#
#        return(df)
        
        
    def test_MaximumLoopLength(self):
        
        df = preprocess.execute("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test_maxloop.csv")
        #df = self.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test_maxloop.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df,20,0,0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena)
        #print("features_first_segment.maximum_loop_length:", features_first_segment.maximum_loop_length)
        self.assertEqual(features_first_segment.maximum_loop_length, 15)
        
    
    def test_FindingCorrectSecondSegment(self):      
        
        df = preprocess.execute("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
        
        first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)

        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[0], 7.0969949712)
        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[-1], 17.5320477473)
        
    def test_DistancePoint100FromCentre(self):
        
        df = preprocess.execute(
        "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
        
        Distance = df['DistanceCentre'].iloc[99]
        print("Distance:", Distance)
        self.assertAlmostEqual(Distance, 36.1062682861314)
        
    def test_MedianDistanceCentre(self):
        
        df = preprocess.execute(
        "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)        
        
        #arena_diameter = df[['x']].max() - df[['x']].min()
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        length_second_segment = cs.getSegmentLength(dt_second_segment)
        
        features_second_segment = sg.Segment(dt_second_segment, length_second_segment, arena)
        
        self.assertAlmostEqual(features_second_segment.median_distance_from_centre, 0.8628325515)
        
    def test_iQRangeDistanceCentre(self):
        df = preprocess.execute(
        "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)        
        
        #arena_diameter = df[['x']].max() - df[['x']].min()
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        
        len_second_segment = cs.getSegmentLength(dt_second_segment)        
        second_segment_features = sg.Segment(dt_second_segment, len_second_segment, arena)
        
        iq_range_distance_centre = second_segment_features.IQRange
        self.assertAlmostEqual(iq_range_distance_centre, 0.0164803959758471)
        
    def test_getSegmentLength(self):
        df = preprocess.execute(
        "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")

        first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment) 
        
        length_segment = cs.getSegmentLength(second_segment)
        
        self.assertAlmostEqual(length_segment, 10.4350527761)
        
    def test_areaFormula(self):
        df = preprocess.execute(
        "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)        
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        length_second_segment = cs.getSegmentLength(dt_second_segment)
        
        features_second_segment = sg.Segment(dt_second_segment,length_second_segment, arena)
        
        #features_second_segment.calcMinEnclosingEllipseArea

        points = np.array([[-1,0,0,1],[0,1,-1,0]]).T      
        
        ellipse = features_second_segment.findMinEnclosingEllipse(points)
        min_enclosing_ellipse_area = features_second_segment.calcMinEnclosingEllipseArea(ellipse.radii)
        
        self.assertAlmostEqual(min_enclosing_ellipse_area, math.pi)
        
    def test_LinesIntersect(self):        
        #See Intersect_Tests.jpg for what the letters refer to
        
        #A
        line1 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        line2 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #B
        line1 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        line2 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #C
        line1 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        line2 = {'x1': 2, 'y1': 1, 'x2': 1, 'y2': 2}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})

        #D
        line1 = {'x1': 2, 'y1': 1, 'x2': 1, 'y2': 2}
        line2 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #E
        line1 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        line2 = {'x1': 1, 'y1': 2, 'x2': 2, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #F
        line1 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        line2 = {'x1': 2, 'y1': 1, 'x2': 1, 'y2': 2}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 1.5, 'y': 1.5})
        
        #G
        line1 = {'x1': 1, 'y1': 1, 'x2': 2, 'y2': 2}
        line2 = {'x1': 4, 'y1': 2, 'x2': 3, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertFalse(bIntersect) 
        
        #H
        line1 = {'x1': 1, 'y1': 3, 'x2': 2, 'y2': 4}
        line2 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertFalse(bIntersect) 
        
        #I Unnecessary

        #J Overlapping
        line1 = {'x1': 1, 'y1': 1, 'x2': 3, 'y2': 3}
        line2 = {'x1': 2, 'y1': 2, 'x2': 4, 'y2': 4}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertTrue(bIntersect)
        self.assertEquals(location, {'x': 2.0, 'y': 2.0})
        
        #K same gradient but not overlapping
        line1 = {'x1': 2, 'y1': 2, 'x2': 1, 'y2': 1}
        line2 = {'x1': 3, 'y1': 3, 'x2': 4, 'y2': 4}
        bIntersect, location = lt.linesIntersect(line1,line2)
        self.assertFalse(bIntersect)         
        
    def test_calcCentralDisplacement(self): 
        df = preprocess.execute(
        "C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test.csv")
        arena = classArena.classArena(df)
                
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0, 0)        
        dt_second_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df, 10, 0.3, cum_dist_end_segment)
        length_second_segment = cs.getSegmentLength(dt_second_segment)
        
        features_second_segment = sg.Segment(dt_second_segment,length_second_segment, arena)
        
        #features_second_segment.calcMinEnclosingEllipseArea

        points = np.array([[-1,0,0,1],[0,1,-1,0]]).T      
        
        ellipse = features_second_segment.findMinEnclosingEllipse(points)
        min_enclosing_ellipse_area = features_second_segment.calcMinEnclosingEllipseArea(ellipse.radii)
        
        self.assertAlmostEqual(min_enclosing_ellipse_area, math.pi)
        
    def test_calcMeanSpeed(self):

        df = preprocess.execute("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/TestData/bee-data_NT_test_maxloop.csv")
                                                                #(traj, lseg, ovlp, cum_dist_end_prev)
        arena = classArena.classArena(df)
        
        dt_first_segment, cum_dist_end_segment, end_trajectory = cs.getSegment(df,20,0,0)
        length_first_segment = cs.getSegmentLength(dt_first_segment)
        features_first_segment = sg.Segment(dt_first_segment, length_first_segment, arena)
        #print("features_first_segment.maximum_loop_length:", features_first_segment.maximum_loop_length)
        self.assertEqual(features_first_segment.mean_speed, 118.75)
        
    #def test_calcMinSpeed(self)
        
#    def test_focusFormula(self):
#        
#        area = calc_features.calcArea(points)
#
#        focus = calc_features.focusFormula(area, seg_length)
#
#        
#        self.assertAlmostEqual(area, math.pi)
        
        
#    def test_calcFocus(self):
#        df = self.setUp()
#        
#        first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
#        second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment)
#        
#        focus = calc_features.calcFocus(segment)
        
    
        
#    def test_CalculatingCorrectDistanceBetweenPoints(self):
#        data = sg.LoadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
#                           
#        p1 = sg.GetPointsFromLine(data,0)
#        p2 = sg.GetPointsFromLine(data,1)
#        print("p1: ", p1)
#        print("p2: ", p2)
#        Distance = sg.CalcDistanceBetweenPoints(p1,p2)
#        print("Distance: " + str(Distance))
#        self.assertAlmostEqual(Distance, 1.763539646)
#       self.assertEqual('foo'.upper(), 'FOO')

#    def test_isupper(self):
#        self.assertTrue('FOO'.isupper())
#        self.assertFalse('Foo'.isupper())
#
#    def test_split(self):
#        s = 'hello world'
#        self.assertEqual(s.split(), ['hello', 'world'])
#        # check that s.split fails when the separator is not a string
#        with self.assertRaises(TypeError):
#            s.split(2)

#if __name__ == '__main__':
#    unittest.main()
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestSegmentMethods)
unittest.TextTestRunner(verbosity=2).run(suite)