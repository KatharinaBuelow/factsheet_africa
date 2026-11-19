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
from page_temperature import insert_page_temperature
from page2_temperature import insert_page2_temperature
from page3_temperature import insert_page3_temperature
from page_precipitation import insert_page_precipitation
from page2_precipitation import insert_page2_precipitation
from page_wind import insert_page_wind
from page_comp_ev import insert_page_compound_event
from page2_comp_ev import insert_page2_compound_event
from page_scenario_robust import insert_page_explain
from page_reading_instruction import insert_page_reading_instructions
from page_indice_list import insert_glossar_page
from page_models_data import insert_page_with_models_data
from last_page_background_information import insert_impressum
from page_back import insert_page_back

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

    def __init__(self, pdf_file, version, region, sector, 
                 gerics_logo, wascal_logo, bmbf_logo, hereon_logo,
                 timeseries_theorie, box_theorie,
                 basic_color, sprache, cs_orange, cs_schwarz,
                 title_image, box_era5, table_cc,
                 ts_TG_anomaly=None, ts_TN_anomaly=None, ts_TX_anomaly=None, ts_TR26_anomaly=None, ts_SU35_anomaly=None, ts_SU40_anomaly=None,
                 ts_RRm_anomaly=None, ts_DD_anomaly=None, ts_R20mm_anomaly=None, ts_RR1_anomaly=None, ts_FG_anomaly=None,
                 hori_SU40_abs=None, copev_su40_DD=None, copev_su40_tr26=None, rcp_image=None):
        self.c = canvas.Canvas(pdf_file, pagesize=A4)
        self.c.setFont('Helvetica', 12)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.story = []
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
        self.sector = sector
        self.version = version
        self.gerics_logo = gerics_logo
        self.bmbf_logo = bmbf_logo
        self.wascal_logo = wascal_logo
        self.hereon_logo = hereon_logo
        self.rcp_image = rcp_image
        self.timeseries_theorie = timeseries_theorie
        self.box_theorie = box_theorie
        self.basic_color = basic_color
        self.sprache = sprache
        self.cs_orange = cs_orange
        self.cs_schwarz = cs_schwarz
        self.title_image = title_image
        self.box_era5 = box_era5
        self.table_cc = table_cc
        self.ts_TG_anomaly = ts_TG_anomaly
        self.ts_TN_anomaly = ts_TN_anomaly
        self.ts_TX_anomaly = ts_TX_anomaly
        self.ts_TR26_anomaly = ts_TR26_anomaly
        self.ts_SU35_anomaly = ts_SU35_anomaly
        self.ts_SU40_anomaly = ts_SU40_anomaly
        self.ts_RRm_anomaly = ts_RRm_anomaly
        self.ts_RR1_anomaly = ts_RR1_anomaly
        self.ts_DD_anomaly = ts_DD_anomaly
        self.ts_R20mm_anomaly = ts_R20mm_anomaly
        self.ts_FG_anomaly = ts_FG_anomaly
        self.hori_SU40_abs = hori_SU40_abs
        self.copev_su40_DD = copev_su40_DD
        self.copev_su40_tr26 = copev_su40_tr26
        self.story = []

        # Header 1: 14pt bold black
        try:
            self.styles["Header14Bold"]
        except KeyError:
            base = self.styles.get("Heading", getSampleStyleSheet()["Heading1"])
            self.styles.add(ParagraphStyle(
                name="Header14Bold",
                parent=base,
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=16,
                alignment=TA_LEFT,
                textColor=colors.black,
                spaceBefore=0,
                spaceAfter=0,
            ))

        # Header 2: 12pt grey
        try:
            self.styles["Header12Grey"]
        except KeyError:
            base = self.styles.get("Heading", getSampleStyleSheet()["Heading1"])
            self.styles.add(ParagraphStyle(
                name="Header12Grey",
                parent=base,
                fontName="Helvetica-Bold",
                fontSize=12,
                leading=14,
                alignment=TA_LEFT,
                textColor=colors.grey,
                spaceBefore=0,
                spaceAfter=0,
            ))


    #----------------------------------------------------------------
    def draw_header(self, text, y_pos, x_pos=None, max_width=None):
        x = self.text_offset_links if x_pos is None else x_pos
        w = (self.width - self.text_offset_links - self.text_offset_rechts) if max_width is None else max_width
        p = Paragraph(text, self.styles["Header14Bold"])
        _, h = p.wrapOn(self.c, w, self.height)
        p.drawOn(self.c, x, y_pos - h)
        return h

    def draw_header2(self, text, y_pos, x_pos=None, max_width=None):
        x = self.text_offset_links if x_pos is None else x_pos
        w = (self.width - self.text_offset_links - self.text_offset_rechts) if max_width is None else max_width
        p = Paragraph(text, self.styles["Header12Grey"])
        _, h = p.wrapOn(self.c, w, self.height)
        p.drawOn(self.c, x, y_pos - h)
        return h

    #----------------------------------------------------------------------
    def savePDF(self):
        """
        Abspeichern als pdf
        """
        self.c.setSubject('Projected climate changes for '+self.region+', based on AFR22-CORDEX simulations')
        self.c.setTitle('Climate Factsheet ' + self.region +', '+ self.version)
        self.c.setAuthor('Climate Service Center Germany (GERICS), 2026')
        self.c.setCreator('Climate Service Center Germany (GERICS), 2026')

        self.c.save()

    def draw_watermark(self, text="DRAFT"):
        """Draw a light grey watermark across the page center."""
        self.c.saveState()
        self.c.setFillColor(colors.Color(0.85, 0.85, 0.85, 1))
        self.c.setFont('Helvetica-Bold', 80)
        # Rotate and position roughly center
        self.c.translate(self.width/2.0, self.height/2.0)
        self.c.rotate(30)
        text_width = stringWidth(text, 'Helvetica-Bold', 80)
        self.c.drawString(-text_width/2.0, 0, text)
        self.c.restoreState()

    def add_footline(self, left_right):
        # Orange header background at top of page
        #self.c.saveState()
        #self.c.setFillColor(self.cs_orange)
        #self.c.setStrokeColor(self.cs_orange)
        #self.c.rect(0, self.height - 1.6 * cm, self.width, 1.6 * cm, stroke=0, fill=1)
        #self.c.restoreState()
        # Light grey footer background (drawn first, behind all footer elements)
        self.c.saveState()
        self.c.setFillColor(colors.Color(0.93, 0.93, 0.93, 1))
        self.c.setStrokeColor(colors.Color(0.93, 0.93, 0.93, 1))
        self.c.rect(0, 0, self.width, 1.6 * cm, stroke=0, fill=1)
        self.c.restoreState()
        logo_gerics = get_image(self.gerics_logo, height =  1.2 * cm)
        logo_wascal = get_image(self.wascal_logo, height =  1.2 * cm)
        logo_breite = logo_gerics.drawWidth + logo_wascal.drawWidth + 0.01  # reduced gap does not work -2
        logo_hoehe = max(logo_gerics.drawHeight, logo_wascal.drawHeight)
        odd_foot = ([[logo_gerics, logo_wascal]])
        even_foot = ([[logo_wascal, logo_gerics]])
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
            createTable(self, even_foot, logo_breite, (logo_hoehe), self.width - self.text_offset_rechts - self.text_offset_links -logo_breite, 0.1* cm, foot_style)
            #createTable(self, even_foot, logo_breite, (logo_hoehe), self.width - self.text_offset_rechts - logo_breite, 0.1* cm, foot_style)
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
            createTable(self, odd_foot, logo_breite, (logo_hoehe), 0.*cm + self.kleiner_abstand,
                          0.1* cm, foot_style)
        else:
            raise Exception(left_right, 'unknown')


    def draw_bottom_rounded_rect(self, x, y, width, height, radius):
        """
        Rechteck mit NUR unten abgerundeten Ecken.
        Box extends a bit more to the left than the text.
        """
        x = x - 25  # Shift box 25 units further left for visual extension
        width = width + 25  # Extend width to compensate for left shift
        p = self.c.beginPath()
        # Start oben rechts
        p.moveTo(x + width, y + height)
        # Obere Kante nach links
        p.lineTo(x, y + height)
        # Linke Seite nach unten bis vor die Rundung
        p.lineTo(x, y + radius)
        # Unten links Rundung (Start 180° -> 270°)
        p.arcTo(x, y, x + 2*radius, y + 2*radius, startAng=180, extent=90)
        # Untere Kante bis vor rechte Rundung
        p.lineTo(x + width - radius, y)
        # Unten rechts Rundung (Start 270° -> 360°)
        p.arcTo(x + width - 2*radius, y, x + width, y + 2*radius, startAng=270, extent=90)
        # Rechte Seite hoch
        p.lineTo(x + width, y + height)
        p.close()
        color = self.cs_orange  # Use cs_orange instead of hardcoded orange
        self.c.setFillColor(color)
        self.c.drawPath(p, fill=1, stroke=0)

    def draw_orange_box_with_text(self, x, y, width, bheight):
        # Draw orange rectangle: revert to original position
        y = self.height - 8.2 * cm
        self.draw_bottom_rounded_rect(self.text_offset_links, y, self.width + 5, bheight, radius=20)
        # Define styles for each line
        style0 = ParagraphStyle('Line0', fontName='Helvetica-Bold', fontSize=24, textColor='white', alignment=TA_LEFT)
        style1 = ParagraphStyle('Line1', fontName='Helvetica-Bold', fontSize=32, textColor='white', alignment=TA_LEFT)
        style2 = ParagraphStyle('Line2', fontName='Helvetica', fontSize=14, textColor='white', alignment=TA_LEFT)
        style3 = ParagraphStyle('Line1b', fontName='Helvetica', fontSize=24, textColor='white', alignment=TA_LEFT)

        # Create paragraphstitle names
        if self.sprache == 'english':   
            line0 = Paragraph(self.region.title(), style0)
            line1 = Paragraph("CLIMATE FACTSHEET", style1)
            line1b = Paragraph(self.sector.upper(), style3)
            line2 = Paragraph("Climate Service Center Germany (GERICS)", style2)
            line3 = Paragraph("WASCAL Competence Centre", style2)
        else:   
            line0 = Paragraph(self.region.title(), style0)
            line1 = Paragraph("FICHE CLIMATIQUE", style1)
            line1b = Paragraph(self.sector.upper(), style3)
            line2 = Paragraph("Climate Service Center Germany (GERICS)", style2)
            line3 = Paragraph("WASCAL Competence Centre", style2)
        #line3 = Paragraph("West African Science Service Centre on Climate Change and Adapted Land Use (WASCAL)", style2)

        # Calculate positions
        line0.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
        line1.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
        line1b.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
        line2.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
        line3.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
        # Raise region and CLIMATE FACTSHEET slightly
        line0.drawOn(self.c, self.text_offset_links, y + bheight - bheight/3 + 0.6*cm)
        line1.drawOn(self.c, self.text_offset_links, y + bheight - ((bheight/3)*2) + 1*cm)
        line1b.drawOn(self.c, self.text_offset_links, y + bheight - ((bheight/3)*2) - 0.5*cm)
        # GERICS below
        line2.drawOn(self.c, self.text_offset_links, y+0.9*cm)
        line3.drawOn(self.c, self.text_offset_links, y + 0.4*cm)
        return


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
        self.schrift_caption = 11
        self.schrift_fliesstext = 12
        self.text_offset_unten = 1.8 * cm

        self.caption_style = ParagraphStyle(
                name='CaptionJustify',
                #parent=styles['Justify'],
                fontName='Helvetica',
                fontSize=self.schrift_caption,
                #leading=self.schrift_caption * 1.2,
                textColor='black',
                alignment=TA_JUSTIFY,
            )
        
        print('Starte mit der Erstellung des Dokuments in make... ')
