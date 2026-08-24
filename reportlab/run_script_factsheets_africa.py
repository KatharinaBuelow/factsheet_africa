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
region = 'Burkina Faso'
sector = 'Agriculture'
#region= 'Togo'
#sector = 'Water'
#region ='Ivory Coast'
#sector = 'Health'

final_pdf_name ='Test_Factsheet_'+region.replace(' ', '_')+'.pdf'
anzahl_simulationen = 18
version = '1'
gerics_logo = '/Users/Buelow/github/factsheet_africa/logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png'
bmbf_logo='/Users/Buelow/github/factsheet_africa/logos/BMFTR_en_DTP_CMYK_gef_durch.jpg'
wascal_logo='/Users/Buelow/github/factsheet_africa/logos/WASCAL_Logo.png'
hereon_logo='/Users/Buelow/github/factsheet_africa/logos/HEREON_logo.png'
rcp_image='/Users/Buelow/github/factsheet_africa/reportlab/emissionen_rcp.png'
timeseries_theorie = '/Users/Buelow/github/factsheet_africa/reportlab/ts_theorie.png'
box_theorie = '/Users/Buelow/github/factsheet_africa/reportlab/box_theorie.png'
title_image = f"/Users/Buelow/github/factsheet_africa/PLOTS/country/FS_{region.replace(' ', '_')}.png"
box_era5 = f"/Users/Buelow/github/factsheet_africa/PLOTS/ERA5_anomaly/ERA5_Annual_anomaly_deviation_to_1991_2020_{region.replace(' ', '_')}_nc.png"
table_cc = f"/Users/Buelow/github/factsheet_africa/PLOTS/table/Table_{region.replace(' ', '_')}_median_1200.png"
ts_TG_anomaly = f"/Users/Buelow/github/factsheet_africa/PLOTS/timeseries/TG/TG_{region.replace(' ', '_')}_timeseries_box_minmax_p15p85_oT.png"
ts_su40_anomaly = f"/Users/Buelow/github/factsheet_africa/PLOTS/timeseries/SU40/SU40_{region.replace(' ', '_')}_timeseries_box_minmax_p15p85_oT.png"
ts_RRm_anomaly = f"/Users/Buelow/github/factsheet_africa/PLOTS/timeseries/RRm/RRm_{region.replace(' ', '_')}_timeseries_box_minmax_p15p85_oT.png"
ts_DD_anomaly = f"/Users/Buelow/github/factsheet_africa/PLOTS/timeseries/DD/DD_{region.replace(' ', '_')}_timeseries_box_minmax_p15p85_oT.png"
ts_R20mm_anomaly = f"/Users/Buelow/github/factsheet_africa/PLOTS/timeseries/R20mm/R20mm_{region.replace(' ', '_')}_timeseries_box_minmax_p15p85_oT.png"
hori_SU40_abs = '/Users/Buelow/github/factsheet_africa/PLOTS/horizontal-plots-exposure/SU40_absolut_West_Africa_1200.png'
copev_su40_tr26='/Users/Buelow/github/factsheet_africa/PLOTS/AFR22_compound_events_diff_era5/Compev_SU40_du3_TR26_du3_median_diff_Burkina_Faso_1200_oT.png'
copev_su40_DD='/Users/Buelow/github/factsheet_africa/PLOTS/AFR22_compound_events_diff_era5/Compev_SU40_du7_DD_du7_median_diff_Burkina_Faso_1200_oT.png'
basic_color = [233,104,33]
sprache = 'english'
cs_orange = colors.Color(basic_color[0]/255., basic_color[1]/255., basic_color[2]/255.)
cs_schwarz = colors.Color(0 / 255., 0 / 255., 0 / 255., 1)
doc = FactSheet(final_pdf_name, version, region, sector, gerics_logo, wascal_logo, bmbf_logo, hereon_logo, 
                timeseries_theorie, box_theorie,\
                basic_color, sprache, cs_orange, cs_schwarz, \
                title_image, box_era5, table_cc, anzahl_simulationen, \
                ts_TG_anomaly, ts_su40_anomaly, ts_RRm_anomaly, \
                ts_DD_anomaly, ts_R20mm_anomaly, hori_SU40_abs, \
                copev_su40_DD,copev_su40_tr26, rcp_image)

doc.createDocument()
doc.savePDF()

