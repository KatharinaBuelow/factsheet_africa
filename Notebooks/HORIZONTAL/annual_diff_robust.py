#!/usr/bin/env python3
import os
import glob
import shutil

import xarray as xr
#
import matplotlib as mpl
import matplotlib.pyplot as plt
import cordex as cx
from pyhomogenize import open_xrdataset
from regrid_afr22 import regrid_ensemble
from calculate_diff_robustness import timeslice, ensemblemean_exp

from format_compound_event_tools import annual_sum_with_carry_grid_fast
# Directory
outdatadir='/work/ch0636/g300047/cicles/compound-events/results/diff_robustness'
# INPUT
datadir='/work/ch0636/g300047/cicles/compound-events/results/annual_ev_coin_du'
weights_dir=os.path.join(datadir,'weights')
#Variable in compound event file:
var='ev_coin_du_days'

# Make desision what you want to plot: 
#var_pattern='SU40_du3_TR26_du3'
#var_pattern='SU35_du3_DD_du5'
#var_pattern='SU35_du3_R20mm_du1'
#var_pattern='SU40_du7_DD_du7' 
#var_pattern='SU35_du7_DD_du7'
#var_pattern='SU40_du3_DD_du5'
#var_pattern='SU40_du3_R20mm_du1'
var_pattern='SU40_du3_R50mm_du1'
#var_pattern='SU40_du3_TR_du3'
#var_pattern='DD_du7_R20mm_du1'
        
# carry on with regridded files
# the function timeslice will select the time slice and 
#  * calculate the mean over the time slice : outdatadir/MEAN*
#  * calculate the difference
#  * calculate the significance of change : outdatadir/significance*
# the result file will contain:
# input value: ev_coin_du(time, rlat, rlon)float32
# mann white u test result: p_value(rlat, rlon)float32
# significance(rlat, rlon)int64
# ev_coin_du_diff(rlat, rlon)float32


# The output is saved in outdatadir

sims_historical = glob.glob(os.path.join(weights_dir,'compev_'+var_pattern+'*1991-2020_annual_regridded_AFR22.nc'))

for sim in sims_historical:
    print(sim)
    #Select timeslice, output annual files (30 timesteps)
    #calculate mean over timeslice 
    #calculate difference
    #calculate significance of change
    timeslice(sim,outdatadir,var=var)

# calculate ensemble mean for each rcp and mean change
ensemblemean_exp(outdatadir, var, var_pattern)



