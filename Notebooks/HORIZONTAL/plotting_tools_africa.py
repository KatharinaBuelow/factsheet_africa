#!/usr/bin/env python3

from fileinput import filename
from fileinput import filename
import os
import numpy as np
import glob
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr
from typing import Optional

from plotting_shape_file import add_scalebar


def savefig(plot, name, dpi):
    plot.savefig(name, dpi=dpi, bbox_inches='tight')
    print('plot ist saved in : ', name)

def directory_available(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def add_unit(data,var):
     
    '''Some indices do not have a unit,
    for example number of Heatwave, Hotspell'''

    if var in ['HSf','HWf']:
        data[var].attrs['units'] = 'Number'
    else:
        print('nothing to do, unit exists')
    return

def get_variable(data,var):
    '''Change the variable of absolute Temperature and unit for plotting'''

    if var in ['TN','TX','TG']:
        data_variable = data[var]-273.15

        data[var].attrs['units']='degree Celsius'
        data[var].attrs['long_name']='Temperature'
    elif var in ['ev_coin_sdu']:
        data_variable = data[var]/30    
    else:
        data_variable = data[var]

    return data_variable


def only_land_points(data):
    '''Mask out ocean data using land-sea mask if available'''

    # Land sea mask
    lsm=xr.open_dataset('/work/ch0636/g300047/cicles/lsm_afr22_common_ohne_pur_wasser.nc')

    land_mask = lsm['sftlf'].where(lsm['sftlf'] == 1)
    data_variable= data.where(land_mask.values == 1)

    return data_variable


def plot_2diff(
        sims_rcp26,
        sims_rcp85,
        robust_rcp26,
        robust_rcp85,
        level_steps_diff, 
        color_steps_diff,
        what,
        robust,
        plotdir,
        title="",
        var="",
        robustness=False,
        westafrica=None,
        user_dpi=300,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:  
    levels=level_steps_diff
    colors=color_steps_diff
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})
   
    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
        }

    if westafrica is True:
        height=3
    else:
        height=4.5

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(6,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
      
    for ax in [ax1, ax2]:
        ax.gridlines(
            draw_labels={"bottom": "x", "left": "y"},
            dms=True,
            x_inline=False,
            y_inline=False,
            linewidth=0.5,
            )
        ax.coastlines(resolution="50m", color="black", linewidth=1)
        ax.add_feature(cf.BORDERS)
        ax.add_feature(cf.OCEAN, facecolor='#f0f0f0')
                            
        if westafrica is True:
            region='West_Africa'
            ax.set_extent([-25, 20, -0.75, 27.3])
            # Space between rows:
            fig.subplots_adjust(hspace=0.03)
            fig.subplots_adjust(wspace=0.25)
        else:
            region='Africa'
            ax.set_extent([-20, 60, -35, 35])

    # Plot data for rcp26
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
        # If variable is timedelta, convert to numeric days for plotting
        try:
            if np.issubdtype(data_variable.dtype, np.timedelta64):
                data_variable = data_variable.dt.days
        except Exception:
            pass
        # Mask out ocean data using land-sea mask
        data_variable = only_land_points(data_variable)

        if var !='number_of_people':
        # Select labels // Units frome metadata
        # Set title of plot
            varname=data[var].long_name
            add_unit(data,var)
            unit=data[var].units
        else:
            varname='Number of people'
            unit='Number'
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 #fontweight='bold', 
                 x=0.5,
                 fontsize=14,
                 position=(0.5, 0.99),
                 )  
                
        im = data_variable.plot(ax=ax1,
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        if robustness is True:
            robust_rcp26=file.replace(what,robust) #'_time-mean_ensemble-diff-median.nc','_ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp26)
            datar_variable = datar[var]

            # Mask out ocean data using land-sea mask
            datar_variable = only_land_points(datar_variable)
            # Significant only when robustness equals ±2
            significant = xr.where(np.abs(datar_variable) == 2, 1, 0).squeeze()
            significant = only_land_points(significant)
            significant.plot.contourf(
                        ax=ax1,
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        
        ax1.set_title(f'RCP26: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)
    
    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        print('rcp85')
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
        # If variable is timedelta, convert to numeric days for plotting
        try:
            if np.issubdtype(data_variable.dtype, np.timedelta64):
                data_variable = data_variable.dt.days
        except Exception:
            pass
        data_variable = only_land_points(data_variable)
        im = data_variable.plot(ax=ax2,
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        
        if robustness is True:
            robust_rcp85=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(robust_rcp85)
            datar_variable = datar[var]
            # Significant only when robustness equals ±2
            significant = xr.where(np.abs(datar_variable) == 2, 1, 0).squeeze()
            significant = only_land_points(significant)
            significant.plot.contourf(
                    ax=ax2,
                    levels=[-.5, .5],
                    colors='none',
                    hatches=[ None,None,"//", ],
                    add_colorbar=False,
                    extend='both',
                    transform=ccrs.PlateCarree()
            )
        ax2.set_title(f'RCP85: {file.split("_")[5]}-{file.split("_")[6]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.05])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label('[ '+unit+' ]', fontsize=10)

    # Improve layout before saving (leave space for bottom colorbar & suptitle)
    fig.tight_layout(rect=[0.03, 0.18, 0.97, 0.93])
    name="{}/{}_diff-robust_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(fig, "{}".format(name), user_dpi) 
    return


def plot_diff(
        sims_rcp26,
        sims_rcp85,
        level_steps_diff, 
        color_steps_diff,
        what,
        robust,
        plotdir,
        title="",
        var="",
        robustness=None,
        westafrica=None,
        user_dpi=300,
        rows=2,
        columns=2,
        row_gap: float = 0.35,
        wspace: Optional[float] = None,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    
    levels=level_steps_diff
    colors=color_steps_diff
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})
        
    if westafrica is True:
        height=5.8
    else:
        height=7.5
    if columns == 2:
        width=7
    elif columns == 3:
        width=10   

    # Create subplots (use constrained_layout to better respect spacing, then fine-tune)
    fig, axes = plt.subplots(
        ncols=columns,
        nrows=rows,
        figsize=(width, height),
        subplot_kw={'projection': ccrs.PlateCarree()},
        constrained_layout=False,  # we'll control manually
        squeeze=False,
    )
    # Initial spacing (will be re-applied after plotting & colorbar addition)
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace, top=0.92, bottom=0.08)
    else:
        fig.subplots_adjust(hspace=row_gap, top=0.92, bottom=0.08)

    for row in axes:
        for ax in row:
            ax.gridlines(
                draw_labels={"bottom": "x", "left": "y"},
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            ax.coastlines(resolution="50m", color="black", linewidth=1)
            ax.add_feature(cf.BORDERS)

            #west Afrika
            #lon : -25.87 to 20 by 0.11 degrees
            #lat : -0.75 to 27.3 by 0.11 degrees
            if westafrica is True:
                region = 'West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region = 'Africa'
                ax.set_extent([-20, 60, -35, 35])

    # Plot data for rcp26
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
    
        # Select labels // Units frome metadata
        # Set title of plot
        varname=data[var].long_name
        add_unit(data,var)
        unit=data[var].units
        
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.97),
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        if robustness is True:
            r_rcp26=file.replace(what,robust) #'time-mean_ensemble-diff-median.nc','ensemble-robustness.nc')
            datar = xr.open_dataset(r_rcp26,decode_timedelta=False)
            
            datar_variable = datar[var]  
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze().astype(int)
            #significant = xr.where(xr.ufuncs.absolute(datar_variable) == 2, 1, 0).squeeze()
            significant.plot.contourf(
                        ax=axes[0,i],
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )

        axes[0, i].set_title(f'RCP26: {file.split("_")[6]}-{file.split("_")[7]}',fontsize=12)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        
        if robustness is True:
            r_rcp85=file.replace(what,robust) #'_time-mean_ensemble-diff-median.nc','_ensemble-robustness.nc')
            datar = xr.open_dataset(r_rcp85,decode_timedelta=False)
            
            datar_variable = datar[var]  
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze().astype(int)
            #significant = xr.where(xr.ufuncs.absolute(datar_variable) == 2, 1, 0).squeeze()
            significant.plot.contourf(
                        ax=axes[1,i],
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        axes[1, i].set_title(f'RCP85: {file.split("_")[6]}-{file.split("_")[7]}',fontsize=12)

    # Add colorbar axis; position may need tuning depending on row_gap
    cbar_ax = fig.add_axes([0.15, 0.04, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ ' + unit + ' ]')

    # Re-apply spacing AFTER colorbar & titles so row_gap takes effect
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace, top=0.90, bottom=0.10)
    else:
        fig.subplots_adjust(hspace=row_gap, top=0.90, bottom=0.10)
    name="{}/{}_diff-robust_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(fig, "{}".format(name), user_dpi) 
    return


def plot_absolut(
        sims_rcp26,
        sims_rcp85,
        level_steps,
        color_steps,
        plotdir,
        title="",
        var="",
        var_pattern="",
        westafrica=None,
        shapefile=None,
        country=None,
        user_dpi=300,
        rows=2,
        columns=2,
        fancy=None,
        row_gap: float = 0.35,
        wspace: Optional[float] = None,
        ):
    
    """Plot absolute values for RCP26/RCP85 in a grid.

    Parameters
    ----------
    row_gap : float
        Vertical space between subplot rows (matplotlib hspace). Default 0.35.
    wspace : float | None
        Optional horizontal space between columns (matplotlib wspace). If None keep default.
    """

    print(sims_rcp26)
    print(sims_rcp85)
    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels=level_steps
    colors=color_steps

    if shapefile is not None:
        print('shapefile provided:')
        try:
            shapefile = shapefile.to_crs(epsg=4326)
        except Exception:
            pass

    if rows == 2:
        height=6.1

    if westafrica is True:
        height=6.1
    else:
        height=7

    if columns == 2:
        width=7
    elif columns == 3:
        width=10
    
    # Create subplots
    fig, axes = plt.subplots(
        ncols=columns,
        nrows=rows,
        figsize=(width, height),
        subplot_kw={'projection': ccrs.PlateCarree()},
        squeeze=False,
    )
    # Apply user-defined spacing between rows (and optionally columns)
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace)
    else:
         fig.subplots_adjust(hspace=row_gap)
    
    for row_index, row in enumerate(axes):
        for col_index, ax in enumerate(row):
            gl = ax.gridlines(
                draw_labels=True,
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.bottom_labels = (row_index == rows - 1)
            gl.left_labels = (col_index == 0)

            ax.tick_params(axis="x", bottom=(row_index == rows - 1), labelbottom=(row_index == rows - 1))
            ax.tick_params(axis="y", left=(col_index == 0), labelleft=(col_index == 0))
            #ax.coastlines(resolution="50m", color="lightgrey", linewidth=1)
            ax.coastlines(resolution="10m", color="black", linewidth=1)

            if shapefile is not None:
                print('adding borders from shapefile')  
            else:
                print('adding default borders')
                ax.add_feature(cf.BORDERS)
                #ax.add_feature(cf.OCEAN, facecolor='#f0f0f0')

            if shapefile is not None and country is not None:
                ax.set_extent([shapefile.total_bounds[0]-0.25, 
                               shapefile.total_bounds[2]+0.25, 
                               shapefile.total_bounds[1]-0.25, 
                               shapefile.total_bounds[3]+0.25])
                

            elif westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data for rcp26
    print('sims_rcp26',sims_rcp26)
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
    
        # Select labels // Units frome metadata
        # Set title of plot
        if var not in ['number_of_people','ev_coin_sdu_median', 'ev_coin_du_days']:
            varname=data[var].long_name
            add_unit(data,var)
            unit=data[var].units
        elif var == 'number_of_people':
            varname='Number of people'
            unit='Number'
        elif var == 'ev_coin_du_days':
            varname=''
            unit='days / year'
        else:
            print('var-long_name not found')
               
        s = "{} {}".format(title,varname)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.95)
                 )  
        
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )
        # Plot shapefile on current axis only if provided
        if shapefile is not None:
            shapefile.plot(ax=axes[0, i], edgecolor='black', linewidth=0.5, facecolor='none')
        # This is not very clever, need to be adjusted according to file_name :-(
        if var =='ev_coin_du_days':
            axes[0, i].set_title(f'RCP26: {file.split("_")[9].split(".")[0]}', fontsize=12)
        else:
            axes[0, i].set_title(f'RCP26: {file.split("_")[6]}-{file.split("_")[7]}',fontsize=12)
    
        if fancy:
            # Add north arrow and scalebar to all subplots
            arrowprops = dict(facecolor='black', edgecolor='black', width=1, headwidth=8, headlength=10)
            # If a shapefile is provided, build union geometry for accurate scalebar
            union_geom = shapefile.unary_union if shapefile is not None else None
            for ax in axes.flat:
                # Arrow pointing up in axes coordinates
                ax.annotate('', xy=(0.08, 0.85), xytext=(0.08, 0.65), xycoords='axes fraction', arrowprops=arrowprops)
                # Label "N" above the arrow
                ax.text(0.08, 0.86, 'N', transform=ax.transAxes, ha='center', va='bottom', fontsize=12)#, fontweight='bold')
                if union_geom is not None:
                    add_scalebar(ax, geom=union_geom, location='lower right', segments=4)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
        
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
         
        if shapefile is not None:
            shapefile.plot(ax=axes[1, i], edgecolor='black', linewidth=0.5, facecolor='none')
        if var =='ev_coin_du_days':
            axes[1, i].set_title(f'RCP85: {file.split("_")[9].split(".")[0]}',fontsize=12)
        else:
            axes[1, i].set_title(f'RCP85: {file.split("_")[6]}-{file.split("_")[7]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label=f'[ {str(unit)} ]')
   
    # Layout (space for colorbar at bottom)(left,bottom,right, top)
    fig.tight_layout(rect=[0.03, 0.01, 0.97, 0.99])

    # just het median/mean from the input file for the outputfilename
    filename = os.path.basename(sims_rcp26[0]) if len(sims_rcp26) > 0 else None
    what = filename.split('_')[1] if filename and len(filename.split('_')) > 1 else None
   
    if country is not None:
        name="{}/{}_{}_absolute_{}_{}.png".format(plotdir, var_pattern, what, country, user_dpi)
    else:
        name="{}/{}_{}_absolute_{}.png".format(plotdir, var_pattern, what, user_dpi)

    print('file is here:', name)
    fig.savefig("{}".format(name), dpi=user_dpi, bbox_inches="tight")# pad_inches=0.02)
    return


def plot_era(
        sim,
        level_steps,
        color_steps,
        plotdir,
        title="",
        var="",
        westafrica=None,
        shapefile=None,
        country=None,
        user_dpi=300,
        rows=2,
        columns=2,
        fancy=None,
        row_gap: float = 0.35,
        wspace: Optional[float] = None,
        ):
    
    """Plot absolute values for ERA5 in a grid.

    Parameters
    ----------
    row_gap : float
        Vertical space between subplot rows (matplotlib hspace). Default 0.35.
    wspace : float | None
        Optional horizontal space between columns (matplotlib wspace). If None keep default.
    """

    print('plotting data from:', sim)
    
    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels=level_steps
    colors=color_steps

    if shapefile is not None:
        print('shapefile provided:')
        try:
            shapefile = shapefile.to_crs(epsg=4326)
        except Exception:
            pass

    

    if westafrica is True:
        height=4
    else:
        height=3.5

    if columns == 1:
        width=5
    elif columns == 3:
        width=10
    
    # Create subplots
    fig, axes = plt.subplots(
        ncols=columns,
        nrows=rows,
        figsize=(width, height),
        subplot_kw={'projection': ccrs.PlateCarree()},
        squeeze=False,
    )
    # Apply user-defined spacing between rows (and optionally columns)
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace)
    else:
         fig.subplots_adjust(hspace=row_gap)

    title_drawn = False
    
    for row in axes:
        for ax in row:
            ax.gridlines(
                draw_labels={"bottom": "x", "left": "y"},
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            #ax.coastlines(resolution="50m", color="lightgrey", linewidth=1)
            ax.coastlines(resolution="10m", color="black", linewidth=1)

            if shapefile is not None:
                print('adding borders from shapefile')  
            else:
                print('adding default borders')
                ax.add_feature(cf.BORDERS)
                #ax.add_feature(cf.OCEAN, facecolor='#f0f0f0')

            if shapefile is not None and country is not None:
                ax.set_extent([shapefile.total_bounds[0]-0.25, 
                               shapefile.total_bounds[2]+0.25, 
                               shapefile.total_bounds[1]-0.25, 
                               shapefile.total_bounds[3]+0.25])
                

            elif westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data 
    
    for i, file in enumerate(sim):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
        # convert to annual values
        data_variable = data_variable
    
        # Select labels // Units frome metadata
        # Set title of plot
        if var not in ['number_of_people','ev_coin_sdu_median', 'ev_coin_sdu']:
            varname=data[var].long_name
            add_unit(data,var)
            unit=data[var].units
        elif var == 'number_of_people':
            varname='Number of people'
            unit='Number'
        elif var == 'ev_coin_sdu_median':
            varname=''
            unit='events per year'
        elif var == 'ev_coin_sdu':
            varname=''
            unit='days/year'
        else:
            print('var-long_name not found')
               
        s = "{} {}".format(title, varname).strip()

        if not title_drawn:
            fig.suptitle(
                f"{s}: ",
                fontsize=14,
                x=0.5,
                y=0.98,
            )
            title_drawn = True

        
        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )
        # Plot shapefile on current axis only if provided
        if shapefile is not None:
            shapefile.plot(ax=axes[0, i], edgecolor='black', linewidth=0.5, facecolor='none')
        # This is not very clever, need to be adjusted according to file_name :-(
        if var =='ev_coin_sdu':
            axes[0, i].set_title(f'ERA5: {file.split("_")[5]}',fontsize=12)
    
        if fancy:
            # Add north arrow and scalebar to all subplots
            arrowprops = dict(facecolor='black', edgecolor='black', width=1, headwidth=8, headlength=10)
            # If a shapefile is provided, build union geometry for accurate scalebar
            union_geom = shapefile.unary_union if shapefile is not None else None
            for ax in axes.flat:
                # Arrow pointing up in axes coordinates
                ax.annotate('', xy=(0.08, 0.85), xytext=(0.08, 0.65), xycoords='axes fraction', arrowprops=arrowprops)
                # Label "N" above the arrow
                ax.text(0.08, 0.86, 'N', transform=ax.transAxes, ha='center', va='bottom', fontsize=12)#, fontweight='bold')
                if union_geom is not None:
                    add_scalebar(ax, geom=union_geom, location='lower right', segments=4)

    
    cbar_ax = fig.add_axes([0.15, 0.055, 0.7, 0.028])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label=f'[ {str(unit)} ]')
   
    # Layout: reserve space for the title at the top and the colorbar at the bottom
    fig.tight_layout(rect=[0.03, 0.09, 0.97, 0.92])

    if country is not None:
        name="{}/{}_absolut_{}_{}.png".format(plotdir, var, country, user_dpi)
    else:
        name="{}/{}_absolut_{}.png".format(plotdir, var , user_dpi)

    print('file is here:', name)
    fig.savefig("{}".format(name), dpi=user_dpi, bbox_inches="tight")# pad_inches=0.02)
    return

