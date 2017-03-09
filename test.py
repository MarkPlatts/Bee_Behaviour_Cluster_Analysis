# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 06:33:50 2017

@author: Mark
"""

import unittest
import segment as sg
import preprocess
import calc_features
import math
import numpy as np

class TestSegmentMethods(unittest.TestCase):
    
    def setUp(self):
        
        df = preprocess.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")
        df = preprocess.addColCumulativeDistance(df)
        df = preprocess.addDistanceCentreCol(df)
        
        return(df)
    
    def test_FindingCorrectSecondSegment(self):      
        
        df = self.setUp()
        
        first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment)

        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[0], 7.53961357202363)
        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[-1], 17.5413857439795)
        
    def test_DistancePoint100FromCentre(self):
        
        df = self.setUp()
        
        Distance = df['DistanceCentre'].iloc[99]
        
        self.assertAlmostEqual(Distance, 34.1204235303938)
        
    def test_MedianDistanceCentre(self):
        df = self.setUp()
        
        width = df[['x']].max() - df[['x']].min()
        
        first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment)
        
        median_distance_centre = calc_features.calcMedianDistanceFromCentre(second_segment, width)
        self.assertAlmostEqual(median_distance_centre, 0.861570194585884)
        
    def test_iQRangeDistanceCentre(self):
        df = self.setUp()
        
        width = df[['x']].max() - df[['x']].min()
        
        first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment)
        
        iq_range_distance_centre = calc_features.calcIQRange(second_segment, width)
        self.assertAlmostEqual(iq_range_distance_centre, 0.00397643745469342)
        
    def test_getSegmentLength(self):
        df = self.setUp()

        first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment) 
        
        length_segment = sg.getSegmentLength(second_segment)
        
        self.assertAlmostEqual(length_segment, 10.0017721719558137)
        
    def test_areaFormula(self):

        points = np.array([[-1,0,0,1],[0,1,-1,0]]).T      
        area = calc_features.areaFormula(points)
        
        self.assertAlmostEqual(area, math.pi)
        
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