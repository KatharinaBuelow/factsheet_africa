#!/usr/bin/env python3

#import os
import pandas as pd

import numpy as np
#import glob
#import matplotlib.pyplot as plt
import pandas as pd
#import seaborn as sns
#import xarray as xr

def select_region(df, region):
    return df.loc[(df["region"].isin([region]))]

def col_name(i):
    # Name der Spalte
    t = i.split("/")[-1]
    c = t.split(".cs")[0]
    return c

def col_obs_name(i):
    # Name der Spalte
    t = i.split("/")[-1]
    c = t.split(".cs")[0]
    return c

def read_obs(i, ind, frequency, saison,region):
    """Einlesen der saisonalen Referenzedaten """

    dft = pd.DataFrame()
    df = pd.read_csv(i)
    sel = select_region(df, region)
    c = col_obs_name(i)
    if ind in ["TG", "TX", "TN"]:
        sel[c] = sel[c] - 273.15

    if ind in ["RRm"] :
        #change unit from mm/day to mm/year
        sel[c] = sel[c].astype(float) * 365

    if saison == 12:
        dft["Index"] = sel["ci_name"]
        dfl = sel[c].map("{:,.1f}".format)

    else:
        sel_ = sel.loc[(sel["mid_month"].isin([saison]))]
        dfl = sel_[c].map("{:,.1f}".format)
        dft["Index"] = sel_["ci_name"].str.cat(sel_["mid_month"].values.astype(str))

    dft = pd.concat([dft, dfl], axis=1)
    return dft

def time_slice(files, region, dft, s, ind, fixh):
    # Es ist wichtig die Spalten hier klar zubenennen, sonst passiert ein Fehler.
    for ts in ("2031_2060", "2069_2098"):
        for rcp in ("rcp26", "rcp85"):
            dfile = sorted([f for f in files if ts in f and rcp in f])
            if not dfile:
                continue
            i = dfile[0]
            df = pd.read_csv(i)
            sel_ = select_region(df, region)
            c = col_name(i)
            sel = sel_.loc[(sel_["mid_month"].isin([s]))]
            if "diff-frac-" in c:
                t = sel[c]
                val = t * 100
                dfl = val.map("{:,.1f} %".format)
            elif fixh in c:
                #print('historical:', c)
                if ind in ["TG", "TX", "TN"]:
                    sel[c] = sel[c] - 273.15
                dfl = sel[c].map("{:,.1f}".format)
            else:
                dfl = sel[c].map("{:,.1f}".format)
            if ind in ["RRm"] and "ensemble-robustness" not in c:
                #change unit from mm/day to mm/year
                dfl = dfl.astype(float) * 365
            dft.reset_index(drop=True, inplace=True)
            dfl.reset_index(drop=True, inplace=True)
            # unclear wird ersetzt: 0 mit 0.5
            if "ensemble-robustness" in c:
                dfl = dfl.replace("0.0", "0.5")
            dft = pd.concat([dft, dfl], axis=1)
    return dft

def time_slice_mm(files):
    # Placeholder DataFrame for Min:Max robustness (no robustness -> fill with 0)
    dfmm = pd.DataFrame(["Min:Max"], columns=["ci_name"])
    dfd = pd.DataFrame(np.nan, index=[0], columns=["dummy"])
    dfmm = pd.concat([dfmm, dfd], axis=1)

    for ts in ("2031_2060", "2069_2098"):
        for rcp in ("rcp26", "rcp85"):
            dfile = sorted([f for f in files if ts in f and rcp in f])
            if not dfile:
                continue
            i = dfile[0]
            c = col_name(i)
            dfmm[c] = 0  # robustness placeholder

    return dfmm

def obs_robust(ind_, i):
    # Beobachtungen haben eine Robustheit
    if i == 12:
        ind = ind_
    else:
        ind = ind_ + str(i)
    dft = pd.DataFrame([ind], columns=["ci_name"])
    dfd = pd.DataFrame(0, index=[0], columns=["dummy"])
    dft = pd.concat([dft, dfd], axis=1)

    # Für Robustheit bleibt Min:Max nan
    dfmm = pd.DataFrame(["Min : Max"], columns=["ci_name"])
    dfm = pd.DataFrame(np.nan, index=[0], columns=["dummy"])
    dfmm = pd.concat([dfmm, dfm], axis=1)
    return dft, dfmm

