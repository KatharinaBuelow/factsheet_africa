#!/usr/bin/env python3
import xarray as xr

from format_data_tools import decode_time_pop, save_file_to_netcdf


def sel_time_mean(ds, start, end):
    return ds.sel(time=slice(start, end)).mean(dim="time")


def select_population_timeslice(pop_dir):
    """
    Select a time slice from a population dataset.
    
    
    """
    # The population data got remapped to arf22 grid in a separate script
    pop_ssp1 = xr.open_dataset(pop_dir+'/org/population_ssp1soc_2.5min_annual_1861-2100_africa22.nc4',decode_times=False)
    pop_ssp3 = xr.open_dataset(pop_dir+'/org/population_ssp3soc_2.5min_annual_1861-2100_africa22.nc4',decode_times=False) 
    #time axis needs to be defined for the population data
    pop_ssp1 = decode_time_pop(pop_ssp1)
    pop_ssp3 = decode_time_pop(pop_ssp3)

    pop_1991_2020_ssp1 = sel_time_mean(pop_ssp1, "1991-01-01", "2020-12-31")
    pop_2031_2060_ssp1 = sel_time_mean(pop_ssp1, "2031-01-01", "2060-12-31")
    pop_2069_2098_ssp1 = sel_time_mean(pop_ssp1, "2069-01-01", "2098-12-31")

    diff_pop_ssp1_2031_2060 = pop_2031_2060_ssp1 - pop_1991_2020_ssp1
    diff_pop_ssp1_2069_2098 = pop_2069_2098_ssp1 - pop_1991_2020_ssp1

    # Calculate mean population
    # 1991-2020 , 2031-2060 , 2069-2098
    pop_1991_2020_ssp3 = sel_time_mean(pop_ssp3, "1991-01-01", "2020-12-31")
    pop_2031_2060_ssp3 = sel_time_mean(pop_ssp3, "2031-01-01", "2060-12-31")
    pop_2069_2098_ssp3 = sel_time_mean(pop_ssp3, "2069-01-01", "2098-12-31")

    diff_pop_ssp3_2031_2060 = pop_2031_2060_ssp3 - pop_1991_2020_ssp3
    diff_pop_ssp3_2069_2098 = pop_2069_2098_ssp3 - pop_1991_2020_ssp3

    save_file_to_netcdf(pop_1991_2020_ssp1, pop_dir, '/pop_1991_2020_ssp1.nc')
    save_file_to_netcdf(pop_2031_2060_ssp1, pop_dir, '/pop_2031_2060_ssp1.nc')
    save_file_to_netcdf(pop_2069_2098_ssp1, pop_dir, '/pop_2069_2098_ssp1.nc')

    save_file_to_netcdf(pop_1991_2020_ssp3, pop_dir, '/pop_1991_2020_ssp3.nc')
    save_file_to_netcdf(pop_2031_2060_ssp3, pop_dir, '/pop_2031_2060_ssp3.nc')
    save_file_to_netcdf(pop_2069_2098_ssp3, pop_dir, '/pop_2069_2098_ssp3.nc')

    save_file_to_netcdf(diff_pop_ssp1_2031_2060, pop_dir, '/pop_diff_2031_2060_ssp1.nc')
    save_file_to_netcdf(diff_pop_ssp3_2031_2060, pop_dir, '/pop_diff_2031_2060_ssp3.nc')
    save_file_to_netcdf(diff_pop_ssp1_2069_2098, pop_dir, '/pop_diff_2069_2098_ssp1.nc')
    save_file_to_netcdf(diff_pop_ssp3_2069_2098, pop_dir, '/pop_diff_2069_2098_ssp3.nc')

    return 