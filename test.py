# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 06:33:50 2017

@author: Mark
"""

import unittest
import segment as sg
from time import gmtime, strftime

class TestSegmentMethods(unittest.TestCase):
    
    def test_FindingCorrectSecondSegment(self):
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())         
        
        df = sg.loadData("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/bee-data_NT.csv")

        df = sg.addColCumulativeDistance(df)
        
        first_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0, 0)        
        second_segment, cum_dist_end_segment = sg.getSegment(df, 10, 0.3, cum_dist_end_segment)

        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[0], 7.53961357202363)
        self.assertAlmostEqual(second_segment['CumulativeDistance'].iloc[-1], 17.5413857439795)
        
        
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