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
    title_text = "READING INSTRUCTIONS" if self.sprache == 'english' else "LESEANLEITUNG"
    title_h = self.draw_header(title_text, einfuegehoehe_top)
  
    # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand
    
    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    if self.sprache == 'english':
        intro_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "This page explains how to read the figures used in this factsheet. "
            "The first graphic illustrates the structure of the time-series plot."
            "</span></para>"
        )
    else:
        intro_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "Diese Seite erklärt, wie die Abbildungen in diesem Factsheet gelesen werden. "
            "Die erste Grafik zeigt den Aufbau des Zeitreihendiagramms."
            "</span></para>"
        )
    
    para = Paragraph(intro_text, styles["Justify"])
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    _, para_height = para.wrapOn(self.c, available_width, self.height)
    # Text oben platzieren
    para_top_y = einfuegehoehe_top - para_height
    para.drawOn(self.c, self.text_offset_links, para_top_y)
    
    # Put figure after the text
    einfuegehoehe_table = einfuegehoehe_top - para_height - self.kleiner_abstand
    map_image = get_image(self.timeseries_theorie, height=8.5 * cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_table - map_image.drawHeight)
    
    # Bildunterschrift direkt unter die graphik
    caption_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>1:</b> Unit <br />"
            "<b>2:</b> Legend <br />"
            "<b>3:</b> Reference period 1991-2020 <br />"
            "<b>4 TIMESERIES:</b> The timeseries plot shows the annual values of the climate indicator for Burkina Faso from 1941 to 2023, relative to the 1991–2020 average. <br />"
            "<b>5 BAR CHART:</b> Legend<br />"
            "</span></para>"
        )
    caption = Paragraph(caption_text, styles['Justify'])
    cap_width, cap_height = caption.wrapOn(self.c, available_width, self.height)
    caption_y = (einfuegehoehe_table - map_image.drawHeight) - self.kleiner_abstand
    caption.drawOn(self.c, self.text_offset_links, caption_y - cap_height)

# Distance for next element: 
    #offsettop = offsettop - textbox_y - self.kleiner_abstand
 
    # draw plot left and caption of figure right at the bottom of the page, 
    # Text to figure 1 (ERA5 anomalies)
    col2_text = (
        "<b>Figure 1:</b> Figure 1 shows annual temperature and precipitation anomalies "
        "for "+self.region+" from 1941–2023, relative to the 1991–2020 average. "
        "Temperatures show a clear long-term warming trend, with mostly positive anomalies since the 2000s. "
        "Precipitation varies strongly: early decades were wetter, the 1980s drought is distinct, "
        "and recent years show mixed patterns. Data source: ERA5 global reanalysis (Hersbach et al., 2020)."
    )

    # Annual anomaly for precipitation and Temperature
    
    map_image = get_image(self.box_theorie, height = 5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    # Place image so its bottom aligns with self.text_offset_unten
    img_y = self.text_offset_unten
    map_image.drawOn(self.c, self.text_offset_links, img_y)
    # Place col2_text right beside the box_theorie at the same height as the top of box_theorie
    col2_width = self.width - self.text_offset_links - self.text_offset_rechts - map_image.drawWidth - 1*cm
    col2_x = self.text_offset_links + map_image.drawWidth + 1*cm
    col2_y = img_y + map_image.drawHeight  # Top of box_theorie

    p2 = Paragraph(col2_text, styles['Justify'])
    p2_width, p2_height = p2.wrap(col2_width, self.height)
    p2.drawOn(self.c, col2_x, col2_y - p2_height)

    return