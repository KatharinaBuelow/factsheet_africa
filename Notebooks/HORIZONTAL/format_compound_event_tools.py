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


import os
import numpy as np
import pandas as pd
import xarray as xr

try:
    import numba as nb
    _HAS_NUMBA = True
except ModuleNotFoundError:
    _HAS_NUMBA = False


if _HAS_NUMBA:
    @nb.njit(parallel=True, fastmath=True)
    def _annual_sum_with_carry_3d(arr, start_year_idx, days_left_start, year_lengths):
        # arr: (time, rlat, rlon)
        nt, ny, nx = arr.shape
        nyears = len(year_lengths)
        out = np.zeros((nyears, ny, nx), dtype=np.float32)

        for j in nb.prange(ny):
            for i in range(nx):
                for t in range(nt):
                    v = arr[t, j, i]
                    if not np.isfinite(v) or v <= 0:
                        continue

                    rem = v
                    yi = start_year_idx[t]

                    add = rem if rem < days_left_start[t] else days_left_start[t]
                    out[yi, j, i] += add
                    rem -= add
                    yi += 1

                    while rem > 0 and yi < nyears:
                        yl = year_lengths[yi]
                        add = rem if rem < yl else yl
                        out[yi, j, i] += add
                        rem -= add
                        yi += 1
        return out
else:
    def _annual_sum_with_carry_3d(arr, start_year_idx, days_left_start, year_lengths):
        # arr: (time, rlat, rlon)
        nt, ny, nx = arr.shape
        nyears = len(year_lengths)
        out = np.zeros((nyears, ny, nx), dtype=np.float32)

        for j in range(ny):
            for i in range(nx):
                for t in range(nt):
                    v = arr[t, j, i]
                    if not np.isfinite(v) or v <= 0:
                        continue

                    rem = v
                    yi = int(start_year_idx[t])

                    add = rem if rem < days_left_start[t] else days_left_start[t]
                    out[yi, j, i] += add
                    rem -= add
                    yi += 1

                    while rem > 0 and yi < nyears:
                        yl = year_lengths[yi]
                        add = rem if rem < yl else yl
                        out[yi, j, i] += add
                        rem -= add
                        yi += 1
        return out


# --- calendar-aware helpers ---
def _is_leap_year(year, calendar="standard"):
    cal = str(calendar).lower()
    if cal in ("noleap", "365_day", "360_day"):
        return False
    if cal in ("all_leap", "366_day"):
        return True
    if cal == "julian":
        return year % 4 == 0
    return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))


def _days_in_year(year, calendar="standard"):
    cal = str(calendar).lower()
    if cal == "360_day":
        return 360
    if cal in ("noleap", "365_day"):
        return 365
    if cal in ("all_leap", "366_day"):
        return 366
    return 366 if _is_leap_year(year, cal) else 365


def _extract_year_doy(d):
    """Return (year, day_of_year) for cftime, datetime, pandas, or numpy datetime64."""
    if hasattr(d, "year"):
        year = int(d.year)
        if hasattr(d, "dayofyr"):
            return year, int(d.dayofyr)
        return year, int(d.timetuple().tm_yday)

    ts = pd.Timestamp(d)
    return int(ts.year), int(ts.dayofyear)


