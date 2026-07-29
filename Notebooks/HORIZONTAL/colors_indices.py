#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr
import cftime


def directory_available(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return


def colorsteps_diff(var):
    """
    Function to define color steps and levels for difference plots
    :param var: variable name
    :return: color_steps_diff, level_steps_diff
    """
    # Colors and levels for the plots
    # for difference plots yearly
    if var in ['TR', 'TR26','SU35', 'HSx', 'HSn', 'SU40']:
        color_steps_diff = ['#d1e5f0', '#ffffff', '#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7', '#df65b0', '#e7298a',
                            '#ce1256', '#980043', '#67001f']
    elif var in ['HSf', ]:
        color_steps_diff = ['#92c5de', '#d1e5f0', '#ffffff', '#ffffff', '#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7',
                            '#df65b0', '#e7298a', '#ce1256', '#980043', '#67001f']
    elif var in ['DD']:
        color_steps_diff = ['#01665e','#35978f','#80cdc1','#c7eae5','#f5f5f5','#f6e8c3','#dfc27d','#bf812d','#8c510a']
    elif var in ['R20mm']:
        color_steps_diff = ['#7f3b08','#b35806','#e08214','#fdb863','#fee0b6','#f7f7f7','#d8daeb','#b2abd2','#8073ac','#542788','#2d004b']
    elif var in ['HWf', ]:
        color_steps_diff = ['#92c5de', '#d1e5f0', '#ffffff', '#ffffff', '#ffffcc', '#ffeda0', '#fed976',
                            '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026']
    # Warmspell with tasmax>30
    elif var in ['SU30', 'HWx', 'HWn']:
        color_steps_diff = ['#d1e5f0', '#ffffff', '#ffffcc', '#ffeda0',
                            '#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
    elif var in ['DTR']:
        color_steps_diff = ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7', '#d1e5f0', '#92c5de', '#4393c3', '#2166ac', '#053061']
        color_steps_diff = color_steps_diff[::-1]
    # difference plots for WSDI
    elif var in ['WSDI']:
        color_steps_diff = ['#ffffff', '#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026', '#7a0177', '#49006a']
    # difference plots of TG:
    elif var in ['TG']:
        color_steps_diff = ['#ffffff', '#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026', '#ae017e', '#7a0177', '#49006a']
    elif var in ['number_of_people']:
        color_steps_diff = ['#a50026','#d73027','#f46d43','#fdae61','#fee08b',
             '#ffffbf','#d9ef8b','#a6d96a', '#66bd63','#1a9850','#006837', '#ffffff','#d9d9d9']
    else:
        print('no colors defined for ', var)

    if var in ['TR', 'TR26','SU30', 'SU35', 'HSn', 'SU40']:
        level_steps_diff = [0, 5, 10, 15, 20, 30, 45, 60, 90, 120]
    elif var in ['DD']:
        level_steps_diff = [-35,-25,-15, -5,5,15,25,35]
    elif var in ['R20mm']:
        level_steps_diff = [-5,-4,-3,-2, -1, 1, 2,3,4,5]
    elif var == 'SU40':
        level_steps_diff = [0, 2, 4, 6, 8, 10, 15, 20, 30, 40]        
    elif var == 'HWn':
        level_steps_diff = [0, 10, 20, 30, 60, 90, 120, 150, 180, 220]
    elif var in ['HSx', 'HWx']:
        level_steps_diff = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    elif var in ['HSf', 'HWf']:
        level_steps_diff = [-3, -1, 0, 1, 3, 5, 7, 9, 11, 13]
    elif var == 'TG':
        level_steps_diff = [-0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    elif var == 'DTR':
        level_steps_diff = [-2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5]
    elif var == 'WSDI':
        level_steps_diff = [0, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350]
    elif var == 'number_of_people':
        level_steps_diff = [0,10,20,30,40,50,60,70,80,90,100,110]
    else:
        print('no level_steps for ' + var + ' are provided')

    return color_steps_diff, level_steps_diff


def colorsteps_absolute(var):
    """
    Function to define color steps and levels for absolute plots
    :param var: variable name
    :return: color_steps, level_steps
    """
    # Colors and levels for the plots
    # for absolute plots year

    if var in ['TR','TR26','SU35','SU30','SU40','HSn']:
        color_steps=['#d9d9d9','#ffffff','#fff7f3','#fde0dd','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177','#807dba','#6a51a3','#54278f','#3f007d']
    elif var in ['DD']:
        color_steps=['#ffffe5','#fff7bc','#fee391','#fec44f','#fe9929','#ec7014','#cc4c02','#993404','#662506','#67000d']
    elif var in ['R20mm']:
        color_steps=['#d9d9d9','#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b']
    elif var in ['TG','DTR']:
        color_steps=['#d9d9d9','#ffffff','#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026']
    elif var in ['HSx','HSf','HWf','HWn','HWx']:
        color_steps=['#d9d9d9','#ffffff','#f7f4f9','#e7e1ef','#d4b9da','#c994c7','#df65b0','#e7298a','#ce1256','#980043','#67001f']
    elif var in ['number_of_people']:
        color_steps=['#d9d9d9','#ffffff','#f5f5f5','#c7eae5',
            '#80cdc1','#66c2a4','#35978f','#01665e','#003c30',
            '#f6e8c3',
            '#dfc27d','#bf812d',"#a35414","#854e0c",'#543005',]
    elif var in ['ev_coin_sdu', 'ev_coin_sdu_median']:
        color_steps=['#d9d9d9','#5e4fa2','#3288bd','#66c2a5','#abdda4','#e6f598','#ffffbf','#fee08b','#fdae61','#f46d43','#d53e4f','#9e0142']
        color_steps=['#d9d9d9','#fff7f3','#fde0dd','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177','#49006a']
    else:
        print('no color steps defined')

    if var=='TR':
        level_steps=[0,30,60,90,120,150,180,210,240,270,300,330,360]
    elif var=='TR26':
        level_steps=[0,30,60,90,120,150,180,210,240,270,300,330,360]
    elif var=='R20mm':
        level_steps=[0,5,10,15,20,25,30,35,40]
    elif var=='TG':
        level_steps=[0,10,15,18,21,24,27,30,33]
    elif var=='DD':
        level_steps=[90,120,150,180,210,240,270,300,330]
    elif var=='DTR':
        level_steps=[0,6,8,10,12,14,16,17,18]
    elif var in ['SU30','SU35','HSn']:
        level_steps=[0,30,60,90,120,150,180,210,240,270,300,330,360]  
    elif var in ['SU40']:
        level_steps=[0,20,40,60,80,100,120,140, 160,180,200,220,240]
    elif var in ['HSx','HWx']:
        level_steps=[0,30,60,90,120,150,180,210,240]
        # Some graphical features:
    # set the colors, special case for population:
    elif var in ['number_of_people']:
        level_steps=[0,5,10,20,30,60,90,120,150,180,210,240,270]
    elif var in ['ev_coin_sdu', 'ev_coin_sdu_median']:
        level_steps = [0,5,10,20,30,40,60,80,100]
        #heavy precip
        #level_steps = [0,1,2,3,4,5,6,7]
    else:
        print('no level_steps for '+ var+' are provided')
    return color_steps, level_steps


def colorsteps_exposure(var):

    """
    colors and levels for robust exposure plots
    """

    if var in ['exposure', 'person_events']:
        color_steps_exp=['#d9d9d9',"#fdfde8",'#ffffcc','#ffeda0','#fed976',
            '#feb24c','#fd8d3c','#fc4e2a',
            '#e31a1c','#bd0026','#800026',"#4B0117"]
    else:
        print('no color steps defined')
    if var=='exposure':
        #level_steps_exp=[0,2,4,6,8,10,12,14,16,18,20]
        level_steps_exp=[0,1,2,3,4,5,6,7,8,9,10]
    elif var=='person_events':
        level_steps_exp=[0,600,1200,1500,1800,2100,2400,2700,3000,3300]
    else:
        print('no level_steps for '+ var+' are provided')
    return color_steps_exp, level_steps_exp

def colorsteps_comp_ev(var, var_pattern):

    """
    colors and levels for robust compound eventsplots
    """
    #era5
    if var in ['ev_coin_sdu']:
        print(var_pattern)
        color_steps=['#ffffff','#f0f0f0','#d9d9d9','#bdbdbd','#969696','#737373','#525252','#252525','#000000'] 
        if var_pattern in ['SU40_du3_TR26_du3','SU40_du7_DD_du7']:
            level_steps=[5,10,15,20,25,30,35,40]
        elif var_pattern in ['SU40_du3_DD_du5','SU40_du3_TR_du3']:
            level_steps=[10,20,30,40,50,60,70,80]  
        elif var_pattern in ['SU35_du3_DD_du5','SU35_du7_DD_du7']:
            level_steps=[25,50,75,100,125,150,175,200]
        elif var_pattern in ['SU35_du3_R20mm_du1', 'SU40_du3_R20mm_du1','SU40_du3_R50mm_du1']:
            level_steps=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7]
        elif var_pattern in ['DD_du7_R20mm_du1']:
            level_steps=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7]    

    # absolute values
    elif var in ['ev_coin_du_days']:
        color_steps=["#fdfde8",'#ffffcc','#ffeda0','#fed976',
            '#feb24c','#fd8d3c','#fc4e2a',
            '#e31a1c','#bd0026','#800026',"#4B0117"]
        if var_pattern in ['SU40_du3_DD_du5','SU40_du3_TR26_du3', 'SU40_du3_TR_du3','SU40_du7_DD_du7']:
            level_steps=[10,20,30,40,60,80,100,120,140,160]
        elif var_pattern in ['SU35_du3_DD_du5','SU35_du7_DD_du7']:
            level_steps=[50,100,120,140,160,180,200,220,240, 260]
        elif var_pattern in ['SU35_du3_R20mm_du1', 'SU40_du3_R20mm_du1','SU40_du3_R50mm_du1']:
            color_steps=['#f7fcfd','#e0ecf4','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#810f7c','#4d004b']
            level_steps=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
        elif var_pattern in ['DD_du7_R20mm_du1']:
            color_steps=['#f7fcfd','#e0ecf4','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#810f7c','#4d004b']
            level_steps=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]    
        #else:
            #level_steps=[5,10,20,30,40,50,60,80,100,120]
        else:
            raise ValueError('no level_steps for ' + var + ' are provided for pattern ' + var_pattern)

        
    elif var in ['ev_coin_du_days_ensemble_median_diff', 'ev_coin_du_days_ensemble_mean_diff']:
        color_steps=["#fdfde8",'#ffffcc','#ffeda0','#fed976',
                        '#feb24c','#fd8d3c','#fc4e2a',
                        '#e31a1c','#bd0026','#800026',"#4B0117"]
        if var_pattern in ['SU40_du3_DD_du5', 'SU40_du3_TR26_du3','SU40_du3_TR_du3','SU40_du7_DD_du7']:
            level_steps=[5,10,20,30,40,50,60,80,100,120]
        elif var_pattern in ['SU35_du3_DD_du5','SU35_du7_DD_du7']:
            level_steps=[5,10,20,30,40,50,60,70,80,90]
        elif var_pattern in ['SU35_du3_R20mm_du1', 'SU40_du3_R20mm_du1','SU40_du3_R50mm_du1']:
            level_steps=[-3,-2,-1,-0.5,0,0.5,1,2,3]  
            color_steps=['#053061','#2166ac','#4393c3','#92c5de','#d1e5f0','#f7f7f7','#fddbc7','#f4a582','#d6604d','#b2182b','#67001f']
        elif var_pattern in ['DD_du7_R20mm_du1']:
            color_steps=['#053061','#2166ac','#4393c3','#92c5de','#d1e5f0','#f7f7f7','#fddbc7','#f4a582','#d6604d','#b2182b','#67001f']
            level_steps=[-3,-2,-1,-0.5,0,0.5,1,2,3]      
        else:
            raise ValueError('no level_steps for ' + var + ' are provided for pattern ' + var_pattern)
    
        #color_steps=['#d9d9d9',"#fdfde8",'#ffffcc','#ffeda0','#fed976',
        #    '#feb24c','#fd8d3c','#fc4e2a',
        #    '#e31a1c','#bd0026','#800026',"#4B0117"]
        
    else:
        raise ValueError('no color steps defined for ' + var)
    return color_steps, level_steps