#!/usr/bin/env python3
# plotting tool for time series

from operator import index
import pandas as pd
import matplotlib.pyplot as plt
import os  
import sys
import numpy as np  

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
    plt.savefig(outfile, dpi=300)
    
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    
    return plt.show()


def line_plot_min_max(df, x, y, index,outputpath, region, ylim=None):
    """Plot median time series with min-max shading per scenario.

    Parameters
    ----------
    df : DataFrame with columns ['year','scenario', y]
    x : str, name of x column (typically 'year')
    y : str, name of value column
    outputpath : str, directory to save plot
    region : str, region name for title
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

    plt.title(f"{region}: Area Mean of {y}", fontsize=16)
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
    plt.text(1991 + 1, plt.ylim()[0] + 0.02 * (plt.ylim()[1]-plt.ylim()[0]), 'Reference (1991-2020)', color='grey', fontsize=10)
     #
    # Save
    safe_x = x.replace(' ', '_')
    #
    safe_region = region.replace(' ', '_')
    outfile = os.path.join(outputpath, f'line_plot_min_max_{index}_{safe_x}_{safe_region}.png')
    plt.savefig(outfile, dpi=300)
    print('Saved plot to: ', outfile)
    return plt.show()


def line_plot_anomaly(data,x,y,outputpath, group, country, index,longname,ylim=None):
    """make line plot of anomaly

    you can either have each realisation in it own color 
    or 
    if group equals scenario, each scenario has its own color 
    ylim : tuple(float,float) or None, optional y-limits; if None auto-scale
    """
    plt.figure(figsize=(12, 8))
    
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

    print(data[:3])
    print(x,y,group,country, longname)

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

    # title, labels
    plt.title(country+' '+y+ ' of area mean '+longname, fontsize=20)
    plt.legend(title='CORDEX AFR22 Realization', loc='upper left', ncol=1, fontsize=8)
    plt.tight_layout()
    plt.xticks(rotation=0)
    plt.xlabel(x, fontsize=16)
    plt.ylabel(y+' of '+longname, fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
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
    plt.xlim(1971, 2100)
    plt.axhline(0, color='grey', linestyle='-', linewidth=1)
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
    # save plot
    outfile = os.path.join(outputpath,'line_plot_'+group+'_'+x+'_'+index+'_'+y+'.png')
    plt.savefig(outfile, dpi=300)
    print('file liegt: ', outfile)
    
    return plt.show()