def rename(df, ind, frequency, fixh, fixmh ,fix, fixm, fixr, rcp, time_period):
    # Umbenennen der Spalten des DataFrame
    # das wird der Name der in der Tabelle später zusehen ist

    df_ = df.copy()
    #print(' Renaming columns for index:', ind, ' RCP:', rcp, ' Time period:', time_period)
    
    #print(' Old column names:', ind + "_" + frequency + "_"+rcp+"_"+fix)
    return df_.rename(
        columns={
            "ci_name": "Index",
            ind + "_" + frequency + "_ref_time-mean": "1991-2020",
            "dummy": "1991-2020",
            #ind + "_" + frequency + "_" + time_period + "_" + rcp + "_" + fixh: rcp + ": " + time_period,
            #ind + "_" + frequency + "_" + time_period + "_" + rcp + "_" + fixmh: rcp + ": " + time_period,
            ind + "_" + frequency + "_" + time_period + "_" + rcp + "_" + fix: rcp + ": Δ " + time_period,
            ind + "_" + frequency + "_" + time_period + "_" + rcp + "_" + fixm: rcp + ": Δ " + time_period,
            ind + "_" + frequency + "_" + time_period + "_" + rcp + "_" + fixr: rcp + ": Δ " + time_period,
        },    
        )

def rename_index(df):
    # Umbenennen des Index
    df_ = df.copy()
    return df_.rename(
        index={
            "TG7": "Mean Temperature [°C]",
            "TR7": "Tropical nights (Tmin > 20°C) [nights]",
            "TR267": "Tropical nights (Tmin > 26°C) [nights]",
            "TN7": "Temperature Min. [°C]",
            "TX7": "Temperature Max. [°C]",
            "SU": "Summer days [days]",
            "SU30": "Heatdays (Tmax > 30°C) [days]",
            "SU357": "Temperature max. > 35°C [days]",
            "SU407": "Temperature max. > 40°C [days]",
            "FD": "Frost days [days]",
            "LFD": "Late frost days [days]",
            "HSx3": "Max. heatwave [days]",
            "HSf3": "Heatwaves [number]",
            "RRm7": "Annual precipitation [mm/year]",
            "RRm1": "Winter precipitation [mm/day]",
            "RRm4": "Spring precipitation [mm/day]",
            "RRm": "Summer precipitation [mm/day]",
            "RRm10": "Autumn precipitation [mm/day]",
            "DD1": "Dry days in winter [days]",
            "DD4": "Dry days in spring [days]",
            "DD": "Dry days in summer [days]",
            "DD10": "Dry days in autumn [days]",
            "DD7": "Dry days [days]",
            "PRCPTOT7": "Total precipitation on wet days [mm/year]",
            "RR17": "Wet days (RR > 1mm) [days]",
            "R20mm7": "Heavy precipitation (RR > 20mm) [days]",
            "DSx5": "Annual max. dry spell [days]",
            "DSf": "Annual dry spells [number]",
            "FG7": "Wind speed [m/s]",
            "FG1": "Winter [m/s]",
            "FG4": "Frühjahr [m/s]",
            "FG": "Sommer [m/s]",
            "FG10": "Herbst [m/s]",
        }
    )

def rename_columns(df_index):
    '''this is just for plotting the table header over two lines'''
    return df_index.rename(columns={
        'rcp26: Δ 2031_2060': 'rcp26:\nΔ 2031-2060', 
        'rcp85: Δ 2031_2060': 'rcp85:\nΔ 2031-2060', 
        'rcp26: Δ 2069_2098': 'rcp26:\nΔ 2069-2098',
        'rcp85: Δ 2069_2098': 'rcp85:\nΔ 2069-2098',
    })

