# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:57:54 2017

@author: Mark
"""
import pandas as pd

def loadData(data_file_name_path):
#Load the data
    loaded_data = pd.read_csv(data_file_name_path)
    return loaded_data