#!/usr/bin/env python3

import os
import pandas as pd

import numpy as np
import glob
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
from typing import Optional
import matplotlib as mpl


def mask_and_save(fp_list, var, mask, out_dir):
    out_list = []
    for fp in fp_list:
        ds = xr.open_dataset(fp, decode_timedelta=False)
        da = ds[var]
        mask_da = xr.DataArray(
            mask, dims=('rlat', 'rlon'),
            coords={'rlat': ds['rlat'], 'rlon': ds['rlon']}
        )
        da_masked = da.where(mask_da, other=np.nan)
        base = os.path.basename(fp)
        out_fp = os.path.join(out_dir, base.replace('.nc', '_BF_masked.nc'))
        da_masked.to_dataset(name=var).to_netcdf(
            out_fp,
            encoding={var: {'zlib': True, 'complevel': 4}}
        )
        ds.close()
        out_list.append(out_fp)
    return out_list


def maskout_country(sims_rcp26,sims_rcp85, shpfile, dm, var, datadir):
    '''mask out values outside the country shapefile
    fp_list: list of file paths to be masked
    shpfile: geopandas dataframe of the country shapefile
    dm: cordex domain object (AFR-22)
    var: variable name to be masked
    datadir: base data directory to save masked files
    '''
    # Compute a boolean mask for the AFR-22 grid that is True inside the shapefile and False outside
    # Uses dm (AFR-22 domain) and shpfile (GeoDataFrame of Burkina Faso)
    bf = shpfile.copy()
    if bf.crs is None:
        bf = bf.set_crs(epsg=4326)
    else:
        bf = bf.to_crs(4326)
    union_geom = bf.unary_union

    lon = dm['lon'].values
    lat = dm['lat'].values
    points = gpd.points_from_xy(lon.ravel(), lat.ravel())
    points_gs = gpd.GeoSeries(points, crs='EPSG:4326')
    mask_flat = points_gs.within(union_geom).to_numpy()
    mask = mask_flat.reshape(lat.shape)

    # Apply mask and save masked files
    out_dir = os.path.join(datadir, 'ENSEMBLE', 'masked')
    os.makedirs(out_dir, exist_ok=True)
    sims_rcp26_masked = mask_and_save(sims_rcp26, var, mask, out_dir)
    sims_rcp85_masked = mask_and_save(sims_rcp85, var, mask, out_dir)

    print('Masked files saved:')
    print('rcp26:', sims_rcp26_masked)
    print('rcp85:', sims_rcp85_masked)

    return sims_rcp26_masked, sims_rcp85_masked


def min_max_levels(sims_rcp26_masked, sims_rcp85_masked, var):
    '''Compute global min/max across masked rcp26 and rcp85 datasets and build 9 evenly spaced levels
    sims_rcp26_masked: list of file paths for rcp26 masked datasets
    sims_rcp85_masked: list of file paths for rcp85 masked datasets
    var: variable name to compute min/max for
    returns: level_steps (list of 9 evenly spaced levels)
    '''
    all_files = sims_rcp26_masked + sims_rcp85_masked

    min_val = np.inf
    max_val = -np.inf

    for fp in all_files:
        ds = xr.open_dataset(fp, decode_timedelta=False)
        da = ds[var] if var in ds.data_vars else list(ds.data_vars.values())[0]
        vmin = float(da.min(skipna=True).to_numpy().item())
        vmax = float(da.max(skipna=True).to_numpy().item())
        min_val = min(min_val, vmin)
        max_val = max(max_val, vmax)
        ds.close()

    # Fallback in case min == max (degenerate data)
    if not np.isfinite(min_val) or not np.isfinite(max_val):
        raise RuntimeError("Unable to compute finite min/max from datasets.")
    if min_val == max_val:
        span = max(1.0, abs(min_val))  # create a small span around the single value
        min_val -= 4 * span
        max_val += 4 * span

    #level_steps = [round(x, 2) for x in np.linspace(min_val, max_val, 9)]
    level_steps = np.round(np.linspace(min_val, max_val, 9)).astype(int)
    
    #print(f'Updated level_steps (min={min_val:.2f}, max={max_val:.2f}): {level_steps}')
    return level_steps

# Add a dynamic scale bar (in km) to the existing shapefile plot (ax)

def _nice_length_km(target_km):
    # pick a nice rounded length close to 20% of map width
    candidates = [10, 25, 50, 100, 150, 200, 300, 500, 1000]
    for c in candidates:
        if c >= target_km:
            return c
    return candidates[-1]

def add_scalebar(ax, geom=None, location='lower left', segments=4, pad_frac=0.05, height_frac=0.01, font_size=10):
    # Representative latitude for km-per-degree conversion
    if geom is not None:
        lat_ref = float(geom.centroid.y)
    else:
        y0, y1 = ax.get_ylim()
        lat_ref = (y0 + y1) / 2.0

    # Approx km per degree of longitude at given latitude
    km_per_deg_lon = 111.32 * np.cos(np.deg2rad(lat_ref))

    # Determine bar length ~ 20% of map width, rounded to a nice value
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    width_deg = x1 - x0
    width_km = max(1e-6, width_deg * km_per_deg_lon)
    length_km = _nice_length_km(width_km * 0.2)
    length_deg = length_km / km_per_deg_lon

    # Bar placement
    pad_x = pad_frac * width_deg
    pad_y = pad_frac * (y1 - y0)
    bar_height = height_frac * (y1 - y0)

    if location == 'lower left':
        bx0 = x0 + pad_x
        by0 = y0 + pad_y
    elif location == 'lower right':
        bx0 = x1 - pad_x - length_deg
        by0 = y0 + pad_y
    elif location == 'upper left':
        bx0 = x0 + pad_x
        by0 = y1 - pad_y - bar_height
    elif location == 'upper right':
        bx0 = x1 - pad_x - length_deg
        by0 = y1 - pad_y - bar_height
    else:
        bx0 = x0 + pad_x
        by0 = y0 + pad_y

    # Draw alternating black/white segments
    seg_width = length_deg / max(1, segments)
    for i in range(segments):
        rect = mpl.patches.Rectangle(
            (bx0 + i * seg_width, by0),
            seg_width,
            bar_height,
            facecolor=('black' if i % 2 == 0 else 'white'),
            edgecolor='black',
            linewidth=0.8
        )
        ax.add_patch(rect)

    # Label
    ax.text(
        bx0 + length_deg / 2.0,
        by0 + bar_height * 1.5,
        f'{int(length_km)} km',
        ha='center', va='bottom',
        fontsize=font_size
    )

# Use the existing ax and Burkina Faso geometry union to add a scale bar
#add_scalebar(ax, geom=union_geom, location='lower left', segments=4)

