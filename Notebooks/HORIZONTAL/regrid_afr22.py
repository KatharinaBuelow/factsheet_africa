#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import xesmf as xe
from typing import Optional

# make regridder
#%time regridder = xe.Regridder(pop, dm, method='conservative')
#pop_regrid = regridder(pop / src_area) * tgt_area

# Regrid each file's 'ev_coin_sdu' to AFR-22 grid and compute ensemble median per gridbox
def regrid_ensemble_median(inputfiles,dm, weights_dir, weightvar='ev_coin_sdu_days'):
    '''first regrid to afr22 dm and afterwards calculate ensemle median
    input list of ensemble file
    output one dataset containing ensemble median
    output is per year original input got divided by 30 - years of timeslices
    '''

    # ensure weights directory exists
    os.makedirs(weights_dir, exist_ok=True)

    ensemble_regridded = []

    for fp in inputfiles:
        print(f'Regridding: {os.path.basename(fp)}')
        with xr.open_dataset(fp, decode_timedelta=False) as ds:

            if weightvar not in ds.variables:
                print(f'  Skipped ({weightvar} not found).')
                continue
            else:
                # it needs to be annual, so each value needs to be divided by 30
                da_src = (ds[weightvar] / 30.0).astype('float32')
                # Create/load per-file weights and regrid to AFR-22
                src_id = os.path.splitext(os.path.basename(fp))[0]
                weight_file = os.path.join(weights_dir, f'w_{src_id}_to_AFR22_bilinear.nc')
                print('weight_file: ',weight_file)

                # Use existing grids; ensure lon/lat are marked as coordinates for xESMF
                ds_for_regrid = ds if ('lon' in ds.coords and 'lat' in ds.coords) else ds.set_coords(['lon', 'lat'])
                print(ds_for_regrid.dims, list(ds_for_regrid.coords))
                print(dm.dims, list(dm.coords))
                rg = xe.Regridder(
                    ds_for_regrid, dm, method='bilinear',
                    filename=weight_file, reuse_weights=os.path.exists(weight_file),
                    )
                da_dst = rg(da_src)
                print('  exists:', os.path.exists(weight_file))
                ensemble_regridded.append(da_dst)

                # Save regridded file to disk
                output_file = os.path.join(weights_dir, f'{src_id}_regridded_AFR22.nc')
                da_dst.to_netcdf(output_file)
                print(f'  Saved regridded data to: {output_file}')
    if len(ensemble_regridded) == 0:
        raise RuntimeError('No regridded data available to compute ensemble median.')

    result = xr.concat(ensemble_regridded, dim='ensemble').median(dim='ensemble', skipna=True)
    result.name = weightvar  # Keep the original variable name

    return result


def regrid_ensemble(inputfiles,dm, weights_dir, weightvar='ev_coin_du_days'):
    '''first regrid to afr22 dm   '''

    # ensure weights directory exists
    os.makedirs(weights_dir, exist_ok=True)

    for fp in inputfiles:
        print(f'Regridding: {os.path.basename(fp)}')
        with xr.open_dataset(fp, decode_timedelta=False) as ds:

            if weightvar not in ds.variables:
                print(f'  Skipped ({weightvar} not found).')
                continue
            else:
                # it needs to be annual files
                da_src = ds[weightvar] 
                # Create/load per-file weights and regrid to AFR-22
                src_id = os.path.splitext(os.path.basename(fp))[0]
                weight_file = os.path.join(weights_dir, f'w_{src_id}_to_AFR22_bilinear.nc')
                print('weight_file: ',weight_file)

                # Use existing grids; ensure lon/lat are marked as coordinates for xESMF
                ds_for_regrid = ds if ('lon' in ds.coords and 'lat' in ds.coords) else ds.set_coords(['lon', 'lat'])
                print(ds_for_regrid.dims, list(ds_for_regrid.coords))
                print(dm.dims, list(dm.coords))
                rg = xe.Regridder(
                    ds_for_regrid, dm, method='bilinear',
                    filename=weight_file, reuse_weights=os.path.exists(weight_file),
                    )
                da_dst = rg(da_src)
                # Preserve the original variable name
                da_dst.name = weightvar
                print('  exists:', os.path.exists(weight_file))

                # Save regridded file to disk
                output_file = os.path.join(weights_dir, f'{src_id}_regridded_AFR22.nc')

                da_dst.to_netcdf(output_file)
                print(f'  Saved regridded data to: {output_file}')

    return 
