#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Run script for creating cicles factsheets.


"""
import warnings
warnings.filterwarnings("ignore")

import os, glob
import sys
here = os.path.abspath(os.getcwd())
sys.path.append(here+'/')
import re
from reportlab_template_africa import *

#################---------------------------##############################---------------------------########################-------------------
#region = 'Burkina Faso'
#region= 'Togo'
region ='Ivory Coast'

final_pdf_name ='Test_Factsheet_'+region.replace(' ', '_')+'.pdf'
anzahl_simulationen = 18
version = '1'
gerics_logo = '/home/buelow/github/factsheet_africa/logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png'
bmbf_logo='/home/buelow/github/factsheet_africa/logos/BMFTR_en_DTP_CMYK_gef_durch.jpg'
wascal_logo='/home/buelow/github/factsheet_africa/logos/WASCAL_Logo.png'
title_image = f"/home/buelow/Downloads/factsheet_africa/PLOTS/COUNTRY/FS_{region.replace(' ', '_')}.png"
box_era5 = f"/home/buelow/Downloads/factsheet_africa/PLOTS/ERA5-Plots-climatestripes/ERA5_Annual_anomaly_deviation_to_1991_2020_{region.replace(' ', '_')}_nc.png"
table_cc = f"/home/buelow/Downloads/factsheet_africa/PLOTS/Table/Table_{region.replace(' ', '_')}_median_grey_300.png"
ts_TG_era5 = f"/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_TG_year_{region.replace(' ', '_')}_ERA5.png"
ts_su40_era5 = f"/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_SU40_year_{region.replace(' ', '_')}_ERA5.png"
ts_RRm_era5 = f"/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_RRm_year_{region.replace(' ', '_')}_ERA5.png"
ts_DD_era5 = f"/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_DD_year_{region.replace(' ', '_')}_ERA5.png"
ts_R20mm_era5 = f"/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_R20mm_year_{region.replace(' ', '_')}_ERA5.png"
hori_SU40_abs = '/home/buelow/Downloads/factsheet_africa/PLOTS/horizontal-plots-exposure/SU40_absolut_West_Africa_1200.png'
copev_su40_tr26='/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_compound_events/SU40_du3_TR26_du3_median_absolut_West_Africa_1200.png'
copev_su40_DD='/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_compound_events/SU40_du3_DD_du5_median_absolut_West_Africa_1200.png'

basic_color = [233,104,33]
sprache = 'english'
cs_orange = colors.Color(basic_color[0]/255., basic_color[1]/255., basic_color[2]/255.)
cs_schwarz = colors.Color(0 / 255., 0 / 255., 0 / 255., 1)
doc = FactSheet(final_pdf_name, version, region, gerics_logo, wascal_logo, bmbf_logo, basic_color, sprache, cs_orange, cs_schwarz, \
                title_image, box_era5, table_cc, anzahl_simulationen, \
                ts_TG_era5, ts_su40_era5, ts_RRm_era5, ts_DD_era5, ts_R20mm_era5, hori_SU40_abs,copev_su40_DD,copev_su40_tr26)

doc.createDocument()
doc.savePDF()