# ----------- Header der Titelseite
        # Page 1 content → watermark → footline
        title_page = insert_title_page(self)
        #self.draw_watermark("DRAFT")
        foot_1 = self.add_footline('ungerade_odd')
# -------Seitenumbruch auf  Seite 2
        self.c.showPage()
        # Page 2 content → watermark → footline
        Table_page = insert_page_with_table(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even')
# -------Seitenumbruch auf  Seite 3
        self.c.showPage()
        # Page 3 content → watermark → footline
        temperature_page = insert_page_temperature(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd')
# -------Seitenumbruch auf  Seite 4
        self.c.showPage()
        # Page 4 content → watermark → footline
        temperature_page = insert_page2_temperature(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even')
# -------Seitenumbruch auf  Seite 5
        self.c.showPage()
        # Page 5 content → watermark → footline
        temperature_page = insert_page3_temperature(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd')                
# -------Seitenumbruch auf  Seite 6
        self.c.showPage()
        # Page 6 content → watermark → footline
        precipitation_page = insert_page_precipitation(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even')
# -------Seitenumbruch auf  Seite 7
        self.c.showPage()
        # Page 7 content → watermark → footline
        precipitation_page = insert_page2_precipitation(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd')        
# -------Seitenumbruch auf  Seite 8
        self.c.showPage()
        # Page 8 content → watermark → footline
        precipitation_page = insert_page_wind(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even')
# -------Seitenumbruch auf  Seite 
        self.c.showPage()
        # Page 9 content → watermark → footline
        compound_event_page = insert_page_compound_event(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd') 
# -------Seitenumbruch auf  Seite 
        self.c.showPage()
        # Page 10 content → watermark → footline
        compound_event_page = insert_page2_compound_event(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even') 
# -------Seitenumbruch auf  Seite 11
        self.c.showPage()
        # Page 11 List of indices → watermark → footline
        from page_indice_list import return_glossar, insert_glossar_page
        glossar_dict = return_glossar(self.sprache)
        variables=['TG','TN','TX','TR26','SU35','SU40','RRm','DD','RR1', 'R20mm', 'FG','FGmax','SU40_du3_DD_du5','SU40_du3_TR26_du3','HSx3','HSf3','DSf','DSx5']
        #variables = ['TG','TX','TN','SU35','SU40','TR','RRm','R5mm','R10mm']
        insert_glossar_page(self, glossar_dict, variables)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd') 
# -------Seitenumbruch auf  Seite 12
        self.c.showPage()
        # Page 12 list of Simulations and data → watermark → footline
        insert_page_with_models_data(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even') 
# -------Seitenumbruch auf  Seite 13
        self.c.showPage()
        # Page 13 scenario / robustness → watermark → footline
        # folgene funktionen sind aus page scenario_robust.py:
        insert_page_explain(self)
        #insert_page_robustinfo(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd') 
# -------Seitenumbruch auf  Seite 14
        self.c.showPage()
        #a lot of files are missing
        # Page 14 how to read → watermark → footline
        insert_page_reading_instructions(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('gerade_even') 
# -------Impressum-Seite einfügen Seite 15
        self.c.showPage()
        # Page 15 Impressum → watermark → footline
        insert_impressum(self)
        #self.draw_watermark("DRAFT")
        foot_2 = self.add_footline('ungerade_odd')
# -------Impressum-Seite einfügen Seite 16
        self.c.showPage()
        # Page 16 Impressum → watermark → footline
        insert_page_back(self)
        #self.draw_watermark("DRAFT")
        #foot_2 = self.add_footline('gerade_even')
        print('Fertig mit der Erstellung des Dokuments')

