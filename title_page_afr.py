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

def draw_orange_box_with_text(self, x, y, width, bheight):
    # Draw orange rectangle: change to white
    self.c.setFillColorRGB(1, 0.5, 0)  # Orange
    y = self.height - 8.5 * cm
    self.c.rect(self.text_offset_links, y, self.width - self.text_offset_links - self.text_offset_rechts, bheight, fill=1, stroke=0)

    # Define styles for each line
    style0 = ParagraphStyle('Line0', fontName='Helvetica-Bold', fontSize=20, textColor='white', alignment=TA_LEFT)
    style1 = ParagraphStyle('Line1', fontName='Helvetica-Bold', fontSize=30, textColor='white', alignment=TA_LEFT)
    style2 = ParagraphStyle('Line2', fontName='Helvetica', fontSize=12, textColor='grey', alignment=TA_LEFT)

    # Create paragraphs
    line0 = Paragraph(self.region.title(), style0)
    line1 = Paragraph("CLIMATE FACTSHEET", style1)
    line2 = Paragraph('Climate Service Center Germany (GERICS)', style2)


    # Calculate positions
    line0.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line1.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line2.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line0.drawOn(self.c, self.text_offset_links, y+bheight-bheight/3)
    line1.drawOn(self.c, self.text_offset_links, y+bheight-((bheight/3)*2))
    line2.drawOn(self.c, self.text_offset_links, y+0.3*cm)
    return

def draw_stripes_box_with_text(self, x, y, width, bheight, climate_stripes_image=None):
    # Draw climate stripes image instead of orange box
    climate_stripes = get_image(climate_stripes_image, height=bheight)
    #text
    einfuegehoehe = self.height - 8.5 * cm
    #stripes
    einfuegehoehestripes = self.height - 1.5 * cm
    climate_stripes.wrapOn(self.c, self.width, self.height)
    climate_stripes.drawOn(self.c, self.text_offset_links, einfuegehoehestripes - climate_stripes.drawHeight)

    # Draw semi-transparent white rectangle over stripes for text readability
    self.c.saveState()
    self.c.setFillColorRGB(1, 1, 1,alpha=0.7)
    self.c.rect(self.text_offset_links, einfuegehoehe, self.width - self.text_offset_links - self.text_offset_rechts, bheight, fill=1, stroke=0)
    self.c.restoreState()

    # Define styles for each line
    style0 = ParagraphStyle('Line0', fontName='Helvetica-Bold', fontSize=20, textColor='grey', alignment=TA_LEFT)
    style1 = ParagraphStyle('Line1', fontName='Helvetica-Bold', fontSize=30, textColor='grey', alignment=TA_LEFT)
    style2 = ParagraphStyle('Line2', fontName='Helvetica', fontSize=12, textColor='grey', alignment=TA_LEFT)

    # Create paragraphs
    line0 = Paragraph(self.region.title(), style0)
    line1 = Paragraph("CLIMATE FACTSHEET", style1)
    line2 = Paragraph('Climate Service Center Germany (GERICS)', style2)

    # Calculate positions
    line0.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, bheight)
    line1.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, bheight)
    line2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, bheight)
    line0.drawOn(self.c, self.text_offset_links, einfuegehoehe + bheight - bheight / 2)
    line1.drawOn(self.c, self.text_offset_links, einfuegehoehe + bheight - ((bheight / 4) * 3))
    line2.drawOn(self.c, self.text_offset_links, einfuegehoehe + 0.3 * cm)
    return

def draw_climate_stripes_with_text(self, x, y, width, bheight, climate_stripes_image=None):
    ''' on the title page, draw the climate stripes image with text box above'''
    climate_stripes = get_image(climate_stripes_image, height = 8.5*cm)
    climate_stripes.wrapOn(self.c, self.width, self.height)
    climate_stripes.drawOn(self.c, self.text_offset_links +12 *cm, einfuegehoehe - climate_stripes.drawHeight)

    # Draw white rectangle
    self.c.setFillColorRGB(1, 1, 1)  # White
    y = self.height - 8.5 * cm
    self.c.rect(self.text_offset_links, y, self.width - self.text_offset_links - self.text_offset_rechts, bheight, fill=1, stroke=0)

    # Define styles for each line
    style0 = ParagraphStyle('Line0', fontName='Helvetica-Bold', fontSize=20, textColor='white', alignment=TA_LEFT)
    style1 = ParagraphStyle('Line1', fontName='Helvetica-Bold', fontSize=30, textColor='white', alignment=TA_LEFT)
    style2 = ParagraphStyle('Line2', fontName='Helvetica', fontSize=12, textColor='grey', alignment=TA_LEFT)

    # Create paragraphs
    line0 = Paragraph(self.region.title(), style0)
    line1 = Paragraph("CLIMATE FACTSHEET", style1)
    line2 = Paragraph('Climate Service Center Germany (GERICS)', style2)

    # Calculate positions
    line0.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line1.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line2.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line0.drawOn(self.c, self.text_offset_links, y+bheight-bheight/3)
    line1.drawOn(self.c, self.text_offset_links, y+bheight-((bheight/3)*2))
    line2.drawOn(self.c, self.text_offset_links, y+0.3*cm)
    return

def get_image(path, height=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, height=height, width = (height/ aspect))

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

    map_image.drawOn(self.c, self.text_offset_links +15 *cm, einfuegehoehe - map_image.drawHeight)
        
    # Orange block (title_pic)
    draw_orange_box_with_text(self,100, 600, 250, 5.5*cm)
    
    # Climate stripes-Bild
    #draw_stripes_box_with_text(self,100, 600, 250, 7.5*cm, climate_stripes_image=self.climate_stripes_image)

    # Country map
    einfuegehoehe = self.height - 6.5 * cm
    print('einfuegehoehe ', einfuegehoehe)
    print('self.height ', self.height)
    map_image = get_image(self.title_image_burkinafaso, height = 6.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +12 *cm, einfuegehoehe - map_image.drawHeight)

    
    if self.sprache == 'english':
        abstract = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>The Regional Climate Factsheet provides brief\
                             and concise information on possible future climate developments for '+self.region+' in the 21st century.\
                             They are based on the results of %s regional climate model simulations, which are\
                             based on the Representative Concentration Pathways (RCPs). RCP8.5 represents a high emission scenario and RCP2.6 a low emission scenario. YYY different parameters\
                             for climate change are presented, which are relevant for various societal sectors.\
                             They are supplemented by an expert judgement of the reliability of the shown changes. </span>' % (self.anzahl_simulationen),
                             self.styles['Justify'], encoding='utf8')
    else:
        abstract = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>Dieser Klimaausblick informiert über' )
            
    abstract_width, abstract_height = \
        abstract.wrapOn(self.c, self.width - self.text_offset_rechts - self.text_offset_links - 5.5*cm, self.height)
    abstract.drawOn(self.c, self.text_offset_links, titleheight_page1 - self.kleiner_abstand - abstract_height)

