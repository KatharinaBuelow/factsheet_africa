#!/usr/bin/env python3

import os
from pathlib import Path
import pandas as pd

from plotting_tools_africa import get_variable
import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xarray as xr

def savefig(plot, name, dpi):
    plot.savefig(name, dpi=dpi, bbox_inches='tight')
    print('plot ist saved in : ', name)
    return


def plot_diff_pop(
        pop_diff_ssp1,
        pop_diff_ssp3,
        level_steps_diff, 
        color_steps_diff, 
        plotdir,
        title="",
        var="",
        westafrica=None,
        user_dpi=1200,
        rows=2,
        columns=2,
        row_gap: float = 0.35,
        wspace: float | None = None,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    
    color_steps_diff = color_steps_diff[::-1]

    font = {
        'family' : 'sans-serif',
        'weight' : 'normal',
        }

    if westafrica is True:
        height=5.6
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
        figsize=(width,height), 
        subplot_kw={'projection': ccrs.PlateCarree()}) 
     
    # Apply user-defined spacing between rows (and optionally columns)
    if wspace is not None:
        fig.subplots_adjust(hspace=row_gap, wspace=wspace)
    else:
        fig.subplots_adjust(hspace=row_gap)
    
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

            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
                # Space between rows:
                fig.subplots_adjust(hspace=0.03)
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])

    # Plot data for ssp1
    for i, file in enumerate(pop_diff_ssp1):
        print('file: ',file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]/1000
        
        varname='Number of People'
        unit='Number*10³'
        
        s = "{} [{}]".format(title,varname)
    
        fig.suptitle(s+": ", 
                 #fontweight='bold', 
                 x=0.5,
                 fontsize=14,
                 position=(0.5, 0.93),
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=level_steps_diff,
                            colors=color_steps_diff,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        axes[0, i].set_title(f'ssp1: {file.split("_")[2]}-{file.split("_")[3]}',fontsize=12)

    # Plot data for ssp3
    for i, file in enumerate(pop_diff_ssp3):

        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable = data[var]/1000
        im = data_variable.plot(ax=axes[1, i],
                           levels=level_steps_diff,
                           colors=color_steps_diff,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )

        axes[1, i].set_title(f'ssp3: {file.split("_")[2]}-{file.split("_")[3]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_diff_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return


def plot_absolute_pop(
        pop_ssp1,
        pop_ssp3,
        level_steps, 
        color_steps,   
        plotdir,
        title="",
        var="",
        westafrica=None,
        user_dpi=300,
        rows=2, 
        columns=2,
        ):

    print(pop_ssp1)
    print(pop_ssp3)

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    
    # Some graphical features:
    if westafrica is True:
        height=5.2
    else:
        height=7
    if columns == 2:
        width=7
    elif columns == 3:
        width=10
    
    # Create subplots
    fig, axes = plt.subplots(
            ncols=columns, nrows=rows, figsize=(width,height), subplot_kw={'projection': ccrs.PlateCarree()}) 
  
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
            
            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # Plot data for ssp1

    for i, file in enumerate(pop_ssp1):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=data[var]/1000    
        # Select labels // Units frome metadata
        # Set title of plot
        if var =='number_of_people':
            varname='Number of People'
            unit='Number * 10³'

        s = "{} {}".format(varname, title)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.99)
                 )  
                
        im = data_variable.plot(ax=axes[0, i],
                            levels=level_steps,
                            colors=color_steps,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            #alpha=.8,
                            )
        # This is not very clever, need to be adjusted according to file_name :-(
        axes[0, i].set_title(f'ssp1: {file.split("_")[1]}-{file.split("_")[2]}',fontsize=12)

    # Plot data for ssp3
    for i, file in enumerate(pop_ssp3):
        data = xr.open_dataset(file,decode_timedelta=False)
        data_variable=data[var]/1000
        if var =='number_of_people':
            varname='Number of People'
            unit='Number *10³'
        im = data_variable.plot(ax=axes[1, i],
                           levels=level_steps,
                           colors=color_steps,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           #alpha=.8,
                           )
        
        axes[1, i].set_title(f'SSP3: {file.split("_")[1]}-{file.split("_")[2]}',fontsize=12)

    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ '+unit+' ]')

    name="{}/{}_absolut_{}_{}.png".format(plotdir, var, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi)
    return

def get_file_path(fullname):
    ''' Extract filepath'''
    import os
    from pathlib import Path

    #filename = os.path.basename(fullname)
    dirname = os.path.dirname(fullname)
    return dirname


