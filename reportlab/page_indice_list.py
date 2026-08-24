import os
import sys
import numpy
import scipy
import scipy.stats
import collections
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table, Flowable, PageBreak, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import ListItem, ListFlowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from utils_image import get_image
from six import string_types
from netCDF4 import Dataset
from reportlab.platypus import Image
import re
import pandas as pd



def insert_glossar_page(self, glossar_dict, variables):
        #back = Image(self.background)
        #back.drawHeight = self.height - 4.75 * cm
        #back.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts
        #back.wrapOn(self.c, self.width, self.height)
        #back.drawOn(self.c, self.text_offset_links, 1.75 * cm)
        
    header_left = ParagraphStyle(
        name="HeaderLeft",
        parent=self.styles["SmallTableContent"],
        alignment=TA_LEFT,
        leftIndent=0,
        firstLineIndent=0,
    )

    einfuegehoehe_top = self.height - 2 * cm
    # Titel: 
    title_text = "DEFINITION OF CLIMATE INDICATORS" if self.sprache == 'english' else "DEFINITION DER KLIMAINDIKATOREN"
    title_h = self.draw_header(title_text, einfuegehoehe_top)
    # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand

    index = 0
    var_col_width = 4.*cm
    content = []
    columnwidths = (var_col_width, self.width - self.text_offset_links - self.text_offset_rechts - var_col_width) # - 0.5 *cm)
    #heights = [0.45 * cm] * (len(variables))
    heights = []
    heights.insert(0, 1. * cm)
    font_size = 12
    font_size2 = 12
    content.append((
    Paragraph('<span name=Helvetica-bold color=black size='+str(font_size)+'>CLIMATE INDEX</span>', style=header_left),
    Paragraph('<span name=Helvetica-bold color=black size='+str(font_size)+'>DEFINITION</span>', style=header_left)
    ))

    variables='TG','TX','TN','SU35','SU40','TR26','RRm','DD','RR1', 'R20mm', 'FG','SU40_du3_DD_du5'
    for var in variables:
            text_zeile = Paragraph('<span name=Helvetica color=black size ='+str(font_size2)+'>'+glossar_dict[var][1]+'</span>', style=self.styles['SmallTableContent'])
            ##breite, hoehe = text_zeile.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - var_col_width, self.height)
            breite, hoehe = text_zeile.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - var_col_width - 1. *cm, self.height)
            varara = Paragraph('<span name=Helvetica color=black size ='+str(font_size2)+'>'+glossar_dict[var][0]+'</span>', style = self.styles['SmallTableContent'])
            breite2, hoehe2 = varara.wrapOn(self.c, var_col_width , self.height)
            content.append((varara, text_zeile))
            #print( hoehe, hoehe2)
            self.hoehe = hoehe
            heights.append(max(hoehe+ 0.25 * cm, hoehe2+ 0.25 * cm)+ 0.2 * cm)
    dum = heights.pop(-1)
    heights.append(dum + 0.25*cm)
    table = Table(content, colWidths=columnwidths, rowHeights=heights)
    table.setStyle([("VALIGN", (0, 0), (1, 0), "MIDDLE"),
                        ("VALIGN", (0, 1), (1, -1), "CENTER"),
                        ("ALIGN", (0, 0), (0, -1), "LEFT"),
                        ("GRID", (0,0), (-1,-1), 0.25, colors.gray),
                        ('BACKGROUND', (0, 0), (-1, -1), (colors.Color(255 / 255., 255 / 255., 255 / 255., 1)))])
    table.wrapOn(self.c, self.width, self.height)
    table.drawOn(self.c, self.text_offset_links, einfuegehoehe_top -0.25 * cm - numpy.sum(heights))

        #table.drawOn(self.c, self.text_offset_links + 0.25*cm, einfuegehoehe_top -0.25 * cm - numpy.sum(heights))
# Katharina noch bearbeiten für 2 Sprache

