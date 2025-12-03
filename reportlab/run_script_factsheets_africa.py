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

final_pdf_name ='Test_factsheet_Burkina_Faso.pdf'
region = 'Burkina Faso'
anzahl_simulationen = 18
version = '1'
gerics_logo = '/home/buelow/github/factsheet_africa/logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png'
bmbf_logo='/home/buelow/github/factsheet_africa/logos/BMFTR_en_DTP_CMYK_gef_durch.jpg'
wascal_logo='/home/buelow/github/factsheet_africa/logos/WASCAL_Logo.png'
title_image_burkinafaso = '/home/buelow/Downloads/factsheet_africa/PLOTS/COUNTRY/FS_Burkina_Faso.png'
box_era5 = '/home/buelow/Downloads/factsheet_africa/PLOTS/ERA5-Plots-climatestripes/ERA5_Annual_anomaly_deviation_to_1991_2020_Burkina_Faso_nc.png'
table_cc = '/home/buelow/Downloads/factsheet_africa/PLOTS/Table/Table_Burkina_Faso_median_grey_300.png'
ts_TG_era5 = '/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_TG_year_Burkina_Faso_ERA5.png'
ts_su40_era5 = '/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_SU40_year_Burkina_Faso_ERA5.png'
ts_RRm_era5 = '/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_RRmm_year_Burkina_Faso_ERA5.png'
ts_DD_era5 = '/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_DD_year_Burkina_Faso_ERA5.png'
ts_R20mm_era5 = '/home/buelow/Downloads/factsheet_africa/PLOTS/AFR22_timeseries/line_plot_min_max_R20mm_year_Burkina_Faso_ERA5.png'
hori_SU40_abs = '/home/buelow/Downloads/factsheet_africa/PLOTS/horizontal-plots-exposure/SU40_absolut_West_Africa_1200.png'


basic_color = [233,104,33]
sprache = 'english'
cs_orange = colors.Color(basic_color[0]/255., basic_color[1]/255., basic_color[2]/255.)
cs_schwarz = colors.Color(0 / 255., 0 / 255., 0 / 255., 1)
doc = FactSheet(final_pdf_name, version, region, gerics_logo, wascal_logo, bmbf_logo, basic_color, sprache, cs_orange, cs_schwarz, \
                title_image_burkinafaso, box_era5, table_cc, anzahl_simulationen, \
                ts_TG_era5, ts_su40_era5, ts_RRm_era5, ts_DD_era5, ts_R20mm_era5, hori_SU40_abs)

doc.createDocument()
doc.savePDF()

