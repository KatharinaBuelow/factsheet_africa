#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
import numpy
from reportlab.lib.units import mm, inch, cm
from reportlab.platypus import Image, Paragraph, Table, Flowable, PageBreak, TableStyle
from reportlab.lib import colors
from reportlab.lib import utils
from skimage import img_as_float, img_as_ubyte, io
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Flowable
from reportlab.lib import colors
from utils_image import get_image
from reportlab.platypus import Table, TableStyle

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
    # Draw orange rectangle: 
    y = self.height - 8.2 * cm
    draw_bottom_rounded_rect(self, self.text_offset_links, y, self.width + 5, bheight, radius=20)
    # Define styles for each line
    style0 = ParagraphStyle('Line0', fontName='Helvetica-Bold', fontSize=20, textColor='white', alignment=TA_LEFT)
    style1 = ParagraphStyle('Line1', fontName='Helvetica-Bold', fontSize=30, textColor='white', alignment=TA_LEFT)
    style2 = ParagraphStyle('Line2', fontName='Helvetica', fontSize=12, textColor='white', alignment=TA_LEFT)

    # Create paragraphs
    line0 = Paragraph(self.region.title(), style0)
    line1 = Paragraph("CLIMATE FACTSHEET", style1)
    line2 = Paragraph("Climate Service Center Germany (GERICS)", style2)

    # Calculate positions
    line0.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line1.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line2.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line0.drawOn(self.c, self.text_offset_links, y+bheight-bheight/3)
    line1.drawOn(self.c, self.text_offset_links, y+bheight-((bheight/3)*2))
    line2.drawOn(self.c, self.text_offset_links, y+0.3*cm)
    return


def insert_title_page(self):
    titleheight_page1 = self.height - 8 * cm
    #  
    #logos at the top:
    #
    einfuegehoehe = self.height - 0.2 * cm    
    map_image = get_image(self.gerics_logo, height = 1.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links , einfuegehoehe - map_image.drawHeight)
    # bmbf
    einfuegehoehe = self.height - 0.2 * cm
    map_image = get_image(self.bmbf_logo, height = 1.9*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +7 *cm, einfuegehoehe - map_image.drawHeight)
    # wascal
    einfuegehoehe = self.height - 0.2 * cm
    map_image = get_image(self.wascal_logo, height = 1.6*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    print('wascal logo, self.height ', self.height)

    map_image.drawOn(self.c, self.text_offset_links +16 *cm, einfuegehoehe - map_image.drawHeight)
        
    # Orange block (title_pic)
    draw_orange_box_with_text(self,100, 600, 250, 6.2*cm)
    
    # Country map
    einfuegehoehe_map = self.height - 7 * cm
    map_image = get_image(self.title_image_burkinafaso, height = 6.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +12.5 *cm, einfuegehoehe_map - map_image.drawHeight)

    if self.sprache == 'english':
        abstract = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>The Regional Climate Factsheet provides brief\
                             and concise information on possible future climate developments for '+self.region+' in the 21st century.\
                             They are based on the results of %s regional climate model simulations, which are\
                             based on the Representative Concentration Pathways (RCPs). RCP8.5 represents a high \
                             emission scenario and RCP2.6 a low emission scenario. YYY different parameters\
                             for climate change are presented, which are relevant for various societal sectors.\
                             They are supplemented by an expert judgement of the reliability of the shown changes. </span>' % (self.anzahl_simulationen),
                             self.styles['Justify'], encoding='utf8')
    else:
        abstract = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>Dieser Klimaausblick informiert über' )
            
    abstract_width, abstract_height = \
        abstract.wrapOn(self.c, self.width - self.text_offset_rechts - self.text_offset_links - 5.2*cm, self.height)
    abstract.drawOn(self.c, self.text_offset_links, titleheight_page1 - self.kleiner_abstand - abstract_height)

    # Zweispaltiger Text nach dem Abstract, ohne Tabelle, über die ganze Seite verteilt

    # Beispieltext für die beiden Spalten
    col1_text = (
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "General introduction to "+self.region+ \
        "content content content content content" \
        "content content content content content" \
        "content content content content content" \
        "General introduction to "+self.region+ " climate. " \
        "General introduction to "+self.region+ " climate. " \
        "General introduction to "+self.region+ " climate. " \
        "General introduction to "+self.region+ " climate. " \
    
        "General introduction to "+self.region+ " climate. "
    )
    col2_text = (
        "What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What kind of Climate Change is already observed? \
        What Climate change is observate with focus on the Sector Agriculture? \
        What Climate change is observate with focus on the Sector Agriculture? \
        What Climate change is observate with focus on the Sector Agriculture? \
        What Climate change is observate with focus on the Sector Agriculture? \
        What Climate change is observate with focus on the Sector Agriculture? "
    )

    # Stil für den Text
    
    style = ParagraphStyle(
    'TwoCol',
    parent=self.styles['Justify'],
    fontName='Helvetica',
    fontSize=10,
    textColor='black'
    )
    # Spaltenbreite berechnen
    total_width = self.width - self.text_offset_links - self.text_offset_rechts - 0.5*cm
    col_width = total_width / 2
    col_height = 6*cm  # Höhe der Spalte (ggf. anpassen)

    # Position unterhalb des Abstracts berechnen
    textbox_y = titleheight_page1 - self.kleiner_abstand - abstract_height - 7.5*cm

    # Paragraphs erzeugen und platzieren
    p1 = Paragraph(col1_text, style)
    p2 = Paragraph(col2_text, style)

    p1.wrapOn(self.c, col_width, col_height)
    p2.wrapOn(self.c, col_width, col_height)

    p1.drawOn(self.c, self.text_offset_links, textbox_y)
    p2.drawOn(self.c, self.text_offset_links + col_width + 1*cm, textbox_y)

# Annual anamolie vor precipitation and Temperature
    einfuegehoehe_balken = self.height - 20* cm
    map_image = get_image(self.box_era5, height = 6.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_balken - map_image.drawHeight)
