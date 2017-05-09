# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:19:06 2017

@author: Mark
"""

import csv

#Create CSV file

#def print2CSV(list_segments):
def output(list_segments):
    
    ofile = open("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/Output_features/test_writing_2_csv.csv", "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    
    #write the column headers
    seg1 = list_segments[0] #get the first segment
    row = ["SegmentIndex"]
    for iFeature in seg1.features:
        row = row + [iFeature.featureName()]
    writer.writerow(row)    
    
    #write the segment values    
    for iSeg in list_segments:
        row = [iSeg.index]
        for iFeature in iSeg.features:
            row = row + [iFeature.value]
        writer.writerow(row)
    
    ofile.close()
