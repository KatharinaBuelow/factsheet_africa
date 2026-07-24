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
import dask
#from dask.distributed import Client
import scipy.stats as sts
import xarray as xr
import dask
from pyhomogenize import open_xrdataset, save_xrdataset

import cordex



# calculate difference for each simulation and time slice to the reference period 1991-2020 and save difference file locally

def calculate_pvalue(ds, ds_ref, var):
    print("Do Mann-Whitney-U-Test.")
    ds_ref = ds_ref.chunk(dict(time=-1))
    ds = ds.chunk(dict(time=-1))
    
    def _mannwhitneyu(sample1, sample2):
        return sts.mannwhitneyu(
            sample1, 
            sample2, 
            nan_policy = "omit",
        )[1]
    da = xr.apply_ufunc(
        _mannwhitneyu,
        ds_ref[var],
        ds[var],
        input_core_dims=[["time"], ["time"]],
        vectorize=True,
        dask="parallelized",
        output_dtypes = ["float32"],
        keep_attrs = True,
    ).compute()
    ds["p_value"] = da
    ds["significance"] = xr.where(da < 0.05, 1, 0)
    ds["significance"].attrs = ds["p_value"].attrs
    return ds

def calculate_mean(sim,var, outfilemean):
    ds = xr.open_dataset(sim, decode_times=False)
    if var not in ds.data_vars:
        raise KeyError(f"Variable '{var}' not found in {sim}. Available: {list(ds.data_vars)}")

    # keep only target variable to avoid writing unrelated variables with
    # problematic encodings/chunks
    ds_mean = ds[[var]].mean(dim="time", keep_attrs=True)
    ds_mean[var].attrs = ds[var].attrs

    # remove inherited encodings/chunksizes after dimension reduction
    ds_mean = ds_mean.reset_encoding()
    for v in ds_mean.variables:
        ds_mean[v].encoding = {}

    ds_mean.load().to_netcdf(outfilemean, mode="w", engine="netcdf4")
    ds.close()
    return

def timeslice(sim,outdatadir,var):
    '''
    Select timeslice, output annual files (30 timesteps)
    calculate mean over timeslice 
    calculate difference
    calculate significance of change
    '''
    # ensure outdatadir directory exists
    os.makedirs(outdatadir, exist_ok=True)

    #compev_SU35_du3_DD_du5_AFR-22_NCC-NorESM1-M_rcp85_r1i1p1_CLMcom-KIT-CCLM5-0-15_v1_day_GERICS_1991-2020_regridded_AFR22.nc
    ds_ref = None
    ds_hist_mean = None
    for timeslice in ('1991-2020','2031-2060', '2069-2098'):
        sim_timeslice = sim.replace("1991-2020", timeslice)
        outfilename = os.path.basename(sim_timeslice)

        #outfile=os.path.join(outdatadir,outfilename)
        outfilemean=os.path.join(outdatadir,'MEAN_'+outfilename)

        # delete existing mean file; ignore if it does not exist
        try:
            os.remove(outfilemean)
            print("Removed existing file:", outfilemean)
        except FileNotFoundError:
            pass

        calculate_mean(sim_timeslice, var, outfilemean)
        
        print('calculate significance')
        
        if timeslice != '1991-2020':
            ds = xr.open_mfdataset(sim_timeslice, decode_times=False)
            ds_ref_c = ds_ref.copy()
            ds = ds.fillna(0)
            print('len(ds.time): ',len(ds.time))
            print('len(ds_ref_c.time): ',len(ds_ref_c.time))
            if len(ds.time) < len(ds_ref_c.time):
                ds_ref_c = ds_ref_c.isel(time=slice(0,len(ds.time)))
                print('len(ds_ref_c.time): ',len(ds_ref_c.time))
            ds_ref_c["time"] = ds.time
            ds_ref_c = ds_ref_c.fillna(0)
            outfilesig=os.path.join(outdatadir,'significance_'+outfilename)

            ds_p = calculate_pvalue(ds, ds_ref_c, var)           
            print('outfilemean: ',outfilemean)
            ds_mean = xr.open_mfdataset(outfilemean, decode_times=False)
            
            ds_p[var+"_diff"] = ds_mean[var] - ds_hist_mean[var]
            save_xrdataset(ds_p, outfilesig)
            print("File written: ", outfilesig)
        
        else:
            print('read historical')
            ds_ref = xr.open_mfdataset(sim_timeslice, decode_times=False)
            ds_hist_mean = xr.open_mfdataset(outfilemean, decode_times=False) 
            ds_hist_mean = ds_hist_mean.drop_vars(["time", "time_bnds"], errors="ignore")
            ds_hist_mean = ds_hist_mean.squeeze()
    return