def plot_diff_exposure(
        exposure_ssp1,
        exposure_ssp3,
        robust_rcp26,
        robust_rcp85,
        plot_dir,
        levels,   
        colors,     
        title="",
        var="",
        varr="",
        robustness=False,
        westafrica=None,
        user_dpi=300,
        rows=2,
        columns=2,
        ):

    from cartopy import crs as ccrs
    import cartopy.feature as cf
    from matplotlib.colors import ListedColormap

    # Some graphical features:
    custom_cmap = ListedColormap(colors)
    custom_cmap.set_bad(color='white')
    hatchcolor='grey'
    
    plt.rcParams.update({'hatch.color': hatchcolor})
    plt.rcParams["font.family"] = "sans-serif"    
    
    if westafrica is True:
        height=5.8
    else:
        height=7.5
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
        constrained_layout=True
    )
    # Apply user-defined spacing between rows (and optionally columns)
    #if wspace is not None:
    #    fig.subplots_adjust(hspace=row_gap, wspace=wspace, top=0.92, bottom=0.08)
    #else:
    #    fig.subplots_adjust(hspace=row_gap, top=0.92, bottom=0.08)
        
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

            if westafrica is True:
                region='West_Africa'
                ax.set_extent([-25, 20, -0.75, 27.3])
                # Space between rows:
                fig.subplots_adjust(hspace=0.03)
            else:
                region='Africa'
                ax.set_extent([-20, 60, -35, 35])
    
    # we need the path for later (probably easier way to handl this?)
    pathe=get_file_path(exposure_ssp1[0])
    pathr=get_file_path(robust_rcp26[0])
    
    im_list = []
    for i, file in enumerate(exposure_ssp1):
        print(file)
        data = xr.open_dataset(file,decode_timedelta=False)
    
        data_variable = data[var]/1000000
        mask_data= data_variable.where(data[var] != 0)
        #varname='Exposure'
        unit='Person-Events *10⁶'

        climate_index=varr
    
        s = "{} {}".format(title,climate_index)
    
        fig.suptitle(s+": ", 
                 fontsize=14, 
                 #fontweight='bold', 
                 x=0.5,
                 position=(0.5, 0.93)
                 )  
                
        im = mask_data.plot(ax=axes[0, i],
                            levels=levels,
                            cmap=custom_cmap,
                            transform=ccrs.PlateCarree(),
                            extend="both",#"neither",
                            add_colorbar=False,
                            alpha=.8,
                            )
        im_list.append(im)
        if robustness is True:
            robust_rcp26=file.replace('_ssp1_exposure_change.nc','_rcp26_ensemble-robustness.nc')
            robust_rcp26=robust_rcp26.replace(pathe,pathr)
            datar = xr.open_dataset(robust_rcp26)
            datar_variable = datar[varr]
            #datar_variable= datar_variable.where(data[var] != 0)
            significant = xr.where(~datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                        ax=axes[0, i],
                        levels=[-.5, .5],
                        colors='none',
                        hatches=[None, None, "//", ],
                        add_colorbar=False,
                        extend='both',
                        transform=ccrs.PlateCarree()
                        )

        # This is not very clever, need to be adjusted according to file_name :-(
        axes[0,i].set_title(f'SSP1/RCP26: {robust_rcp26.split("_")[6]}-{robust_rcp26.split("_")[7]}',fontsize=12)
        
   
    # Plot data for ssp3 rcp85

    for i, file in enumerate(exposure_ssp3):
        data = xr.open_dataset(file,decode_timedelta=False)
        
        data_variable = data[var]/1000000
        mask_data= data_variable.where(data[var] != 0)
        im = mask_data.plot(ax=axes[1, i],
                           levels=levels,
                           cmap=custom_cmap,
                           transform=ccrs.PlateCarree(),
                           extend="both",#"neither",
                           add_colorbar=False,
                           alpha=.8,
                           )
        im_list.append(im)
        if robustness is True:
            robust_rcp85=file.replace('_ssp3_exposure_change.nc','_rcp85_ensemble-robustness.nc')
            robust_rcp85=robust_rcp85.replace(pathe,pathr)
            datar = xr.open_dataset(robust_rcp85)
            datar_variable = datar[varr]
            mask_datar_variable= datar_variable.where(data[var] != 0)
            significant = xr.where(~mask_datar_variable.isin([-1, 1, 0]), 1, 0).squeeze()
            significant.plot.contourf(
                    ax=axes[1, i],
                    levels=[-.5, .5],
                    colors='none',
                    hatches=[ None,None,"//", ],
                    add_colorbar=False,
                    extend='both',
                    transform=ccrs.PlateCarree()
                )
        axes[1,i].set_title(f'SSP3/RCP85: {robust_rcp85.split("_")[6]}-{robust_rcp85.split("_")[7]}',fontsize=12)

    # Add colorbar axis; position may need tuning depending on row_gap
    #cbar_ax = fig.add_axes([0.15, 0.004, 0.7, 0.03])
    #fig.colorbar(im, cax=cbar_ax, orientation="horizontal", label='[ ' + unit + ' ]')
    #fig.colorbar(im, orientation="horizontal", shrink=0.85, label='[ ' + unit + ' ]')
    # common colorbar:
    fig.colorbar(im, ax=axes.ravel(), shrink=0.85, label='[ ' + unit + ' ]', orientation='horizontal')

    name="{}/{}_{}_diff-robust_{}_{}.png".format(plot_dir, var, varr, region, user_dpi)

    savefig(plt, "{}".format(name),user_dpi) 
    return
