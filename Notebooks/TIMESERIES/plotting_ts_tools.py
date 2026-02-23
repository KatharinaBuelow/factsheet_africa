#!/usr/bin/env python3
# plotting tool for time series

from operator import index
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import os  
import sys
import numpy as np  


# Consistent dark grey for lines previously using 'black'
DARKGREY = "#525151"

def select_index(idx: str):
    index_meta = {
        'TG': {
            'longname': 'mean temperature [°C]',
            'longnameK': 'mean temperature [K]',
            'unit_base': '°C',
            'unit_alt': 'K',
            'description': 'Near-surface air temperature'
        },
        'R20mm': {
            'longname': 'number of days with pr > 20 mm per day',
            'unit_base': 'days',
            'description': 'Heavy precipitation days (>=20 mm)'
        },
        'DD': {
            'longname': 'number of dry days',
            'unit_base': 'days',
            'description': 'Dry days (precipitation < 1 mm/day)'
        },
        'SU40': {
            'longname': 'number of days with Tmax > 40°C',
            'unit_base': 'days',
            'description': 'Very hot days'
        },
        'TR26': {
            'longname': 'number of days with Tmin > 26°C',
            'unit_base': 'days',
            'description': 'Tropical nights (warm minimum temperature)'
        }
    }

    if idx not in index_meta:
        # Fallback: return None if index not found
        print(f"Warning: Index '{idx}' not recognized. Available indices: {list(index_meta.keys())}")
        return None
    meta = index_meta[idx]
    
    return meta


def cleanup(data, index, longname, longnameK):
    # adjust dataframe for plotting
    # drop column ci_package_name
    data = data.drop(columns=['ci_package_name', 'ci_package_reference'])
    # rename columns
    if index == 'TG':
        data = data.rename(columns={'time': 'year', 'value': longnameK})
        data['mean temperature [°C]'] = data['mean temperature [K]'] - 273.15
    else:
        data = data.rename(columns={'time': 'year', 'value': longname})

    # some new columns
    data['GCM'] = data['realization'].str.split('_').str[3]
    data['RCM'] = data['realization'].str.split('_').str[2]
    data['scenario'] = data['realization'].str.split('_').str[4]
    data['realization'].unique()

    data['year'] = pd.to_datetime(data['year'], format='%Y-%m-%d')

    return data

def adjust_names(data):
    # Some names need fixing: rename RCMs // GCMs
    data['RCM'] = data['RCM'].replace({'ICTP-RegCM4-7-0ICTP-RegCM4-7': 'ICTP-RegCM4-7'})
    data['GCM'] = data['GCM'].replace({'MPI-M-MPI-ESM-MRMPI-M-MPI-ESM-MR': 'MPI-M-MPI-ESM-MR',
                                         'NCC-NorESM1-MNCC-NorESM1-M': 'NCC-NorESM1-M',})
    return data

def adjust_length(data, start_date, end_date):
    # Cut data to common period 1971-2098
    # start_date = '1971-01-01'
    # end_date = '2098-12-31'
    mask = (data['year'] >= start_date) & (data['year'] <= end_date)
    return data[mask]

def calculate_anomaly_timeslice (df, slices_to_use):
    anom_slice_means=[]

    # Robust year accessor (int or datetime)
    year_series = df["year"]
    if pd.api.types.is_datetime64_any_dtype(year_series):
        year_values = year_series.dt.year
    else:
        year_values = pd.to_numeric(year_series, errors="coerce")
    slice_stats = []

    for name, start_year, end_year in slices_to_use:
        idx = (year_values >= start_year) & (year_values <= end_year)
        sel = df.loc[idx].copy()  # keep 'year' for aggregation
        if sel.empty:
            continue
        grp = sel.groupby(["realization", "scenario","region","standard_name"], as_index=False).agg(
            anomaly_mean=("anomaly", "mean"),
            years=("year", "nunique")
        )
        grp["slice"] = name
        slice_stats.append(grp)
    anom_slice_means = (
        pd.concat(slice_stats, ignore_index=True)
        if slice_stats
        else pd.DataFrame(columns=["slice", "region", "standard_name", "realization", "scenario", "anomaly_mean", "years"])
        )
    anom_slice_means = anom_slice_means[["slice", "region", "standard_name", "realization", "scenario", "anomaly_mean", "years"]]
    
    return anom_slice_means