def return_glossar_en(english=True):
    glossar_dict = {
        'TG': ['Temperature', 
           'The temperature refers to near-surface air temperature (2 m above ground). '
           'Annual and seasonal means are calculated using daily mean temperatures. '
           'Seasonal means follow the meteorological year: winter = December–February, '
           'spring = March–May, summer = June–August, autumn = September–November.'],
        'TX': ['Maximum Temperature', 
           'The temperature refers to near-surface air temperature (2 m above ground). '
           'Annual and seasonal means are calculated using daily maximum temperatures.'],
        'TN': ['Minimum Temperature', 
           'The temperature refers to near-surface air temperature (2 m above ground). '
           'Annual and seasonal means are calculated using daily minimum temperatures.'],
        'SU30': ['Hot Days', 
             'Number of days per year with a daily maximum temperature above 30 °C.'],
        'SU35': ['Very Hot Days', 
             'Number of days per year with a daily maximum temperature above 35 °C.'],
        'SU40': ['Extremely Hot Days', 
             'Number of days per year with a daily maximum temperature above 40 °C.'],
        'TR26': ['Tropical Nights', 
           'Number of days per year with a daily minimum temperature above 20 °C.'],
        'CHD30x': ['Maximum Duration of Heatwaves', 
               'Annual maximum duration of periods when the daily maximum temperature exceeds 30 °C.'],
        'RRm': ['Precipitation', 
            'Precipitation values are calculated based on daily totals and given as average yearly sums in mm per year'
            'Values include both liquid and solid precipitation (rain and snow)'],
        'R5mm': ['Precipitation ≥ 5 mm/day', 
             'Number of days per year with precipitation (rain and snow) exceeding 5 mm.'],
        'R10mm': ['Precipitation ≥ 10 mm/day', 
              'Number of days per year with precipitation (rain and snow) exceeding 10 mm.'],
        'R15mm': ['Precipitation ≥ 15 mm/day', 
              'Number of days per year with precipitation (rain and snow) exceeding 15 mm.'],
        'R20mm': ['Precipitation ≥ 20 mm/day', 
              'Number of days per year with precipitation (rain and snow) reaching or exceeding 20 mm.'],
        'R25mm': ['Precipitation ≥ 25 mm/day', 
              'Number of days per year with precipitation (rain and snow) exceeding 25 mm.'],
        'DD': ['Dry Days', 
           'Number of days per year with precipitation (rain and snow) below 1 mm.'],
        'RR1': ['Wet Days', 
            'Number of days per year with precipitation (rain and snow) of at least 1 mm.'],
        'FG': ['Wind Speed', 
           'Mean annual wind speed in m/s.'],
        'HSx3': ['Maximum Duration of Heatwaves', 
             'Annual maximum length of periods with at least three consecutive days exceeding a daily maximum temperature of 30 °C.'],
        'HSf3': ['Mean Frequency of Heatwaves', 
             'Annual mean number of periods with at least three consecutive days exceeding a daily maximum temperature of 30 °C.'],
        'DSf': ['Mean Frequency of Dry Periods', 
            'Annual mean number of periods with at least five consecutive days with precipitation below 1 mm.'],
        'DSx5': ['Maximum Duration of Dry Periods', 
             'Annual maximum length of periods with at least five consecutive days with precipitation below 1 mm.'],
        'SU40_du3_DD_du5': ['Compound Heatdays and Dry Days events', 
             'Annual mean number of compound events combining at least 3 consecutive heatdays and at least 4 consecutive dry days.'],
        'SU40_du3_TR26_du3': ['Compound Heatdays and Tropical Nights events', 
             'Annual mean number of compound events combining at least 3 consecutive heatdays and at least 3 consecutive tropical nights.'],
    }
    return glossar_dict

def return_glossar_fr():
    glossar_dict = {
        'TG': ['Température', 'La température fait référence à la température de l’air près de la surface (2 m au-dessus du sol). ...'],
        # Add all glossary entries in French here
    }
    return glossar_dict

def return_glossar(sprache='english'):
    if sprache.lower() in ['fr', 'français']:
        return return_glossar_fr()
    else:
        return return_glossar_en()