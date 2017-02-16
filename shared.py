# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:29:33 2017

@author: Mark
"""

def centreArena(df):
    centre_x = (df['x'].max() + df[['x']].min()).iloc[0]/2.0
    centre_y = (df['y'].max() + df[['y']].min()).iloc[0]/2.0
    return centre_x, centre_y
    
