#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Dies ist der automatische regional Climate-Fact-Sheet-Generator.
Er erstellt ein pdf-Dokument angelehnt an das GERICS Climate Fact Sheet Design unter Verwendung
von reportlab.
Die Datenbasis sind AFR22-CORDEX-Simulationen.
Die Struktur des Dokuments ist in der Klasse FactSheet definiert.
#
"""
import os
import sys
here = os.path.abspath(os.getcwd())
sys.path.append(here+'/')
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
from reportlab.lib import utils
from six import string_types
from netCDF4 import Dataset
import re
import pandas as pd
from title_page_africa import insert_title_page
from page_with_table import insert_page_with_table
from background_information import insert_impressum

#####################################################################
def get_image(path, height=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, height=height, width = (height/ aspect))

#####################################################################
def createTable(self, content, columnwidths, rowheights, x, y, style):
        """
        Vordefinierte Tabelle
        """
        table = Table(content, colWidths=columnwidths, rowHeights=rowheights)
        try:
            if not style:
                table.setStyle([("VALIGN", (0, 0), (0, 0), "TOP"),
                            ('BACKGROUND', (0, 0), (1, 1),
                             (colors.Color(255 / 255., 255 / 255., 204 / 255., 1)))])
            else:
                table.setStyle(style)
        except:
            0
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, x, y)
#####################################################################

class FactSheet(object):
    """
    Bitte eintragen
    """

    def __init__(self, pdf_file, version, region, gerics_logo, wascal_logo, bmbf_logo, basic_color, sprache, cs_orange, cs_schwarz,
                 title_image_burkinafaso, box_era5, table_cc, anzahl_simulationen):
        self.c = canvas.Canvas(pdf_file, pagesize=A4)
        self.c.setFont('Helvetica', 12)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leftIndent=0,))
        self.styles.add(ParagraphStyle(name='Heading', alignment=TA_JUSTIFY, font_size=12))
        self.styles.add(ParagraphStyle(name='SmallTableContent', alignment=TA_LEFT, font_size=8))
        self.styles.add(ParagraphStyle(name='Image_caption', alignment=TA_JUSTIFY, font_size=6, leading=8))
        self.styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(name='Centered', parent=self.styles['Justify'], alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(name='alert', parent=self.styles['Justify'], leading=14,
                                       backColor=
                                       colors.Color(255 / 255., 192 / 255., 203 / 255., 0.75),
                                       borderColor=
                                       colors.Color(178 / 255., 34 / 255., 34 / 255.),
                                       borderWidth=1, borderPadding=5, borderRadius=2,
                                       spaceBefore=10, spaceAfter=10, display="inline-block", margin=100))
        self.styleN = self.styles["BodyText"]
        self.styleN.alignment = TA_LEFT
        self.pdf_file = pdf_file
        self.region = region
        self.version = version
        self.gerics_logo = gerics_logo
        self.bmbf_logo = bmbf_logo
        self.wascal_logo = wascal_logo
        self.basic_color = basic_color
        self.sprache = sprache
        self.cs_orange = cs_orange
        self.cs_schwarz = cs_schwarz
        self.title_image_burkinafaso = title_image_burkinafaso
        self.box_era5 = box_era5
        self.table_cc = table_cc
        self.anzahl_simulationen = anzahl_simulationen

    #----------------------------------------------------------------------
    def savePDF(self):
        """
        Abspeichern als pdf
        """
        self.c.setSubject('Projected climate changes for '+self.region+', based on AFR22-CORDEX simulations')
        self.c.setTitle('Climate Factsheet ' + self.region +', '+ self.version)
        self.c.setAuthor('Climate Service Center Germany (GERICS), 2025')
        self.c.setCreator('Climate Service Center Germany (GERICS), 2025')

        self.c.save()

    def add_footline(self, left_right):
        logo = get_image(self.gerics_logo, height =  1.2 * cm)
        logo_breite = logo.drawWidth
        logo_hoehe = logo.drawHeight
        second_foot = ([[logo]])
        foot_style = ([("VALIGN", (0, 0), (0, 0), "BOTTOM"),
                      ("ALIGN", (0, 0), (0, 0), "CENTER"),])
        page_num = self.c.getPageNumber()
        text1 = "Climate Factsheet"
        t1 = Paragraph('<span name=Helvetica color=black size = 8>%s</span>' % text1, self.styles['Justify'], encoding='utf8')
        t1w, t1b = t1.wrapOn(self.c, self.width, self.height)
        self.c.setFillColor(self.cs_orange)
        text2 = Paragraph('<span name=Helvetica color=rgb('+str(self.basic_color[0])+','+str(self.basic_color[1])+','+str(self.basic_color[2])+') size=8>'+self.region.title()+' </span>',
                         self.styles['Justify'], encoding='utf8')
        text2.wrapOn(self.c, self.width - self.text_offset_rechts - self.text_offset_links, self.height)
        text3 = str(page_num)
        self.c.setFont('Helvetica', 10)
        self.c.setFillColor(self.cs_schwarz)
        text_mitte = Paragraph('<span name=Helvetica color=black size = 12>''</span>', self.styles['Justify'], encoding='utf8')
        tmw, tmh = text_mitte.wrapOn(self.c, self.width, self.height)
        textWidth = stringWidth("", 'Helvetica', 10)
        if left_right == 'gerade_even':
            self.c.setFont('Helvetica', 10)
            text2.drawOn(self.c, self.text_offset_links, 0.6 * cm - 0.25*cm)
            self.c.drawString(0.5*self.width -textWidth*0.5 - 0.5*cm, 0.75 * cm - tmh*0.25, "")
            self.c.setFillColor(self.cs_schwarz)
            self.c.setFont('Helvetica', 8)
            self.c.drawString(self.text_offset_links, 0.9 * cm - 0.1*cm, text1)
            self.c.setFillColor(self.cs_orange)
            self.c.setFillColor(colors.Color(0 / 255., 0 / 255., 0 / 255., 1))
            self.c.drawString(0.75 * cm, 0.75 * cm, text3)
            createTable(self, second_foot, logo_breite, (logo_hoehe), self.width - self.text_offset_rechts - logo_breite*0.55 - self.kleiner_abstand,
                          0.1* cm, foot_style)
        elif left_right == 'ungerade_odd':
            t1_width = stringWidth(text1, 'Helvetica', 8, 'utf-8')
            text2_t = self.region
            t2_width = stringWidth(text2_t, 'Helvetica', 8, 'utf-8')
            text2.drawOn(self.c,self.width  -self.text_offset_rechts -t2_width, 0.6 * cm - 0.25*cm)
            self.c.setFont('Helvetica', 10)
            self.c.drawString(0.5*self.width -textWidth*0.5 - 0.5*cm, 0.75 * cm - tmh*0.25, "")
            self.c.setFont('Helvetica', 8)
            self.c.drawString(self.width  -self.text_offset_rechts -t1_width, 0.9 * cm - 0.1*cm, text1)
            self.c.setFillColor(self.cs_orange)
            self.c.setFillColor(self.cs_orange)
            self.c.setFillColor(colors.Color(0 / 255., 0 / 255., 0 / 255., 1))
            self.c.drawString(self.width - 1*cm, 0.75 * cm, text3)
            createTable(self, second_foot, logo_breite, (logo_hoehe), 0.*cm + self.kleiner_abstand,
                          0.1* cm, foot_style)
        else:
            raise Exception(left_right, 'unknown')

    def createDocument(self):
        """
        creats climate factsheet
        """
# ---------- allgemeine Definitionen
        heute = datetime.today()
        cs_orange_trans = colors.Color(240 / 255., 131 / 255., 1 / 255., 0.75)
        self.text_offset_links = self.width - 19. * cm
        self.text_offset_rechts = self.width - 19.5 * cm
        self.breite = self.width - self.text_offset_links - self.text_offset_rechts
        self.abstand_zu_title = 1.5 * cm
        self.abstand_zu_subtitle = 1. * cm
        self.kleiner_abstand = 0.5 * cm
        varia_breite = 2.5 * cm
        self.schrift_tabellen = 8
        self.schrift_fliesstext = 10
        print('Starte mit der Erstellung des Dokuments in make... ')
# ----------- Header der Titelseite
        title_page = insert_title_page(self)
        foot_1 = self.add_footline('ungerade_odd')
# -------Seitenumbruch auf  Seite 2
        self.c.showPage()
        Table_page = insert_page_with_table(self)
        foot_2 = self.add_footline('gerade_even')
# -------Seitenumbruch
        self.c.showPage()
        impressum_page = insert_impressum(self)


