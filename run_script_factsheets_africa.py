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

final_pdf_name ='Test_Burkina_Faso_reportlab.pdf'
region = 'Burkina Faso'
anzahl_simulationen = 18
version = '1'
gerics_logo = 'logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png'
bmbf_logo='logos/BMFTR_en_DTP_CMYK_gef_durch.jpg'
wascal_logo='logos/WASCAL_Logo.png'
title_image_burkinafaso = 'country_map/FS_Burkina_Faso.png'
box_era5 = 'test-pictures/EOBS_Annual_anomaly_deviation-2023_to_1971_2000_08212_08215_07334_Region_um_Karlsruheneu_1200.png'
table_cc = 'test-pictures/Karlsruhe_table_GWL_08212_08215_07334_Region_um_Karlsruhe_median_grey_1200_update.png'
basic_color = [233,104,33]
sprache = 'english'
cs_orange = colors.Color(basic_color[0]/255., basic_color[1]/255., basic_color[2]/255.)
cs_schwarz = colors.Color(0 / 255., 0 / 255., 0 / 255., 1)
doc = FactSheet(final_pdf_name, version, region, gerics_logo, wascal_logo, bmbf_logo, basic_color, sprache, cs_orange, cs_schwarz, \
                title_image_burkinafaso, box_era5, table_cc,anzahl_simulationen)

doc.createDocument()
doc.savePDF()

