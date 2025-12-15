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
    # Draw orange rectangle: revert to original position
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
    line3 = Paragraph("WASCAL Competence Centre", style2)
    #line3 = Paragraph("West African Science Service Centre on Climate Change and Adapted Land Use (WASCAL)", style2)

    # Calculate positions
    line0.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line1.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line2.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    line3.wrapOn(self.c, self.width - self.text_offset_links -self.text_offset_rechts, bheight)
    # Raise region and CLIMATE FACTSHEET slightly
    line0.drawOn(self.c, self.text_offset_links, y + bheight - bheight/3 + 0.6*cm)
    line1.drawOn(self.c, self.text_offset_links, y + bheight - ((bheight/3)*2) + 0.5*cm)
    # Place line3 directly under CLIMATE FACTSHEET
    
    # GERICS below
    line2.drawOn(self.c, self.text_offset_links, y+0.9*cm)
    line3.drawOn(self.c, self.text_offset_links, y + 0.4*cm)
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
    map_image = get_image(self.title_image, height = 6.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +12.5 *cm, einfuegehoehe_map - map_image.drawHeight)

    if self.sprache == 'english':
        abstract = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>The Regional Climate Factsheet \
                            provides brief\
                             and concise information on possible future climate developments for '+self.region+' in the 21st century.\
                             They are based on the results of %s regional climate model simulations, which are\
                             based on the Representative Concentration Pathways (RCPs). RCP8.5 represents a high \
                             emission scenario and RCP2.6 a low emission scenario. 12 different parameters\
                             for climate change are presented, which are relevant for various societal sectors.\
                             Climate change information is complemented by the occurrence of specific, co-occurring extreme events.\
                             They are supplemented by an expert judgement of the reliability of the shown changes. </span>' % (self.anzahl_simulationen),
                             self.styles['Justify'], encoding='utf8')
    else:
        abstract = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>Dieser Klimaausblick informiert über' )
            
    abstract_width, abstract_height = \
        abstract.wrapOn(self.c, self.width - self.text_offset_rechts - self.text_offset_links - 5.2*cm, self.height)
    abstract.drawOn(self.c, self.text_offset_links, titleheight_page1 - self.kleiner_abstand - abstract_height)

    # Zweispaltiger Text nach dem Abstract, ohne Tabelle, über die ganze Seite verteilt
    print('titelseite:', self.region)
    # Beispieltext für die beiden Spalten
    if self.region == "Burkina Faso":
        col1_text = (
        self.region +" is located in West Africa and is influenced by the dynamics of the West \
        African Monsoon system. This system drives seasonal rainfall, with precipitation levels generally increasing \
        from the arid Sahelian north to the humid coastal south. "+self.region+" is located inland and has a semi-arid \
        to tropical climate, characterized by a long dry season and a short rainy season from June to September. \
        In recent decades, "+self.region+" has faced increasing climate variability and extreme weather events, \
        such as prolonged droughts in (notably during the 1970s and 1980s). These trends are consistent with broader regional patterns linked to climate change."
    )
    elif self.region == "Togo":
        col1_text = (
        self.region +" is located in West Africa and is influenced by the dynamics of the West \
        African Monsoon system. This system drives seasonal rainfall, with precipitation levels generally increasing \
        from the arid Sahelian north to the humid coastal south."+self.region+" experiences humid, tropical climates, \
        especially in their southern \
        regions, with two rainy seasons (typically from March to July and September to November).\
        The southern coastal areas receive high annual rainfall, while the northern parts are drier.\
        In recent decades, "+self.region+" has faced increasing climate variability and extreme weather events, \
        with urban and rural flooding." 
    )
        #kein platz mehr
        #These trends are consistent with broader regional patterns linked to climate change."
    
    elif self.region == "Ivory Coast":
        col1_text = (
        self.region +" is located in West Africa and is influenced by the dynamics of the West \
        African Monsoon system. This system drives seasonal rainfall, with precipitation levels generally increasing \
        from the arid Sahelian north to the humid coastal south."+self.region+" experiences humid, tropical climates, \
        especially in their southern \
        regions, with two rainy seasons (typically from March to July and September to November).\
        The southern coastal areas receive high annual rainfall, while the northern parts are drier.\
        In recent decades, "+self.region+" has faced increasing climate variability and extreme weather events, \
        with urban and rural flooding."
        #These trends are consistent with broader regional patterns linked to climate change."
    )
    else:
        col1_text = (
        self.region +" is located in Africa."
    )
    
    col2_text = (
            "<b>Figure 1:</b> The figure shows annual temperature and precipitation anomalies for "+self.region+" from 1941 to 2023, based on ERA5 reanalysis data. The anomalies are calculated relative to the 1991–2020 reference period, which is indicated by the vertical dashed lines."\
        "In the upper panel, temperature anomalies (in °C) reveal a clear long-term warming trend. Most years before the 1980s were cooler than the reference period, with anomalies often below –1 °C, especially during the 1950s and 1960s. Starting in the late 1980s, anomalies approach zero, and from the 2000s onward, nearly all years are warmer than the 1991–2020 average. \
        The most recent decade shows persistent positive anomalies, exceeding +1 °C in several years, highlighting significant warming compared to the reference period."\
        "The lower panel displays precipitation anomalies (in %). Early decades, particularly the 1940s and 1950s, were generally wetter than the reference period, with anomalies reaching +40 % or more. From the 1970s onward, negative anomalies become more frequent, indicating drier conditions relative to 1991–2020. The Sahel drought period in the 1980s is evident, with anomalies below –20%. Recent years show mixed variability, but overall, precipitation tends to show high annual variability."\
        "This visualization underscores that the 1991–2020 reference period itself is already warmer than earlier decades, meaning current anomalies represent additional warming beyond an already elevated baseline."\
        "Data source: ERA5 global reanalysis (Hersbach et al., 2020). "
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
    col_height = 20*cm

    # Position unterhalb des Abstracts berechnen
    textbox_y = titleheight_page1 - self.kleiner_abstand - abstract_height - 6.0*cm

    # Paragraphs erzeugen und platzieren
    p1 = Paragraph(col1_text, style)
    p2 = Paragraph(col2_text, style)

    p1.wrapOn(self.c, col_width, col_height)
    p2_width, p2_height = p2.wrapOn(self.c, col_width, col_height)

    # Draw first column under abstract as before
    p1.drawOn(self.c, self.text_offset_links, textbox_y)

    # Draw second column bottom-aligned with the col1 graphic baseline
    # The graphic (box_era5) is placed at y = (self.height - 20*cm) - drawHeight
    # with a requested height of 8*cm, so align p2's bottom to that baseline.
    box_target_top = self.height - 20*cm
    box_height = 8*cm
    graphic_baseline_y = box_target_top - box_height
    p2_y = max(graphic_baseline_y, (self.kleiner_abstand if hasattr(self, 'kleiner_abstand') else 0.8*cm))
    p2.drawOn(self.c, self.text_offset_links + col_width + 1*cm, p2_y)

# Annual anamolie vor precipitation and Temperature
    einfuegehoehe_balken = self.height - 18.5* cm  # add small gap below col1_text by lowering figure slightly
    map_image = get_image(self.box_era5, height = 8*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_balken - map_image.drawHeight)

    # Caption below Figure 1 (ERA5 anomalies), aligned to col1_text width
    caption_style = ParagraphStyle(
        'FigCaption',
        parent=self.styles['Justify'],
        fontName='Helvetica',
        fontSize=8,
        textColor='black'
    )
    caption_text = (
        "<b>Figure 1:</b> Annual mean anomalies of observed temperature and precipitation for "
        + self.region +
        " from 1950 to 2023, relative to the 1991–2020 average."
    )
    caption = Paragraph(caption_text, caption_style)
    cap_w, cap_h = caption.wrapOn(self.c, col_width, self.height)
    graphic_baseline_y = einfuegehoehe_balken - map_image.drawHeight
    caption.drawOn(self.c, self.text_offset_links, graphic_baseline_y - cap_h - 0.2*cm)