def calculate_ensemble_robustness(
        da_diff,
        da_sig,
        ensemble_dim,
        compute=True,
):
    def _where(
            da,
            rel_op,
            rel_value=0,
            then_value=1,
            else_value=0,
    ):
        if rel_op == ">":
            return xr.where(da > rel_value, then_value, else_value)
        if rel_op == "<":
            return xr.where(da < rel_value, then_value, else_value)
        if rel_op == "==":
            return xr.where(da == rel_value, then_value, else_value)
        raise ValueError("relational operator {} not known.".format(rel_op))

    def _percentage(da, da_ref, dim):
        da_s = da.sum(dim=dim)
        da_c = da_ref.count(dim=dim)
        return xr.where(da_c > 0, da_s / da_c, np.nan)
    
    diff_p = _where(da_diff, ">")
    diff_n = _where(da_diff, "<")
    #diff_0 = _where(ds[diff], "==")
    diff_p_p = _percentage(diff_p, da_diff, ensemble_dim)
    diff_n_p = _percentage(diff_n, da_diff, ensemble_dim)
    #diff_0_p = _percentage(diff_0, ds[diff], ensemble_dim)

    sig_p = _where(diff_p, "==", rel_value=1, then_value=da_sig)
    sig_n = _where(diff_n, "==", rel_value=1, then_value=da_sig)
    #sig_0 = _where(diff_0, "==", rel_value=1, then_value=ds[sig])
    sig_p_p = _percentage(sig_p, da_diff, ensemble_dim)
    sig_n_p = _percentage(sig_n, da_diff, ensemble_dim)
    #sig_0_p = _percentage(sig_0, ds[diff], ensemble_dim)

    da = xr.where(((diff_p_p >= 2/3) & (sig_p_p >= 1/2)), 1, 0)
    da = xr.where(((diff_n_p >= 2/3) & (sig_n_p >= 1/2)), -1, da)
    if compute is True:
        da = da.compute()
    return da

def ensemblemean_exp(outdatadir, var, var_pattern):
    ''' calculate mean for each scenario'''
    for timeslice in ['1991-2020','2031-2060', '2069-2098']:
        for exp in ['rcp26','rcp85']:
            outputfile = os.path.join(outdatadir, 'ENS_MEDIAN_' + var_pattern + '_' + exp + '_' + timeslice + '.nc')
            outputfile2 = os.path.join(outdatadir, 'ENS_MEAN_' + var_pattern + '_' + exp + '_' + timeslice + '.nc')
            
            ensemble_mean_files = glob.glob(os.path.join(outdatadir, 'MEAN_*' + var_pattern + '*' + exp + '*' + timeslice + '*.nc'))

            print(ensemble_mean_files)

            if len(ensemble_mean_files) == 0:
                print('No ensemble mean files found for:', exp, timeslice)
                continue

            mean_datasets = [xr.open_dataset(f, decode_times=False)[[var]] for f in ensemble_mean_files]
            result = xr.concat(mean_datasets, dim='ensemble').median(dim='ensemble', skipna=True)
            result2 = xr.concat(mean_datasets, dim='ensemble').mean(dim='ensemble', skipna=True)
            # save result to outputfile
            result.to_netcdf(outputfile)
            result2.to_netcdf(outputfile2)
            print('Ensemble median is calculated:', outputfile)
            print('Ensemble mean is calculated:', outputfile2)

            if timeslice != "1991-2020":

                ensemble_sig_files = glob.glob(os.path.join(outdatadir, 'significance_*' + var_pattern + '_*' + exp + '*' + timeslice + '*.nc'))

                datasets = []
                for ifile in ensemble_sig_files:
                    ds = xr.open_mfdataset(ifile, decode_times=False)
                    print('ifile =', ifile)
                    #
                    filename = os.path.basename(ifile)
                    #significance_compev_SU35_du3_DD_du5_AFR-22_MOHC-HadGEM2-ES_rcp85_r1i1p1_CLMcom-KIT-CCLM5-0-15_v1_day_GERICS_2031-2060_regridded_AFR22.nc
                    parts = filename.split('_')
                    RCM=parts[10]
                    GCM=parts[7]
                    print(GCM, RCM)
                    # compound events do not have attriobutes
                    #gcm = ds.attrs["driving_model_id"]
                    #rcm = ds.attrs["model_id"]
                    gcmrcm = "{}-{}".format(GCM, RCM)
                    ds = ds.assign_coords({"GCM-RCM": gcmrcm})
                    ds = ds.drop_vars([var, "p_value", "time", "time_bnds"], errors="ignore")
                    ds["significance"] = ds["significance"].expand_dims("GCM-RCM")
                    ds[var+"_diff"] = ds[var+"_diff"].expand_dims("GCM-RCM")
                    datasets += [ds]

                if len(datasets) == 0:
                    print('No significance files found for:', exp, timeslice)
                    continue

                ds_total = xr.concat(datasets, dim="GCM-RCM", data_vars=[var+"_diff", "significance"], compat="override", coords="minimal")
                #
                print('start to calculate ensemlbe robustness')
                ds_total["robustness"] = calculate_ensemble_robustness(
                    da_diff=ds_total[var+"_diff"],
                    da_sig=ds_total["significance"],
                    ensemble_dim="GCM-RCM",
                )
                ds_total[var+"_ensemble_mean_diff"] = ds_total[var+"_diff"].mean(dim="GCM-RCM")
                ds_total[var+"_ensemble_median_diff"] = ds_total[var+"_diff"].median(dim="GCM-RCM")
                outputfile = os.path.join(outdatadir, 'ENS_ROBUSTNESS_' +var_pattern+'_'+ timeslice + '_' + exp + '.nc')
                ds_total.to_netcdf(outputfile)
                print('Ensemble robustness is calculated:', outputfile)

    return