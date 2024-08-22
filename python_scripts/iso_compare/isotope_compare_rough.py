#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 21:50:26 2024

Compare CCC23 data to ECM


@author: Liam
"""

#%% Import packages 

# general
import numpy as np
import pandas as pd

# plotting
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# my functions/classes
import sys
sys.path.append("../core_scripts/")
from ECMclass import ECM

#%% User Inputs

# smoothing window, mm
window = 10

# paths
path_to_data = '../../data/'
path_to_figures = '../../../figures/first_plot/'
path_to_iso = '../../../'
metadata_file = 'metadata.csv'

#%% set up colormap

# make colormap
cmap = matplotlib.colormaps.get_cmap('coolwarm')

#%% Read in metadata and import data

meta = pd.read_csv(path_to_data+metadata_file)

# import each script as an ECM class item
data = []
cores = []
sections = []
faces = []
ACorDCs = []
for index,row in meta.iterrows():
    
    core = row['core']
    section = row['section']
    
    # filter for ALHIC2302 shallow ice
    if core == 'ccc23' and (section== 'd40' or section == 'd41'):


        
        face = row['face']
        ACorDC = row['ACorDC']
        
        print("Reading "+core+", section "+section+'-'+face+'-'+ACorDC)
    
        data_item = ECM(core,section,face,ACorDC)
        
        
        # MANUALLY ADJUST DEPTHS
        if section =='d40':
            data_item.depth = data_item.depth-210.67+210.333
        elif section == 'd41':
            data_item.depth = data_item.depth-211.22+210.778
            
        data_item.rem_ends(10)
        data_item.smooth(window)
        data.append(data_item)
        
        cores.append(core)
        sections.append(section)
        faces.append(face)
        ACorDCs.append(ACorDC)

sec = set(sections)


#%% load water isotope data

iso = pd.read_csv(path_to_iso+'prelim_iso.csv')
iso['depth'] = iso['depth']/100

dmin = 210.2
dmax = 211.5

# filter for depth
iso = iso[iso['depth'] > dmin]
iso = iso[iso['depth'] < dmax]


#%% make plot

fig,ax = plt.subplots(1,2,dpi=200,figsize=(8,8))
ax0a = ax[0]
ax0b = ax[0].twiny()
ax1a = ax[1]
ax1b = ax[1].twiny()

ax0b.set_xlabel('d18O (per mille)')
ax1b.set_xlabel('d18O (per mille)')
ax0a.set_xlabel('AC conductivity (amps)')
ax1a.set_xlabel('DC onductivity (amps)')



for d in data:
    if d.ACorDC == 'AC':
        axs = ax0a
    else:
        axs = ax1a
    
    ycnt=0
    for y in d.y_vec:
        idx = d.y_s == y
        axs.plot(d.meas_s[idx],d.depth_s[idx],label="track "+str(ycnt+1),color=cmap(ycnt/len(d.y_vec)))
        ycnt+=1
        
ax0b.plot(iso['d18O'],iso['depth'],'k.-')
ax1b.plot(iso['d18O'],iso['depth'],'k.-')

ax0b.set_ylim([dmax,dmin])
ax1b.set_ylim([dmax,dmin])

data_item


#%%

for i in range(len(iso)-1):
    if iso['depth'].iloc[i+1]<iso['depth'].iloc[i]:
        print(i)
    
    