def minmax(files, region, s, method):
    # Einlesen der Minimum und Maximum Dateien
    # Sie werden in eine Spalte gequetscht, damit sie später in der Tabelle unter dem Median zusehen sind.
    #print('in MM')
    #print(files)
    # Die Beobachtungen haben kein Minimum und Maximum, da es nur 1 Datenfile gibt.
    dft = pd.DataFrame(["Min:Max"], columns=["ci_name"])
    dfd = pd.DataFrame(np.nan, index=[0], columns=["dummy"])
    dft = pd.concat([dft, dfd], axis=1)
    
    for i in files:
        
        if method == "pro":
            minfile = i.replace("diff-frac-median", "diff-frac-min")
            maxfile = i.replace("diff-frac-median", "diff-frac-max")
        else:
            minfile = i.replace("-median.csv", "-min.csv")
            maxfile = i.replace("-median.csv", "-max.csv")
     
        dfmin = pd.read_csv(minfile)
        dfmax = pd.read_csv(maxfile)

        seln_ = select_region(dfmin, region)
        selx_ = select_region(dfmax, region)
        seln = seln_.loc[(seln_["mid_month"].isin([s]))]
        selx = selx_.loc[(selx_["mid_month"].isin([s]))]
        
        cmin = col_name(minfile)
        cmax = col_name(maxfile)
        

        if method == "pro":
            endcmax = cmax.split("-")[4]
            t = seln[cmin]
            val_cmin = t * 100
            tm = selx[cmax]
            val_cmax = tm * 100
            dfn = val_cmin.map("{:,.1f}".format)
            dfm = val_cmax.map("{:,.1f}".format)
        else:
            tmp = cmax.split(".")[0]
            endcmax = tmp.split("-")[-1]
            #print('endcmax: ', endcmax)
            dfn = seln[cmin].map("{:,.1f}".format)
            dfm = selx[cmax].map("{:,.1f}".format)

        dfn_ = dfn.reset_index(drop=True)
        dfm_ = dfm.reset_index(drop=True)
        dft_ = pd.concat([dft, dfn_, dfm_], axis=1)
        dft__ = dft_.replace("0.0", "0")
        dft = dft__.replace("-0.0", "0")
        dft[cmin + "-" + endcmax] = dft[cmin] + " : " + dft[cmax]
        dft.drop([cmin, cmax], inplace=True, axis=1)

    return dft

# Die Tabelle klarer gestalten:

def add_plus(value):
    float_value = float(value)
    if float_value > 0:
        return "+" + str(float_value)
    else:
        return str(float_value)
    
    # some graphic style tools:

# Design:
# Schrift größe bestimmen

def annotate_row(row_index):
    # Always return a list with length equal to the number of columns (5)
    if row_index == "Min:Max":
        return [10] * 5  # Font sizes for each column in row
    else:
        return [14] * 5  # Default font sizes


def annotate_row_weight(row_index):
    # Always return a list with length equal to the number of columns (5)
    if row_index == "Min:Max":
        return ["light"] * 5
    else:
        return ["bold"] * 5


def label_color(label): 
    # Always return a color for the label
    if label in ["Mean Temperature [°C]","Temperature Max. [°C]", "Temperature Min. [°C]"]:
        return "#dcab4c"
    if label in ["Tropical nights (Tmin > 26°C) [nights]", "Temperature max. > 35°C [days]","Temperature max. > 40°C [days]"]:
        return "#cf6752"
    if label == "Hitzewellen [Anzahl]":
        return "#cf6752"
    if label == "Dry days [days]":
        return "#97b0ca"
    if label  in ["Wet days (RR > 1mm) [days]","Heavy precipitation (RR > 20mm) [days]","Annual precipitation [mm/year]","Total precipitation on wet days [mm/year]"]:
        return "#615793"
    if label == "jährl. max.Trockenperiode [Tage]":
        return "#882a4f"
    if label == "Wind speed [m/s]":
        return "#609C88"
    else:
        return "#636363"  # Default color (black)
    