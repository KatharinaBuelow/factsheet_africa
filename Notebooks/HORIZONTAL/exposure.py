#!/usr/bin/env python3
import xarray as xr

def diff_exposure(pop_ref, index_ref, diff_pop, diff_index, var):
    """
    Calculate the change of exposure of a person 
    to changing climate variable and change in  population
    literature: Liu et al. , 2016, Weber et al. 2020,
    """
    # Calculate the exposure
    p_ref = xr.open_dataset(pop_ref,decode_timedelta=False)
    diff_p = xr.open_dataset(diff_pop,decode_timedelta=False)
    i_ref = xr.open_dataset(index_ref,decode_timedelta=False)
    diff_i = xr.open_dataset(diff_index,decode_timedelta=False)

    exp = xr.Dataset()
    exp['exposure'] = p_ref['number_of_people'] * diff_i[var] + i_ref[var] * diff_p['number_of_people'] + diff_i[var] * diff_p['number_of_people']

    return exp
