#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 09:39:20 2024

Plot all data from ALHIC2302 Shallow Cores

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
metadata_file = 'metadata.csv'

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
    
    # filter for ALHIC2302 shallow ice
    if core == 'ccc23':

        
        section = row['section']
        face = row['face']
        ACorDC = row['ACorDC']
        
        print("Reading "+core+", section "+section+'-'+face+'-'+ACorDC)
    
        data_item = ECM(core,section,face,ACorDC)
        data_item.rem_ends(10)
        data_item.smooth(window)
        data.append(data_item)
        
        cores.append(core)
        sections.append(section)
        faces.append(face)
        ACorDCs.append(ACorDC)

sec = set(sections)

#%% define plotting function
def plotquarter(y_vec,ycor,d,meas,button,axs,rescale):
    
    width = y_vec[1] - y_vec[0]
    
    for y in y_vec:
        
        
        idx = ycor==y
        
        tmeas = meas[idx]
        tbut = button[idx]
        tycor = ycor[idx]
        td = d[idx]
        
        for i in range(len(tmeas)-1):
            
            if tbut[i] == 0:
                
                axs.add_patch(Rectangle((y-(width-0.2)/2,td[i]),(width-0.2),td[i+1]-td[i],facecolor=my_cmap(rescale(tmeas[i]))))
            else:
                axs.add_patch(Rectangle((y-(width-0.2)/2,td[i]),(width-0.2),td[i+1]-td[i],facecolor='k'))
            
    return()

#%% define function to find unique elements in list
def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    
    return(unique_list)

#%% Make colormap

# make colormap
my_cmap = matplotlib.colormaps['Spectral']

#%% plot each section


for sec in unique(sections):

    
    # print update
    print("Running Section "+sec)
    
    # set data to empty
    AC_t = None
    AC_l = None
    DC_t = None
    DC_l = None
    #loop through data 
    for d in data:
        
        # find faces
        if d.section==sec:
            if d.ACorDC == 'AC':
                AC = d                 
            else:
                DC = d
    
    # find depth max and minimum
    minvec = []
    maxvec = []
    AC_all = []
    DC_all = []
    for data_face in [AC,DC]:
        if data_face != None:
            minvec.append(min(data_face.depth))
            maxvec.append(max(data_face.depth))
                
    ACpltmin = np.percentile(AC.meas_s,5)
    ACpltmax = np.percentile(AC.meas_s,95)
    DCpltmin = np.percentile(DC.meas_s,5)
    DCpltmax = np.percentile(DC.meas_s,95)
    
    
    ACrescale = lambda k: (k-ACpltmin) /  (ACpltmax-ACpltmin)
    DCrescale = lambda k: (k-DCpltmin) /  (DCpltmax-DCpltmin)
    dmin = min(minvec)
    dmax = max(maxvec)
    
    # make figure
    fig,ax = plt.subplots(1,2,figsize=(9,6),dpi=200)
    
    # set up plots
    for a,d in zip(ax,[AC,DC]):
        
        a.set_ylim([dmax, dmin])
        a.set_ylabel('Depth (m)')
        a.set_xlabel('Distance Accross Core')
        
        if d != None:
            
            a.set_xlim([d.y_right,d.y_left])
            
            yall = d.y_s
            yvec = d.y_vec
            
            if d.ACorDC == 'AC':
                rescale = ACrescale
            else:
                rescale = DCrescale
                
            # plot data
            plotquarter(yvec,
                        yall,
                        d.depth_s,
                        d.meas_s,
                        d.button_s,
                        a,
                        rescale)

    # housekeeping
    fig.suptitle('CCC23 - '+sec+' - '+str(window)+' mm smooth')
    ax[0].set_title('AC')
    ax[1].set_title('DC')

    
    fig.tight_layout()

    # ad colorbar
    #fig.subplots_adjust(bottom=0.8)
    #    ACcbar_ax = fig.add_axes([0.08,-0.07,0.35,0.05])
    ACcbar_ax = fig.add_axes([0.07,-0.05,0.35,0.05])
    ACnorm = matplotlib.colors.Normalize(vmin=ACpltmin,vmax=ACpltmax)
    DCcbar_ax = fig.add_axes([0.58,-0.05,0.35,0.05])
    DCnorm = matplotlib.colors.Normalize(vmin=DCpltmin,vmax=DCpltmax)
    ACcbar = fig.colorbar(matplotlib.cm.ScalarMappable(norm=ACnorm, cmap=my_cmap),cax=ACcbar_ax,
                  orientation='horizontal',label='Current (amps)')
    DCcbar = fig.colorbar(matplotlib.cm.ScalarMappable(norm=DCnorm, cmap=my_cmap),cax=DCcbar_ax,
                  orientation='horizontal',label='Current (amps)')
    
    # save figure
    fname = path_to_figures +'ccc23-'+sec+'.png'
    fig.savefig(fname,bbox_inches='tight')
    plt.close(fig)
    print("     done with small plot")
    








    