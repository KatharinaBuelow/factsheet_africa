from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils
import os


def insert_page_reading_instructions(self):

    """
    Create a page with reading instructions
    """
    #------------------ Seitenumbruch auf Impressum Seite
    einfuegehoehe_top = self.height - 2*cm

    #--------------------------
    # Titel: 
    #-------------------------
    title_text = "READING INSTRUCTIONS" if self.sprache == 'english' else "FRENCH"
    title_h = self.draw_header(title_text, einfuegehoehe_top)
  
    # Spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand
    
    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    if self.sprache == 'english':
        intro_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "This page explains how to read the timeseries and bar chart figures used in this factsheet."
            "</span></para>"
        )
    else:
        intro_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "FRENCH."
            "</span></para>"
        )
    
    para = Paragraph(intro_text, styles["Justify"])
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    _, para_height = para.wrapOn(self.c, available_width, self.height)

    # Place text at the top of the page, below the title
    einfuegehoehe = einfuegehoehe_top - para_height
    para.drawOn(self.c, self.text_offset_links, einfuegehoehe)
    
    # Put figure after the text
    einfuegehoehe = einfuegehoehe - para_height 
    map_image = get_image(self.timeseries_theorie, height=8.5 * cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe - map_image.drawHeight)
    einfuegehoehe = einfuegehoehe - map_image.drawHeight 
    
    # Caption directly below the figure
    if self.sprache == 'english':
        caption_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>1:</b> Magnitude and unit of the simulated change in the respective climate variable.<br /><br />"
            "<b>2:</b> Legend for the time series plot: colors indicate the underlying emission "
            "scenarios (RCP2.6: blue; RCP8.5: red). The dark line represents the ensemble median, "
            "while the shaded area denotes the full range of the climate projections used. <br /><br />"
            "<b>3:</b> The reference period 1991-2020 is shown as a grey shaded area. "
            "Anomalies are expressed relative to the 30-year climatological mean of this "
            "period, with each annual value "
            "representing its deviation from the 1991-2020 average. <br /><br />"
            "<b>4 TIME SERIES:</b> The time series from 1971 to 2098 depicts annual anomalies "
            "of the climate indicator relative to the 30-year mean of the reference period 1991-2020. "
            "The ensemble median is shown by the dark line, "
            "while individual climate projections are displayed as thin lines in the background. "
            "The shaded envelope represents the full range of projected values and highlights the uncertainty "
            "across the ensemble. <br /><br />"
            "</span></para>"
        )
    else:
        caption_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "FRENCH."
            "</span></para>"
        )
    caption = Paragraph(caption_text, styles['Justify'])
    cap_width, cap_height = caption.wrapOn(self.c, available_width, self.height)
    einfuegehoehe = (einfuegehoehe - cap_height) #- self.kleiner_abstand * 0.5
    caption.drawOn(self.c, self.text_offset_links, einfuegehoehe)

    if self.sprache == 'english':   
        col2_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>5 BAR CHART:</b> The bar chart illustrates the range of simulated changes "
            "for two 30-year periods relative to the reference period 1991-2020: 2031-2060, "
            "representing the period \"mid-21st century\", and 2069-2098, "
            "representing the period \"end of the 21st century\". The bars summarize characteristic "
            "statistics of the ensemble of available climate model projections: Maximum, 85th percentile, Median, 15th percentile, Minimum. "
            "The full range of simulation results is bounded by the minimum and maximum values. "
            "The median represents the projection located at the center of the ensemble distribution. "
            "Additionally, the 15th and 85th percentiles indicate the values below "
            "which 15% and 85% of the simulations fall, respectively. <br /><br />"
            "<b>6:</b> Legend for the bar chart: colors indicate the underlying emission "
            "scenarios (RCP2.6: blue; RCP8.5: red). The grey line represents the ensemble median, "
            "while the dark shaded area denotes the range between the 15th and 85th percentiles. "
            "The lighter shaded area indicates the full range of the climate projections used. <br />"
            "</span></para>"
        )
    else:
        col2_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "FRENCH."
            "</span></para>"
        )   
    map_image = get_image(self.box_theorie, height = 5*cm)
    map_image.wrapOn(self.c, self.width, self.height)

    # Figure and text are placed in two columns, 
    # with the figure on the left and the text on the right
    # they are allined at their middle, so that the figure and text are centered vertically
    
    top_y = einfuegehoehe - self.kleiner_abstand *3
    image_y = top_y - map_image.drawHeight
    map_image.drawOn(self.c, self.text_offset_links, image_y)
    # Place col2_text right beside the box_theorie and align vertical center
    col2_width = self.width - self.text_offset_links - self.text_offset_rechts - map_image.drawWidth - 1*cm
    col2_x = self.text_offset_links + map_image.drawWidth + 1*cm

    p2 = Paragraph(col2_text, styles['Justify'])
    p2_width, p2_height = p2.wrap(col2_width, self.height)
    image_center_y = image_y + (map_image.drawHeight / 2.0)
    p2_y = image_center_y - (p2_height / 2.0)
    p2.drawOn(self.c, col2_x, p2_y)

    return