def calculate_anomaly(df, baseline_start, baseline_end, value_col):
    """Calculate anomalies relative to a baseline period per realization and add running means.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: 'year' (date-like or year), 'realization', value_col.
    baseline_start, baseline_end : str or datetime-like
        Inclusive start/end of baseline period (e.g. '1991-01-01', '2020-12-31').
    value_col : str
        Column name with the variable values (e.g. 'mean temperature [°C]').

    Returns
    -------
    pd.DataFrame
        Original dataframe with added columns:
        'year' (int), 'mean_ref', 'anomaly', 'running_mean_10yr', 'running_mean_30yr'.
    """
    df = df.copy()

    # Ensure year numeric (accept either YYYY or date strings)
    if df['year'].dtype == 'O' or str(df['year'].dtype).startswith(('datetime', 'object')):
        # Try parse to datetime then extract year
        try:
            years_parsed = pd.to_datetime(df['year'], errors='coerce')
            df['year'] = years_parsed.dt.year
        except Exception:
            raise ValueError("Column 'year' could not be parsed to datetime to extract year.")

    # Convert baseline boundaries to years (handle if strings with date)
    bstart_year = pd.to_datetime(baseline_start).year
    bend_year = pd.to_datetime(baseline_end).year

    if bstart_year > bend_year:
        raise ValueError("baseline_start must be <= baseline_end")

    # Reference subset
    mask_ref = (df['year'] >= bstart_year) & (df['year'] <= bend_year)
    df_ref = df.loc[mask_ref].copy()
    if df_ref.empty:
        raise ValueError("Baseline selection produced no rows. Check baseline years overlap data range.")

    required_cols = {'realization', value_col}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Mean per realization over baseline
    mean_per_realization = (
        df_ref.groupby('realization', as_index=False)[value_col]
        .mean()
        .rename(columns={value_col: 'mean_ref'})
    )

    # Map baseline mean back
    df = df.merge(mean_per_realization, on='realization', how='left')

    # Compute anomaly
    df['anomaly'] = df[value_col] - df['mean_ref']

    # Sort for running means
    df = df.sort_values(['realization', 'year'])

    # Running means (use center=False so trailing window; adjust if centered desired)
    df['running_mean_10yr'] = (
        df.groupby('realization')['anomaly']
          .transform(lambda x: x.rolling(window=10, min_periods=10).mean())
    )
    df['running_mean_30yr'] = (
        df.groupby('realization')['anomaly']
          .transform(lambda x: x.rolling(window=30, min_periods=30).mean())
    )

    return df

####################
# line plot function
#####################

def line_plot(data,x,y,explore,index, outputpath):
    print(explore)
    # Define unique styles
    colors = ['darkblue', 'darkred','green', 'orange', 'purple', 'brown', 'pink']
    marker_styles = ['o', 'x', '^']
    line_styles = ['-', ':', '--',':']
    # Create unique mappings
    scenarios = data['scenario'].unique()
    gcms = data['GCM'].unique()
    rcms = data['RCM'].unique()
    plt.figure(figsize=(12, 8))
    
    if explore =='GCMcolor': 
        color_map = dict(zip(gcms, colors))
        linestyle_map = dict(zip(scenarios, line_styles))
        marker_map = dict(zip(rcms, marker_styles))
        for (scenario, gcm, rcm), group in data.groupby(['scenario', 'GCM', 'RCM']):
            plt.plot(
                group[x], group[y],
                label=f'{scenario} | {gcm} | {rcm}',
                color=color_map[gcm],
                linestyle=linestyle_map[scenario],
                marker=None,
                alpha=0.5,
                markersize=4,
                linewidth=2
            )

    elif explore =='RCMcolor':
        color_map = dict(zip(rcms, colors))
        linestyle_map = dict(zip(scenarios, line_styles))
        marker_map = dict(zip(rcms, marker_styles))
        for (scenario, gcm, rcm), group in data.groupby(['scenario', 'GCM', 'RCM']):
            plt.plot(
                group[x], group[y],
                label=f'{scenario} | {gcm} | {rcm}',
                color=color_map[rcm],
                linestyle=linestyle_map[scenario],
                marker=None,
                alpha=0.5,
                markersize=4,
                linewidth=1.5
                )

    elif explore =='Scenario':
        color_map = dict(zip(scenarios, colors))
        linestyle_map = dict(zip(gcms, line_styles))
        marker_map = dict(zip(rcms, marker_styles))
    
    
    # Create the plot
        
        for (scenario, gcm, rcm), group in data.groupby(['scenario', 'GCM', 'RCM']):
            plt.plot(
                group[x], group[y],
                label=f'{scenario} | {gcm} | {rcm}',
                color=color_map[scenario],
                linestyle=linestyle_map[gcm],
                marker=marker_map[rcm],
                alpha=0.5,
                markersize=4,
                linewidth=1
            )
    else:
        raise ValueError("Invalid value for 'explore'. Must be 'GCM', 'RCM', or 'Scenario'.")
    
    plt.title('WASCAL region area mean temperature')
    plt.legend(title='CORDEX AFR22 Realization', loc='upper left', ncol=1, fontsize=8)
    plt.tight_layout()
    plt.xticks(rotation=0)
    plt.xlabel(x)
    plt.ylabel(y)
    # rename x and y for plotname
    x=x.replace(' ', '_')
    y=y.replace(' ', '_')
    # save plot
    outfile = os.path.join(outputpath,'line_plot_'+x+'_'+index+'_'+explore+'.png')
    plt.savefig(outfile, dpi=1200, bbox_inches='tight', pad_inches=0.3)
    
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')    
    return plt.show()

