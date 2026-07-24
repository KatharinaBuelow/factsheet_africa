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
from format_compound_event_tools import annual_sum_with_carry_grid_fast

# Directory input data: calculated compound events
datadir='/work/ch0636/g300047/cicles/compound-events/results'
outdatadir='/work/ch0636/g300047/cicles/compound-events/results/annual_ev_coin_du'
#Variable in compound event file:
var='ev_coin_du'

# Make desision what you want to plot: 
#var_pattern='SU40_du3_TR26_du3'
#var_pattern='SU35_du3_DD_du5'
#var_pattern='SU40_du3_R20mm_du1'
#var_pattern='SU40_du3_DD_du5'
#var_pattern='SU40_du7_DD_du7'
#var_pattern='SU35_du7_DD_du7'
#var_pattern='SU40_du3_R20mm_du1'
var_pattern='SU40_du3_R50mm_du1'
#var_pattern='SU40_du3_TR_du3'
##var_pattern='DD_du7_R20mm_du1'

# openfile

files=glob.glob(os.path.join(datadir, f"compev_{var_pattern}_AFR-22_*.nc"))
for f in files:
    print(f)
    coin_ds = open_xrdataset(f, decode_times=False)
 
    # Re-run
    outfile=os.path.basename(f).replace(".nc", "_annual.nc")
    outfile_grid = os.path.join(outdatadir, outfile)
    ds_out = annual_sum_with_carry_grid_fast(coin_ds, outfile_grid)
    
    print(f"Updated with date dimension: {outfile_grid}")