def plot_diff_compev(
        sims_rcp26,
        sims_rcp85,
        level_steps,
        color_steps,
        plotdir,
        title="",
        var="",
        var_pattern=None,
        robustness=False,
        westafrica=None,
        shapefile=None,
        country=None,
        user_dpi=300,
        rows=2,
        columns=2,
        fancy=None,
        row_gap: float = 0.35,
        wspace: Optional[float] = None,
        ):
    
    """Plot absolute values for RCP26/RCP85 in a grid.

    Parameters
    ----------
    row_gap : float
        Vertical space between subplot rows (matplotlib hspace). Default 0.35.
    wspace : float | None
        Optional horizontal space between columns (matplotlib wspace). If None keep default.
    """

    print(sims_rcp26)
    print(sims_rcp85)
    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels=level_steps
    colors=color_steps
    unit='days/year'
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})

    if shapefile is not None:
        print('shapefile provided:')
        try:
            shapefile = shapefile.to_crs(epsg=4326)
        except Exception:
            pass

    if rows == 2:
        height=6

    if westafrica is True:
        height=6
        if title=='':
            height=5
    else:
        height=7

    if columns == 2:
        width=7
    elif columns == 3:
        width=10
    
    # Create subplots
    fig, axes = plt.subplots(
        ncols=columns,
        nrows=rows,
        figsize=(width, height),
        subplot_kw={'projection': ccrs.PlateCarree()},
        squeeze=False,
    )
    # Apply user-defined spacing between rows (and optionally columns)
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace)
    else:
         fig.subplots_adjust(hspace=row_gap)
    
    for row_axes in axes:
        for ax in row_axes:
            subplot_row = ax.get_subplotspec().rowspan.start
            subplot_col = ax.get_subplotspec().colspan.start

            gl = ax.gridlines(
                draw_labels=True,
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.bottom_labels = (subplot_row == rows - 1)
            gl.left_labels = (subplot_col == 0)

            ax.tick_params(axis="x", bottom=(subplot_row == rows - 1), labelbottom=(subplot_row == rows - 1))
            ax.tick_params(axis="y", left=(subplot_col == 0), labelleft=(subplot_col == 0))
            #ax.coastlines(resolution="50m", color="lightgrey", linewidth=1)
            ax.coastlines(resolution="10m", color="black", linewidth=1)

            if shapefile is not None:
                print('adding borders from shapefile')  
            else:
                print('adding default borders')
                ax.add_feature(cf.BORDERS)
                #ax.add_feature(cf.OCEAN, facecolor='#f0f0f0')

            if shapefile is not None and country is not None:
                ax.set_extent([shapefile.total_bounds[0]-0.25, 
                               shapefile.total_bounds[2]+0.25, 
                               shapefile.total_bounds[1]-0.25, 
                               shapefile.total_bounds[3]+0.25])
                

            elif westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data for rcp26
    print('sims_rcp26',sims_rcp26)
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
    
        # Select labels // Units frome metadata
        # Set title of plot
            
        s = "{}".format(title)
    
        fig.suptitle(s, 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.95)
                 )  

        im = data_variable.plot(ax=axes[0, i],
                            levels=levels,
                            colors=colors,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )
        if robustness is True:
            datar_variable = data['robustness']

            # Significant only when robustness equals ±1
            significant = xr.where(np.abs(datar_variable) == 1, 1, 0).squeeze()
            # do not plot NaN cells
            significant = significant.where(datar_variable.notnull())
            significant.plot.contourf(
                        ax=axes[0, i],
                        levels=[-.5, .5],
                        colors='none',
                        # now hatches are applied to the not significant areas, with a grey color for the hatches
                        hatches=['', '//', ''],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        # Plot shapefile on current axis only if provided
        if shapefile is not None:
            shapefile.plot(ax=axes[0, i], edgecolor='black', linewidth=0.5, facecolor='none')
        # This is not very clever, need to be adjusted according to file_name :-(
        axes[0, i].set_title(f'RCP26: {file.split("_")[7]}',fontsize=12)
    
        if fancy:
            # Add north arrow and scalebar to all subplots
            arrowprops = dict(facecolor='black', edgecolor='black', width=1, headwidth=8, headlength=10)
            # If a shapefile is provided, build union geometry for accurate scalebar
            union_geom = shapefile.unary_union if shapefile is not None else None
            for ax in axes.flat:
                # Arrow pointing up in axes coordinates
                ax.annotate('', xy=(0.08, 0.85), xytext=(0.08, 0.65), xycoords='axes fraction', arrowprops=arrowprops)
                # Label "N" above the arrow
                ax.text(0.08, 0.86, 'N', transform=ax.transAxes, ha='center', va='bottom', fontsize=12)#, fontweight='bold')
                if union_geom is not None:
                    add_scalebar(ax, geom=union_geom, location='lower right', segments=4)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
        
        im = data_variable.plot(ax=axes[1, i],
                           levels=levels,
                           colors=colors,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
        if robustness is True:
            datar_variable = data['robustness']

            # Significant only when robustness equals ±1
            significant = xr.where(np.abs(datar_variable) == 1, 1, 0).squeeze()

            # do not plot NaN cells
            significant = significant.where(datar_variable.notnull())

            significant.plot.contourf(
                        ax=axes[1, i],
                        levels=[-.5, .5],
                        colors='none',
                        #hattches for1: significant values
                        #hatches=[None, None, "//", ],
                        # now hatches are applied to the not significant areas, with a grey color for the hatches
                        hatches=["", "//", ""],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        if shapefile is not None:
            shapefile.plot(ax=axes[1, i], edgecolor='black', linewidth=0.5, facecolor='none')
        
        axes[1, i].set_title(f'RCP85: {file.split("_")[7]}',fontsize=12)

    axes = np.atleast_2d(axes)

    for r in range(rows):
        for c in range(columns):
            ax = axes[r, c]

            gl = ax.gridlines(
                draw_labels=True,
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.bottom_labels = (r == rows - 1)  # only bottom row
            gl.left_labels = (c == 0)           # only left column

            ax.coastlines(resolution="10m", color="black", linewidth=1)

            # optional: also hide matplotlib ticks on inner panels
            ax.tick_params(axis="x", labelbottom=(r == rows - 1), bottom=(r == rows - 1))
            ax.tick_params(axis="y", labelleft=(c == 0), left=(c == 0))

    cbar_ax = fig.add_axes([0.17, 0.002, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label=f'[ {str(unit)} ]')
   
    # Layout (space for colorbar at bottom)(left,bottom,right, top)
    fig.tight_layout(rect=[0.03, 0.01, 0.97, 0.99])
    # incase the mean is chosen instead of the median, the file name will be adjusted accordingly
    what = str.split(var, '_')[5]

    if title != "":
        name="{}/Compev_{}_{}_diff_{}.png".format(plotdir, var_pattern, what, user_dpi)
        if country is not None:
            name="{}/Compev_{}_{}_diff_{}_{}.png".format(plotdir, var_pattern, what, country, user_dpi)
    else:
        name="{}/Compev_{}_{}_diff_{}_{}_oT.png".format(plotdir, var_pattern , what, country, user_dpi)
    print('file is here:', name)
    fig.savefig("{}".format(name), dpi=user_dpi, bbox_inches="tight")

    return

def plot_diff_compev_era5(
        sims_rcp26,
        sims_rcp85,
        sims_era5,
        level_steps,
        color_steps,
        levelsteps_era5,
        colorsteps_era5,
        plotdir,
        title="",
        var="",
        varera5="",
        var_pattern=None,
        robustness=False,
        westafrica=None,
        shapefile=None,
        country=None,
        user_dpi=300,
        rows=2,
        columns=3,
        fancy=None,
        row_gap: float = 0.35,
        wspace: Optional[float] = None,
        ):
    
    """

    Parameters
    ----------
    row_gap : float
        Vertical space between subplot rows (matplotlib hspace). Default 0.35.
    wspace : float | None
        Optional horizontal space between columns (matplotlib wspace). If None keep default.
    """

    print(sims_rcp26)
    print(sims_rcp85)
    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    # set the colors:
    levels_diff = level_steps
    colors_diff = color_steps
    levels_era5 = levelsteps_era5
    colors_era5 = colorsteps_era5
    unit='days/year'
    hatchcolor='grey'
    plt.rcParams.update({'hatch.color': hatchcolor})

    if shapefile is not None:
        print('shapefile provided:')
        try:
            shapefile = shapefile.to_crs(epsg=4326)
        except Exception:
            pass

    if rows == 2:
        height=6

    if westafrica is True:
        height=6.2
        if title=='':
            height=5.5
    else:
        height=7

    if columns == 2:
        width=7
    elif columns == 3:
        width=10
    
    # Create subplots
    fig, axes = plt.subplots(
        ncols=columns,
        nrows=rows,
        figsize=(width, height),
        subplot_kw={'projection': ccrs.PlateCarree()},
        squeeze=False,
    )
    # Apply user-defined spacing between rows (and optionally columns)
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace)
    else:
         fig.subplots_adjust(hspace=row_gap)
    
    for row_axes in axes:
        for ax in row_axes:
            subplot_row = ax.get_subplotspec().rowspan.start
            subplot_col = ax.get_subplotspec().colspan.start

            if subplot_row == 1 and subplot_col == 0:
                ax.set_visible(False)
                continue

            gl = ax.gridlines(
                draw_labels=True,
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.bottom_labels = (subplot_row == rows - 1)
            gl.left_labels = (subplot_col == 0)

            ax.tick_params(axis="x", bottom=(subplot_row == rows - 1), labelbottom=(subplot_row == rows - 1))
            ax.tick_params(axis="y", left=(subplot_col == 0), labelleft=(subplot_col == 0))
            #ax.coastlines(resolution="50m", color="lightgrey", linewidth=1)
            ax.coastlines(resolution="10m", color="black", linewidth=1)

            if shapefile is not None:
                print('adding borders from shapefile')  
            else:
                print('adding default borders')
                ax.add_feature(cf.BORDERS)
                #ax.add_feature(cf.OCEAN, facecolor='#f0f0f0')

            if shapefile is not None and country is not None:
                ax.set_extent([shapefile.total_bounds[0]-0.25, 
                               shapefile.total_bounds[2]+0.25, 
                               shapefile.total_bounds[1]-0.25, 
                               shapefile.total_bounds[3]+0.25])
                
    
    im_era5 = None
    im_diff = None

    # Plot data for ERA5
    for i, file in enumerate(sims_era5):
        data = xr.open_dataset(file, decode_timedelta=False)
        data_variable = get_variable(data, varera5)

        fig.suptitle(
            f"{title}",
            fontsize=14,
            x=0.5,
            position=(0.5, 0.95),
        )

        im_era5 = data_variable.plot(
            ax=axes[0, 0],
            levels=levels_era5,
            colors=colors_era5,
            transform=ccrs.PlateCarree(),
            extend="both",
            add_colorbar=False,
        )
        if shapefile is not None:
            shapefile.plot(ax=axes[0, 0], edgecolor='black', linewidth=0.5, facecolor='none')
        axes[0, 0].set_title(f'ERA5: {file.split("_")[5]}', fontsize=12)

    # Plot data for rcp26
    print('sims_rcp26',sims_rcp26)
    for i, file in enumerate(sims_rcp26):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
    
        # Select labels // Units frome metadata
        # Set title of plot
            
        s = "{}".format(title)
    
        fig.suptitle(s, 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.95)
                 )  

        im_diff = data_variable.plot(ax=axes[0, i + 1],
                    levels=levels_diff,
                    colors=colors_diff,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )
        if robustness is True:
            datar_variable = data['robustness']

            # Significant only when robustness equals ±1
            significant = xr.where(np.abs(datar_variable) == 1, 1, 0).squeeze()
            # do not plot NaN cells
            significant = significant.where(datar_variable.notnull())
            significant.plot.contourf(
                        ax=axes[0, i + 1],
                        levels=[-.5, .5],
                        colors='none',
                        # now hatches are applied to the not significant areas, with a grey color for the hatches
                        hatches=['', '//', ''],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        # Plot shapefile on current axis only if provided
        if shapefile is not None:
            shapefile.plot(ax=axes[0, i + 1], edgecolor='black', linewidth=0.5, facecolor='none')
        # This is not very clever, need to be adjusted according to file_name :-(
        axes[0, i + 1].set_title(f'RCP26: {file.split("_")[7]}',fontsize=12)
    
        if fancy:
            # Add north arrow and scalebar to all subplots
            arrowprops = dict(facecolor='black', edgecolor='black', width=1, headwidth=8, headlength=10)
            # If a shapefile is provided, build union geometry for accurate scalebar
            union_geom = shapefile.unary_union if shapefile is not None else None
            for ax in axes.flat:
                # Arrow pointing up in axes coordinates
                ax.annotate('', xy=(0.08, 0.85), xytext=(0.08, 0.65), xycoords='axes fraction', arrowprops=arrowprops)
                # Label "N" above the arrow
                ax.text(0.08, 0.86, 'N', transform=ax.transAxes, ha='center', va='bottom', fontsize=12)#, fontweight='bold')
                if union_geom is not None:
                    add_scalebar(ax, geom=union_geom, location='lower right', segments=4)

    # Plot data for rcp85
    for i, file in enumerate(sims_rcp85):
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=get_variable(data,var)
        
        im_diff = data_variable.plot(ax=axes[1, i + 1],
                           levels=levels_diff,
                           colors=colors_diff,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
        if robustness is True:
            datar_variable = data['robustness']

            # Significant only when robustness equals ±1
            significant = xr.where(np.abs(datar_variable) == 1, 1, 0).squeeze()

            # do not plot NaN cells
            significant = significant.where(datar_variable.notnull())

            significant.plot.contourf(
                        ax=axes[1, i + 1],
                        levels=[-.5, .5],
                        colors='none',
                        #hattches for1: significant values
                        #hatches=[None, None, "//", ],
                        # now hatches are applied to the not significant areas, with a grey color for the hatches
                        hatches=["", "//", ""],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )
        if shapefile is not None:
            shapefile.plot(ax=axes[1, i + 1], edgecolor='black', linewidth=0.5, facecolor='none')
        
        axes[1, i + 1].set_title(f'RCP85: {file.split("_")[7]}',fontsize=12)

    axes = np.atleast_2d(axes)

    for r in range(rows):
        for c in range(columns):
            ax = axes[r, c]

            if r == 1 and c == 0:
                ax.set_visible(False)
                continue

            gl = ax.gridlines(
                draw_labels=True,
                dms=True,
                x_inline=False,
                y_inline=False,
                linewidth=0.5,
            )
            gl.top_labels = False
            gl.right_labels = False
            gl.bottom_labels = (r == rows - 1)  # only bottom row
            gl.left_labels = (c == 0)           # only left column

            ax.coastlines(resolution="10m", color="black", linewidth=1)

            # optional: also hide matplotlib ticks on inner panels
            ax.tick_params(axis="x", labelbottom=(r == rows - 1), bottom=(r == rows - 1))
            ax.tick_params(axis="y", labelleft=(c == 0), left=(c == 0))

    if im_era5 is not None:
        if title=='':
            cbar_ax_era5 = fig.add_axes([0.11, 0.49, 0.22, 0.03])
        else:
            cbar_ax_era5 = fig.add_axes([0.11, 0.44, 0.22, 0.03])
        fig.colorbar(im_era5, cax=cbar_ax_era5, orientation="horizontal", label=f'[ {str(unit)} ]')

    if im_diff is not None:
        cbar_ax_diff = fig.add_axes([0.39, 0.04, 0.56, 0.03])
        fig.colorbar(im_diff, cax=cbar_ax_diff, orientation="horizontal", label=f'[ {str(unit)} ]')
   
    # Layout (space for colorbar at bottom)(left,bottom,right, top)
    fig.tight_layout(rect=[0.03, 0.08, 0.97, 0.99])
    # incase the mean is chosen instead of the median, the file name will be adjusted accordingly
    what = str.split(var, '_')[5]

    if title != "":
        name="{}/Compev_{}_{}_diff_{}.png".format(plotdir, var_pattern, what, user_dpi)
        if country is not None:
            name="{}/Compev_{}_{}_diff_{}_{}.png".format(plotdir, var_pattern, what, country, user_dpi)
    else:
        name="{}/Compev_{}_{}_diff_{}_{}_oT.png".format(plotdir, var_pattern , what, country, user_dpi)
    print('file is here:', name)
    fig.savefig("{}".format(name), dpi=user_dpi, bbox_inches="tight")

    return