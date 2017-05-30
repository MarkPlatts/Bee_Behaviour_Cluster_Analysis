# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:19:06 2017

@author: Mark
"""

import csv

#Create CSV file

#def print2CSV(list_segments):
def output(list_segments):
    
    ofile = open("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/Output_features/segment_features.csv", "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    
    #write the column headers
    seg1 = list_segments[0] #get the first segment
    row = ["SegmentID", "Experiment", "UsingLight", "FileName"]
    for iFeature in seg1.features:
        row = row + [iFeature.featureName()]
        
    writer.writerow(row)    
    
    #write the segment values    
    for iSeg in list_segments:
        row = [iSeg.segmentID, iSeg.experiment_name, iSeg.using_light, iSeg.filename]
        for iFeature in iSeg.features:
            row = row + [iFeature.value]
        writer.writerow(row)
    
    ofile.close()

def output_xy(list_segments):
    
    ofile = open("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/Output_features/segment_xys.csv", "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    
    #write the column headers
#    seg1 = list_segments[0] #get the first segment
    row = ["SegmentID", "Experiment", "UsingLight", "FileName", "x_mm", "y_mm"]
#    for iFeature in seg1.features:
#        row = row + [iFeature.featureName()]
        
    writer.writerow(row)    
    
    #write the segment xys    
    for iSeg in list_segments:
        nRows = len(iSeg.segment_data.index)
        for iRow in range(0, nRows):
            row = [iSeg.segmentID, iSeg.experiment_name, iSeg.using_light, iSeg.filename, \
                    iSeg.segment_data.iloc[iRow]['x_mm'], iSeg.segment_data.iloc[iRow]['y_mm']]
#            for iFeature in iSeg.features:
#                row = row + [iFeature.value]
            writer.writerow(row)
    
    ofile.close()    