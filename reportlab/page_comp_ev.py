from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils


def insert_page_compound_event(self):
    """
    Create a page with compound events
    """
    # Beispielbild und Text
    # Zuerst: Seitentitel und Zusammenfassungstext über der Grafik
    einfuegehoehe_top = self.height - 2 * cm
    print("creation page for compound events : " + self.region)
    # Titel: 
    title_text = "COMPOUND EXTREME EVENTS" if self.sprache == 'english' else "KOMBINIERTE EXTREME EREIGNISSE"
    title_h = self.draw_header(title_text, einfuegehoehe_top)
    # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    region_norm = self.region.strip().lower()
    print(f"[compound] region='{self.region}' normalized='{region_norm}'")
    if region_norm in ("ivory coast", "côte d'ivoire"):
        print("[compound] Using Ivory Coast summary text")
        summary_text = (
        "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
        "Projected concurrent occurrence of heatwaves (Tmax > 40 °C) and tropical nights (minimum temperature > 26°C) lasting\
         at leat 3 days in West Africa. The figure shows the ensemble median for \
        different time periods (1991–2020, 2031–2060, 2069–2098) under two emission scenarios (RCP2.6 and RCP8.5). \
        The color scale indicates the expected number of such events per year. Results reveal a strong upward trend \
        over time, particularly under RCP8.5, where events become extremely frequent by the end of the century, \
        exceeding 150 per year in some regions. In contrast, RCP2.6 shows a much smaller increase, emphasizing \
        the critical role of emission reductions in limiting extreme climate impacts.This combination of extreme heat, \
        both day and night, poses significant health risks and strains resources in these vulnerable areas. ​"
        "</span></para>"
        )
    else:
        summary_text = (
        "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
        "Concurrent occurrence of heat days (Tmax > 40 °C) lasting at least 3 consecutive days "
        "and dry periods (RR < 1 mm day⁻¹) lasting at least 7 consecutive days in West Africa. "
        "The figure shows the annual mean number of such events derived from ERA5 for the reference "
        "period 1991-2020 (grey shading) and the ensemble median change relative to 1991-2020 "
        "for two future periods (2031-2060 and 2069-2098) under the RCP2.6 and RCP8.5 emission scenarios. "
        "The colour scale indicates the projected change in the annual frequency of these events. "
        "Results reveal a strong increase over time, particularly under RCP8.5, "
        "where the annual frequency rises substantially by the end of the century, "
        "with increases exceeding 100 events per year in some regions. "
        "In contrast, RCP2.6 shows a much smaller increase, highlighting the critical importance "
        "of emission reductions in limiting extreme climate impacts."
        "</span></para>"
    )    
    para = Paragraph(summary_text, styles["Justify"]) 
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    para_width, para_height = para.wrapOn(self.c, available_width, self.height)
    # Text oben platzieren
    para_top_y = einfuegehoehe_top - para_height
    para.drawOn(self.c, self.text_offset_links, para_top_y)

    # Danach: Elemente gleichmäßig verteilen: eine Grafik + eine Caption im verbleibenden Bereich
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    bottom_margin = 2 * cm
    start_y = para_top_y - self.kleiner_abstand

    # Caption-Texte vorab definieren und Höhen bestimmen
    if region_norm in ("ivory coast", "côte d'ivoire"):
        print("[compound] Using Ivory Coast caption")
        caption_text = (
            "<b>Figure 13:</b> Projected concurrent occurrence of heatwaves (Tmax > 40 °C) and tropical nights (Minimum Temperature > 26°C)\
             in "+self.region+" lasting at least 3 days. The figure shows the annual mean number of such events derived from ERA5 for the reference "
            "period 1991-2020 (grey shading) and the ensemble median change relative to 1991-2020 "
            "for two future periods (2031-2060 and 2069-2098) under the RCP2.6 and RCP8.5 emission scenarios. "
            "The colour scale indicates the expected number of such events per year. "
            "The non-hatched regions indicate robust projected changes, whereas hatched regions indicate areas where projected changes are not robust."
        )
    else:
        caption_text = (
            "<b>Figure 13:</b> Projected concurrent occurrence of heat days (Tmax > 40 °C) and dry days (RR < 1 mm/day)\
            in West Africa lasting at least 3 and 7 days. The figure shows the annual mean number of such events derived from ERA5 for the reference "
            "period 1991-2020 (grey shading) and the ensemble median change relative to 1991-2020 "
            "for two future periods (2031-2060 and 2069-2098) under the RCP2.6 and RCP8.5 emission scenarios. "
            "The colour scale indicates the expected number of such events per year. "
            "The non-hatched regions indicate robust projected changes, whereas hatched regions indicate areas where projected changes are not robust."
        )
  
    caption = Paragraph(caption_text, self.caption_style)
    _, cap_height = caption.wrapOn(self.c, available_width, self.height)
    

    # Verfügbarer Platz: für eine Grafik + eine Caption
    gap_size = self.kleiner_abstand
    available_height_total = start_y - bottom_margin - gap_size - cap_height
    image_height_each_max = max(1 * cm, available_height_total)

    # Seitenverhältnisse prüfen und Höhe ggf. durch Breite begrenzen
    if region_norm in ("ivory coast", "côte d'ivoire"):
        print("[compound] Selecting image copev_su40_tr26 for Ivory Coast")
        img_reader1 = utils.ImageReader(self.copev_su40_tr26)
    else:
        print("[compound] Selecting image copev_su40_DD for other regions")
        img_reader1 = utils.ImageReader(self.copev_su40_DD)  
      
    iw1, ih1 = img_reader1.getSize()
    aspect1 = ih1 / float(iw1)
    target_height1 = min(16.5 * cm, image_height_each_max, available_width * aspect1)

    # Zielhöhe für die einzelne Grafik
    equal_height = target_height1

    # Erstes Bild zeichnen
    if region_norm in ("ivory coast", "côte d'ivoire"):
        map_image = get_image(self.copev_su40_tr26, height=equal_height)
        print("Using copev_su40_tr26 image for Ivory Coast")
    else:
        map_image = get_image(self.copev_su40_DD, height=equal_height)
        print("Using copev_su40_DD image for other regions")
    map_image.wrapOn(self.c, self.width, self.height)
    img1_y = start_y - map_image.drawHeight
    map_image.drawOn(self.c, self.text_offset_links, img1_y)
    # Caption 1 direkt darunter
    caption_y = img1_y - gap_size
    caption.drawOn(self.c, self.text_offset_links, caption_y - cap_height)
