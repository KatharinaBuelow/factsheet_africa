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
from reportlab_template_fuer_katharina import *

#################---------------------------##############################---------------------------########################-------------------

final_pdf_name ='Test_Burkina_Faso_reportlab.pdf'
region = 'Burkina Faso'
anzahl_simulationen = 18
version = '1'
gerics_logo = '/work/ch0636/g300047/cicles/Factsheets/logos/Logo_GERICS_Neu_mit_Unterzeile_EN.png'
bmbf_logo='/work/ch0636/g300047/cicles/Factsheets/logos/BMFTR_en_DTP_CMYK_gef_durch.jpg'
wascal_logo='/work/ch0636/g300047/cicles/Factsheets/logos/WASCAL_Logo.png'
title_image_burkinafaso = '/work/ch0636/g300047/cicles/Factsheets/country_map/FS_Burkina_Faso.png'
basic_color = [233,104,33]
sprache = 'english'
cs_orange = colors.Color(basic_color[0]/255., basic_color[1]/255., basic_color[2]/255.)
cs_schwarz = colors.Color(0 / 255., 0 / 255., 0 / 255., 1)
title_pic = "/work/ch0636/g300047/cicles/Factsheets/pictures/orange_block.jpg"
doc = FactSheet(final_pdf_name, version, region, gerics_logo, wascal_logo, bmbf_logo, title_pic, basic_color, sprache, cs_orange, cs_schwarz, title_image_burkinafaso,anzahl_simulationen)

doc.createDocument()
doc.savePDF()

