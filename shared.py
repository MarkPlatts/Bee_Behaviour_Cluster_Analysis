# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:29:33 2017

@author: Mark
"""

def centreArena(df):
    centre_x = (df['x_mm'].max() + df[['x_mm']].min()).iloc[0]/2.0
    centre_y = (df['y_mm'].max() + df[['y_mm']].min()).iloc[0]/2.0
    return centre_x, centre_y
    