def annual_sum_with_carry_grid_fast(src_ds, outfile, out_var_name="ev_coin_du_days", dates=None):
    
    da=src_ds['ev_coin_du']
    if "time" not in da.dims:
        raise ValueError("Input DataArray must have a 'time' dimension.")

    time_calendar = (
        da["time"].attrs.get("calendar")
        or da["time"].encoding.get("calendar")
        or "standard"
    )

    if dates is None:
        time_values = da["time"].values
        if np.issubdtype(np.asarray(time_values).dtype, np.number):
            time_units = da["time"].attrs.get("units", da["time"].encoding.get("units", None))
            if time_units is None:
                raise ValueError("Numeric time axis found, but no time units available in attrs/encoding.")
            dates = xr.coding.times.decode_cf_datetime(
                time_values,
                units=time_units,
                calendar=time_calendar,
            )
        else:
            # Keep native index values (works for DatetimeIndex and CFTimeIndex)
            idx = da.indexes.get("time", None)
            if idx is not None:
                dates = np.asarray(idx.values)
            else:
                dates = np.asarray(time_values)

    if len(dates) != da.sizes["time"]:
        raise ValueError("Length of 'dates' must match size of da.time.")

    year_doy = np.array([_extract_year_doy(d) for d in dates], dtype=np.int32)
    years = year_doy[:, 0]
    doy = year_doy[:, 1].astype(np.int16)

    unique_years = np.unique(years)
    year_to_idx = {y: i for i, y in enumerate(unique_years)}
    start_year_idx = np.array([year_to_idx[y] for y in years], dtype=np.int32)

    year_lengths = np.array([_days_in_year(int(y), time_calendar) for y in unique_years], dtype=np.float32)
    days_left_start = (year_lengths[start_year_idx] - doy + 1).astype(np.float32)

    if all(d in da.dims for d in ("time", "rlat", "rlon")):
        y_dim, x_dim = "rlat", "rlon"
        da_t = da.transpose("time", y_dim, x_dim)
    elif all(d in da.dims for d in ("time", "x", "y")):
        y_dim, x_dim = "x", "y"
        da_t = da.transpose("time", y_dim, x_dim)
    elif all(d in da.dims for d in ("time", "lat", "lon")):
        y_dim, x_dim = "lat", "lon"
        da_t = da.transpose("time", y_dim, x_dim)
    else:
        raise ValueError(
            f"Unsupported dimensions {da.dims}. Expected ('time','rlat','rlon') or ('time','x','y') or ('time','lat','lon')."
        )
    arr = np.asarray(da_t.values, dtype=np.float32)

    out = _annual_sum_with_carry_3d(arr, start_year_idx, days_left_start, year_lengths)

    annual_da = xr.DataArray(
        out,
        dims=("year", y_dim, x_dim),
        coords={"year": unique_years, y_dim: da_t[y_dim], x_dim: da_t[x_dim]},
        name=out_var_name,
        attrs={
            "long_name": "annual sum of ev_coin_du with cross-year carry-over",
            "units": "days",
            "calendar": time_calendar,
        },
    )

    ds_out = annual_da.to_dataset()

    # Convert dimension from "year" to CF-compliant "time" and write to NetCDF
    cal_lower = str(time_calendar).lower()
    years_out = ds_out["year"].values.astype(int)

    ds_out = ds_out.rename({"year": "time"})

    if cal_lower in {"noleap", "365_day"}:
        time_vals = [cftime.DatetimeNoLeap(int(y), 1, 1) for y in years_out]
    elif cal_lower in {"all_leap", "366_day"}:
        time_vals = [cftime.DatetimeAllLeap(int(y), 1, 1) for y in years_out]
    elif cal_lower == "360_day":
        time_vals = [cftime.Datetime360Day(int(y), 1, 1) for y in years_out]
    elif cal_lower == "julian":
        time_vals = [cftime.DatetimeJulian(int(y), 1, 1) for y in years_out]
    else:
        # standard/gregorian/proleptic_gregorian
        time_vals = pd.to_datetime([f"{int(y)}-01-01" for y in years_out])

    # Do not store an auxiliary year coordinate
    ds_out = ds_out.assign_coords(time=("time", time_vals))
    ds_out["time"].attrs = {
        "standard_name": "time",
        "long_name": "time",
        "axis": "T",
    }

    write_calendar = "proleptic_gregorian" if cal_lower in {"standard", "gregorian"} else cal_lower
    ds_out["time"].encoding = {
        "units": "days since 1900-01-01 00:00:00",
        "calendar": write_calendar,
    }

    if src_ds is not None:
        for extra_name in ("lat", "lon", "lat_bnds", "lon_bnds"):
            if extra_name in src_ds.data_vars:
                ds_out[extra_name] = src_ds[extra_name]
            elif extra_name in src_ds.coords:
                ds_out = ds_out.assign_coords({extra_name: src_ds.coords[extra_name]})

        grid_mapping_name = annual_da.attrs.get("grid_mapping", None)
        if grid_mapping_name and grid_mapping_name in src_ds.variables and grid_mapping_name not in ds_out.variables:
            ds_out[grid_mapping_name] = src_ds[grid_mapping_name]

    encoding = {out_var_name: {"zlib": True, "complevel": 4, "dtype": "float32"}}
    try:
        ds_out.to_netcdf(outfile, engine="netcdf4", encoding=encoding)
    except Exception:
        ds_out.to_netcdf(outfile)

    return ds_out