#############################
# line plot min max function
#############################

def line_plot_min_max(df, x, y, index,outputpath, region, dfera5=None, ylim=None):
    """Plot median time series with min-max shading per scenario.

    Parameters
    ----------
    df : DataFrame with columns ['year','scenario', y]
    x : str, name of x column (typically 'year')
    y : str, name of value column
    outputpath : str, directory to save plot
    region : str, region name for title
    era5 : bool, whether to use ERA5 data
    dfera5 : DataFrame, optional ERA5 data for comparison
    ylim : tuple(float,float) or None, optional y-limits; if None auto-scale
    """
    if y not in df.columns:
        raise ValueError(f"Column '{y}' not found in dataframe. Available: {list(df.columns)}")
    if 'scenario' not in df.columns:
        raise ValueError("Dataframe must contain column 'scenario'.")
    if x not in df.columns:
        raise ValueError(f"Column '{x}' not found in dataframe.")

    print('Plotting column: ', y)
    # Ensure year numeric for plotting
    if np.issubdtype(df[x].dtype, np.datetime64):
        _df = df.copy()
        _df[x] = _df[x].dt.year
    else:
        _df = df.copy()

    grouped = _df.groupby([x, 'scenario'])[y]
    median = grouped.median().unstack()
    min_values = grouped.min().unstack()
    max_values = grouped.max().unstack()

    scenario_colors = {'rcp26': 'darkblue', 'rcp85': 'darkred'}

    plt.figure(figsize=(12, 6))
    
    for scenario in median.columns:
        color = scenario_colors.get(scenario, None)
        if color is None:
            # assign a fallback color
            color = plt.cm.tab10(list(median.columns).tolist().index(scenario) % 10)
        plt.plot(median.index, median[scenario], label=f'{scenario} median', color=color, linewidth=2)
        plt.fill_between(median.index, min_values[scenario], max_values[scenario], alpha=0.15, color=color, label=f'{scenario} range')
        # Optional min/max dashed outlines
        plt.plot(median.index, min_values[scenario], linestyle='--', linewidth=0.6, color=color, alpha=0.7)
        plt.plot(median.index, max_values[scenario], linestyle='--', linewidth=0.6, color=color, alpha=0.7)
        print(x, y)
    if dfera5 is not None:
        # Prepare ERA5 frame to ensure required columns exist
        if x not in dfera5.columns:
            raise ValueError(f"ERA5 dataframe missing column '{x}'. Columns available: {list(dfera5.columns)}")
        if y not in dfera5.columns:
            raise ValueError(f"ERA5 dataframe missing column '{y}'. Columns available: {list(dfera5.columns)}")
        era5_years = dfera5[x]
        # If datetime, convert
        if np.issubdtype(era5_years.dtype, np.datetime64):
            era5_years = era5_years.dt.year
        plt.plot(era5_years, dfera5[y], label='ERA5', color=DARKGREY, linewidth=2.5, zorder=5)
            
    plt.title(f"Area mean for {region}: of {y}", fontsize=20)
    plt.legend(title='CORDEX AFR22 Realizations', loc='upper left', ncol=1, fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.xticks(rotation=0)
    plt.xlabel(x, fontsize=14)
    plt.ylabel(y, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=12)

    # Y limits: if not provided and looks like temperature 
    # in °C, set a sensible span
    if ylim is not None:
        plt.ylim(*ylim)
    else:
        # Auto with small padding
        ymin, ymax = plt.ylim()
        span = ymax - ymin
        plt.ylim(ymin - 0.02 * span, ymax + 0.02 * span)

    # Reference verticals (hard-coded years for now)
    plt.xlim(1971, 2100)
    for yr in (1991, 2020):
        plt.axvline(yr, color='grey', linestyle='-', linewidth=1)
    plt.fill_betweenx(y=plt.ylim(), x1=1991, x2=2020, color='grey', alpha=0.08)
    plt.text(1991 + 1, plt.ylim()[0] + 0.02 * (plt.ylim()[1]-plt.ylim()[0]), 'Reference (1991-2020)', color='grey', fontsize=14)
     #
    # Save
    safe_x = x.replace(' ', '_')
    #
    safe_region = region.replace(' ', '_')
    if dfera5 is not None:
        outfile = os.path.join(outputpath, f'line_plot_min_max_{index}_{safe_x}_{safe_region}_ERA5.png')
    else:
        outfile = os.path.join(outputpath, f'line_plot_min_max_{index}_{safe_x}_{safe_region}.png')
    plt.savefig(outfile, dpi=1200, bbox_inches='tight', pad_inches=0.3)
    print('Saved plot to: ', outfile)
    return plt.show()

#############################
# Load RCMS data
#############################

def load_rcms_csv(csv_path, country, index, longname, start_date=None, end_date=None, longnameK=None):
    """Load a CORDEX AFR-22 country-averaged CSV and return a tidy DataFrame for plotting.

    Expected minimal columns in the CSV: ['region','time','value'] OR already a
    renamed value column. The function will:
      * filter the selected country (exact match on 'region')
      * rename 'time' -> 'year'
      * for index 'TG' convert Kelvin to Celsius if both longnameK and longname provided
      * return DataFrame with columns ['year', longname]

    Parameters
    ----------
    csv_path : str
        Path to CORDEX AFR-22 CSV (e.g. climdexCORDEX_AFR22_TG_year_weighted_means.csv)
    country : str
        Country name to filter (as used in 'region' column)
    index : str
        Index identifier (e.g. 'TG')
    longname : str
        Target long name column for plotting (e.g. 'mean temperature [°C]')
    longnameK : str, optional
        Column name holding Kelvin values when index == 'TG'

    Returns
    -------
    pd.DataFrame
        Columns: 'year' (int), longname (float)
    """
    df = pd.read_csv(csv_path)
    if 'region' not in df.columns:
        raise ValueError("CORDEX AFR-22 CSV must contain a 'region' column for country filtering.")
    df = df[df['region'] == country]
    if df.empty:
        raise ValueError(f"No CORDEX AFR-22 rows found for country '{country}'.")

    # If 'time' column exists, rename to 'year'
    if 'time' in df.columns:
        df = df.rename(columns={'time': 'year'})
    if 'year' not in df.columns:
        raise ValueError("CORDEX AFR-22 CSV needs a 'time' or 'year' column.")

    # Convert to datetime then extract year number if not already int
    #if not np.issubdtype(df['year'].dtype, np.integer):
    #    try:
    #        df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year
    #    except Exception:
    #        raise ValueError("Could not parse year values in CORDEX AFR-22 CSV.")

    
    rcm_clean=cleanup(df, index, longname, longnameK)
    rcm_clean=adjust_names(rcm_clean)
    cut_data=adjust_length(rcm_clean, start_date, end_date)
    return cut_data


#############################
# ERA5 helper loader
#############################

def load_era5_csv(csv_path, country, index, longname, start_date=None, longnameK=None):
    """Load an ERA5 country-averaged CSV and return a tidy DataFrame for plotting.

    Expected minimal columns in the CSV: ['region','time','value'] OR already a
    renamed value column. The function will:
      * filter the selected country (exact match on 'region')
      * rename 'time' -> 'year'
      * for index 'TG' convert Kelvin to Celsius if both longnameK and longname provided
      * return DataFrame with columns ['year', longname]

    Parameters
    ----------
    csv_path : str
        Path to ERA5 CSV (e.g. climdexERA5_TG_year_weighted_means.csv)
    country : str
        Country name to filter (as used in 'region' column)
    index : str
        Index identifier (e.g. 'TG')
    longname : str
        Target long name column for plotting (e.g. 'mean temperature [°C]')
    longnameK : str, optional
        Column name holding Kelvin values when index == 'TG'

    Returns
    -------
    pd.DataFrame
        Columns: 'year' (int), longname (float)
    """
    df = pd.read_csv(csv_path)
    if 'region' not in df.columns:
        raise ValueError("ERA5 CSV must contain a 'region' column for country filtering.")
    df = df[df['region'] == country]
    if df.empty:
        raise ValueError(f"No ERA5 rows found for country '{country}'.")

    # If 'time' column exists, rename to 'year'
    if 'time' in df.columns:
        df = df.rename(columns={'time': 'year'})
    if 'year' not in df.columns:
        raise ValueError("ERA5 CSV needs a 'time' or 'year' column.")

    # Convert to datetime then extract year number if not already int
    #if not np.issubdtype(df['year'].dtype, np.integer):
    #    try:
    #        df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year
    #    except Exception:
    #        raise ValueError("Could not parse year values in ERA5 CSV.")

    
    era5_clean=cleanup(df, index, longname, longnameK)
    era5_clean=adjust_names(era5_clean)
    era5_cut= adjust_length(era5_clean, start_date, '2023-12-31')
    
    return era5_cut

################################
# line plot anomaly function
################################

def line_plot_anomaly(data,x,y,outputpath, group, country, index, longname,era5=None,ylim=None):
    """make line plot of anomaly

    you can either have each realisation in it own color 
    or 
    if group equals scenario, each scenario has its own color 
    ylim : tuple(float,float) or None, optional y-limits; if None auto-scale
    """
    plt.figure(figsize=(12, 6))
    
    # colors:
    colors = ['darkblue', 'darkred']
    marker_styles = ['o', 'x', '^']
    line_styles = ['-', ':', '--',':']
    scenarios = data['scenario'].unique()
    gcms = data['GCM'].unique()
    rcms = data['RCM'].unique()
    color_map = dict(zip(scenarios, colors))
    linestyle_map = dict(zip(gcms, line_styles))
    marker_map = dict(zip(rcms, marker_styles))

    
    if group =='scenario':
        # Create the plot
        for (scenario, gcm, rcm), group in data.groupby(['scenario', 'GCM', 'RCM']):
            plt.plot(
            group[x], group[y],
            label=f'{scenario} | {gcm} | {rcm}',
            color=color_map[scenario],
            linestyle=linestyle_map[gcm],
            marker=marker_map[rcm],
            alpha=0.5,
            markersize=4,
            linewidth=1
            )
    elif group =='scenario_min_max':
        grouped = data.groupby([x, 'scenario'])[y]
        median = grouped.median().unstack()
        min_values = grouped.min().unstack()
        max_values = grouped.max().unstack()
        for scenario in median.columns:
            plt.plot(median.index, median[scenario], label=f'{scenario} median', color=color_map[scenario], linewidth=2)
            plt.fill_between(median.index, min_values[scenario], max_values[scenario], alpha=0.15, color=color_map[scenario], label=f'{scenario} range')
            # min/max dashed outlines
            plt.plot(median.index, min_values[scenario], linestyle='--', linewidth=0.6, color=color_map[scenario], alpha=0.7)
            plt.plot(median.index, max_values[scenario], linestyle='--', linewidth=0.6, color=color_map[scenario], alpha=0.7)
    else:
        for realization, group in data.groupby('realization'):
            plt.plot(
            group[x],
            group[y],
            label=realization
        )
    if era5 is not None:
        # Prepare ERA5 frame to ensure required columns exist
        if x not in era5.columns:
            raise ValueError(f"ERA5 dataframe missing column '{x}'. Columns available: {list(era5.columns)}")
        if y not in era5.columns:
            raise ValueError(f"ERA5 dataframe missing column '{y}'. Columns available: {list(era5.columns)}")
        era5_years = era5[x]
        # If datetime, convert
        if np.issubdtype(era5_years.dtype, np.datetime64):
            era5_years = era5_years.dt.year
        plt.plot(era5_years, era5[y], label='ERA5', color=DARKGREY, linewidth=2.5, zorder=5)
    
    # title, labels
    plt.title(f"Area mean for {country}: {y} of {longname}", fontsize=20)
    plt.legend(title='CORDEX AFR22 Realization', loc='upper left', ncol=1, fontsize=8)
    plt.tight_layout()
    plt.xticks(rotation=0)
    plt.xlabel(x, fontsize=14)
    plt.ylabel(y+' of '+longname, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    # Y limits: 
    if ylim is not None:
        plt.ylim(*ylim)
        ytext=ylim[0]+0.1
    else:
        # Auto with small padding
        ymin, ymax = plt.ylim()
        span = ymax - ymin
        plt.ylim(ymin - 0.02 * span, ymax + 0.02 * span)
        ytext=ymin+0.1
    plt.xlim(1970, 2100)
    plt.axhline(0, color=DARKGREY, linestyle='-', linewidth=1)
    plt.axvline(1991, color='grey', linestyle='-', linewidth=1)
    plt.axvline(2020, color='grey', linestyle='-', linewidth=1)
    # Fill between the vertical lines for the reference period
    plt.fill_betweenx(
        y=plt.ylim(), 
        x1=1991, 
        x2=2020, 
        color='lightgrey', 
        alpha=0.1
    )
    # Add a legend for the shaded area
    plt.text(1992, ytext, 'Reference (1991-2020)', color='grey', fontsize=14)
    # rename x and y for plotname
    x=x.replace(' ', '_')
    y=y.replace(' ', '_')
    country=country.replace(' ', '_')
    # save plot
    if era5 is not None:
        outfile = os.path.join(outputpath,'line_plot_'+group+'_'+x+'_'+index+'_'+y+'_'+country+'_ERA5.png')
    else:
        outfile = os.path.join(outputpath,'line_plot_'+group+'_'+x+'_'+index+'_'+y+'_'+country+'.png')
    plt.savefig(outfile, bbox_inches='tight' ,pad_inches=0.3, dpi=1200)
    print('file liegt: ', outfile)
    
    return plt.show()

def box_plot_anomaly(src, outputpath, country, var, longname):

    # Use scenario-based colors
    palette = {"rcp26": "lightblue", "rcp85": "lightcoral"}
    inner_palette= {"rcp26": "darkblue", "rcp85": "darkred"}

    # Ensure consistent hue order from data to match the palette keys
    hue_order = [k for k in palette.keys() if k in src["scenario"].unique().tolist()]
    # Consistent order for slices on the x-axis
    slice_order = sorted(src["slice"].unique().tolist())

    # Calculate spacing so columns are evenly distributed
    n_slices = len(slice_order)
    n_hues = len(hue_order)
    total_columns = n_slices * n_hues
    x_positions = []
    for i, s in enumerate(slice_order):
        for j, h in enumerate(hue_order):
            x_positions.append(i * n_hues + j)
    #slice_pos = {s: i * n_hues for i, s in enumerate(slice_order)}

    # Summary stats per slice/scenario
    stats = (
        src.groupby(["slice", "scenario"])["anomaly_mean"]
        .agg(
            ymin="min",
            ymax="max",
            p15=lambda s: s.quantile(0.15),
            p85=lambda s: s.quantile(0.85),
            median="median",
            n="size",
        )
        .reset_index()
    )

    # Plot
    fig, ax = plt.subplots(figsize=(8,8))

    base_width = 0.4
    inner_width = base_width #* 0.8

    for idx, row in stats.iterrows():
        s = row["slice"]
        h = row["scenario"]
        if h not in hue_order:
            continue
    # Find x position for each column
        x_center = slice_order.index(s) * n_hues + hue_order.index(h)
    # Min–Max box (light)
        ax.add_patch(Rectangle(
            (x_center - base_width / 2, row["ymin"]),
            base_width,
            row["ymax"] - row["ymin"],
            facecolor=palette[h],
            edgecolor=inner_palette[h],
            alpha=0.35
        ))
    # P15–P85 box (dark)
        ax.add_patch(Rectangle(
            (x_center - inner_width / 2, row["p15"]),
            inner_width,
            row["p85"] - row["p15"],
            facecolor=inner_palette[h],
            edgecolor=inner_palette[h],
            alpha=0.7
        ))
    # Median line
        ax.hlines(row["median"], x_center - inner_width / 2, x_center + inner_width / 2, colors="lightgray", linewidth=2)
    # Extend x-axis limits by base_width/2 for visual padding
        ax.set_xlim(-base_width, total_columns  -base_width )
    # Axes formatting
    xticks = [slice_order.index(s) * n_hues + j for s in slice_order for j in range(n_hues)]
    xticklabels = [f"{s}\n{h}" for s in slice_order for h in hue_order]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    #ax.set_xlabel("Time Slice / Scenario")
    ax.set_ylabel(f"{country}: {longname} anomaly to 1991-2020")
    # Build legend
    if hue_order:
        legend_handles = []
        for h in hue_order:
            legend_handles.append(
                Patch(facecolor=palette[h], edgecolor=inner_palette[h], alpha=0.35, label=f"Min-Max ({h})")
            )
            legend_handles.append(
                Patch(facecolor=inner_palette[h], edgecolor=inner_palette[h], alpha=0.7, label=f"P15–P85 ({h})")
            )
        legend_handles.append(
            plt.Line2D([0], [0], color="lightgray", lw=2, label="Median")
        )
        ax.legend(handles=legend_handles)
    # Add values of min, max, p85, p15, and median to each box-plot
    for idx, row in stats.iterrows():
        s = row["slice"]
        h = row["scenario"]
        if h not in hue_order:
            continue
        x_center = slice_order.index(s) * n_hues + hue_order.index(h)
        # Add a small offset to x_center for annotation clarity
        x_center = x_center + 0.12+ base_width/2
        # Annotate min
        ax.text(x_center, row["ymin"], f"{row['ymin']:.2f}", va='bottom', ha='center', fontsize=8, color=inner_palette[h])
        # Annotate max
        ax.text(x_center, row["ymax"], f"{row['ymax']:.2f}", va='top', ha='center', fontsize=8, color=inner_palette[h])
        # Annotate p15
        ax.text(x_center, row["p15"], f"{row['p15']:.2f}", va='bottom', ha='center', fontsize=8, color=palette[h])
        # Annotate p85
        ax.text(x_center, row["p85"], f"{row['p85']:.2f}", va='top', ha='center', fontsize=8, color=palette[h])
        # Annotate median
        ax.text(x_center, row["median"], f"{row['median']:.2f}", va='center', ha='center', fontsize=8, color='black')
    plt.tight_layout()

    # Save
    country = country.replace(' ', '_')
    outfile = os.path.join(outputpath, var + '_' + country + '_box_minmax_p15p85.png')
    plt.savefig(outfile, dpi=300)
    plt.show()

def lineplot_and_boxplot(df, df_era5, src,country, var, longname, outputpath):
    '''Create a combined figure with a line plot of anomalies and a box plot of statistics.'''

    # Use scenario-based colors
    palette = {"rcp26": "lightblue", "rcp85": "lightcoral"}
    inner_palette= {"rcp26": "darkblue", "rcp85": "darkred"}

    # Ensure consistent hue order from data to match the palette keys
    hue_order = [k for k in palette.keys() if k in src["scenario"].unique().tolist()]
    # Consistent order for slices on the x-axis
    slice_order = sorted(src["slice"].unique().tolist())

    # Summary stats per slice/scenario
    stats = (
        src.groupby(["slice", "scenario"])["anomaly_mean"]
        .agg(
            ymin="min",
            ymax="max",
            p15=lambda s: s.quantile(0.15),
            p85=lambda s: s.quantile(0.85),
            median="median",
            n="size",
        )
        .reset_index()
    )
    # Ensure ERA5 years are int for plotting
    df_era5_plot = df_era5.copy()
    if pd.api.types.is_datetime64_any_dtype(df_era5_plot['year']):
        df_era5_plot['year'] = df_era5_plot['year'].dt.year

    # Drop NaN anomalies for plotting
    df_era5_plot = df_era5_plot.dropna(subset=['anomaly'])

    # Create a figure with two subplots (side by side)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [3, 1]})
    # --- Left: line_plot_anomaly (manual version) ---
    for scenario in hue_order:
        for _, group in df[df['scenario'] == scenario].groupby('realization'):
            axes[0].plot(group['year'], group['anomaly'], color=palette[scenario], alpha=0.3, linewidth=1)
        median = df[df['scenario'] == scenario].groupby('year')['anomaly'].median()
        # Plot median line
        axes[0].plot(median.index, median.values, color=inner_palette[scenario], label=f"{scenario} median", linewidth=2)
        # Fill between min and max for each year
        grouped = df[df['scenario'] == scenario].groupby('year')['anomaly']
        min_vals = grouped.min()
        max_vals = grouped.max()
        axes[0].fill_between(min_vals.index, min_vals.values, max_vals.values, color=palette[scenario], alpha=0.15, label=f"{scenario} min-max")

    # Add ERA5 anomaly as black line if available
    if 'anomaly' in df_era5_plot.columns and not df_era5_plot.empty:
        axes[0].plot(df_era5_plot['year'], df_era5_plot['anomaly'], color='black', label='ERA5', linewidth=2)

    # Robust y-limits ignoring NaN
    ymin = np.nanmin(df['anomaly'].values) - 0.5
    ymax = np.nanmax(df['anomaly'].values) + 0.5
    ytext = ymin+0.1
    axes[0].set_xlim(1969, 2100)
    axes[0].axhline(0, color=DARKGREY, linestyle='-', linewidth=1)
    axes[0].axvline(1991, color='grey', linestyle='-', linewidth=1)
    axes[0].axvline(2020, color='grey', linestyle='-', linewidth=1)
    # Fill between the vertical lines for the reference period
    axes[0].fill_betweenx(
        y=axes[0].get_ylim(), 
        x1=1991, 
        x2=2020, 
        color='lightgrey', 
        alpha=0.1
    )
    # Add a legend for the shaded area
    axes[0].text(1992, ytext, 'Reference (1991-2020)', color='grey', fontsize=12)

    axes[0].set_title(f"{longname} anomaly time series\n{country}")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel(f"{longname} anomaly to 1991-2020")
    axes[0].set_ylim(ymin, ymax)
    axes[0].legend()
    #axes[0].grid(True)
    #
    # --- Right: boxplot (manual version) ---
    #
    base_width = 0.4
    inner_width = base_width
    # Calculate spacing so columns are evenly distributed
    n_slices = len(slice_order)
    n_hues = len(hue_order)
    total_columns = n_slices * n_hues
    x_positions = []
    for i, s in enumerate(slice_order):
        for j, h in enumerate(hue_order):
            x_positions.append(i * n_hues + j)
    #slice_pos = {s: i * n_hues for i, s in enumerate(slice_order)}

    for idx, row in stats.iterrows():
        s = row["slice"]
        h = row["scenario"]
        if h not in hue_order:
            continue
        x_center = slice_order.index(s) * n_hues + hue_order.index(h)
        axes[1].add_patch(Rectangle(
            (x_center - base_width / 2, row["ymin"]),
            base_width,
            row["ymax"] - row["ymin"],
            facecolor=palette[h],
            edgecolor=inner_palette[h],
            alpha=0.35
        ))
        axes[1].add_patch(Rectangle(
            (x_center - inner_width / 2, row["p15"]),
            inner_width,
            row["p85"] - row["p15"],
            facecolor=inner_palette[h],
            edgecolor=inner_palette[h],
            alpha=0.7
        ))
        axes[1].hlines(row["median"], x_center - inner_width / 2, x_center + inner_width / 2, colors="lightgray", linewidth=2)
        x_anno = x_center + 0.12 + base_width/2
        axes[1].text(x_anno, row["ymin"]-0.2, f"{row['ymin']:.2f}", va='bottom', ha='center', fontsize=8, color=inner_palette[h])
        axes[1].text(x_anno, row["ymax"]+0.2, f"{row['ymax']:.2f}", va='top', ha='center', fontsize=8, color=inner_palette[h])
        axes[1].text(x_anno, row["p15"], f"{row['p15']:.2f}", va='bottom', ha='center', fontsize=8, color=palette[h])
        axes[1].text(x_anno, row["p85"], f"{row['p85']:.2f}", va='top', ha='center', fontsize=8, color=palette[h])
        axes[1].text(x_anno, row["median"], f"{row['median']:.2f}", va='center', ha='center', fontsize=8, color='black')

        axes[1].set_xlim(-base_width, total_columns - base_width)
    xticks = [slice_order.index(s) * n_hues + j for s in slice_order for j in range(n_hues)]
    xticklabels = [f"{s}\n{h}" for s in slice_order for h in hue_order]

    axes[1].set_xticks(xticks)
    axes[1].set_xticklabels(xticklabels)
    axes[1].set_ylim(ymin, ymax)
    axes[1].set_ylabel(f"{longname} anomaly to 1991-2020")
    axes[1].set_title(f"Projected {longname} anomaly\n(30-year means)")
    axes[1].grid(True, axis='y')
    legend_handles = []
    for h in hue_order:
        legend_handles.append(Patch(facecolor=palette[h], edgecolor=inner_palette[h], alpha=0.35, label=f"Min-Max ({h})"))
        legend_handles.append(Patch(facecolor=inner_palette[h], edgecolor=inner_palette[h], alpha=0.7, label=f"P15–P85 ({h})"))
    legend_handles.append(plt.Line2D([0], [0], color="lightgray", lw=2, label="Median"))
    axes[1].legend(handles=legend_handles, loc='upper left')

    plt.tight_layout()
    # Save
    country = country.replace(' ', '_')
    outfile = os.path.join(outputpath, var + '_' + country + '_timeseries_box_minmax_p15p85.png')
    print(f"Saving figure to {outfile}")
    plt.savefig(outfile, dpi=300)
    plt.show()
    return    