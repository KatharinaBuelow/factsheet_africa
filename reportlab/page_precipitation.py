from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils


def insert_page_precipitation(self):
    """
    Create a page with precipitation graphs
    """
    # Beispielbild und Text
    # Zuerst: Seitentitel und Zusammenfassungstext über der Grafik
    einfuegehoehe_top = self.height - 2 * cm

    # Titel: Precipitation
    title_text = "PRECIPITATION" if self.sprache == 'english' else "NIEDERSCHLAG"
    title_h = self.draw_header(title_text, einfuegehoehe_top)

     # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    summary_text = (
        "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
        "The graphs show the projected evolution of mean annual precipitation and mean number of dry days (daily precipitation amount <1mm/day) \
        for "+self.region+" from 1971 to 2098, based on CORDEX AFR22\
         regional climate model realizations under two emission scenarios: RCP2.6 (blue) and RCP8.5 (red). The solid lines represent \
         the median of the model ensemble for each scenario, while the shaded areas indicate the range between the minimum and maximum \
         values across all models. The historical reference period (1991–2020) is highlighte.  The projections reveal no clear trend.\
          The shaded ranges illustrate the large uncertainty among models, with wider bands indicating greater \
         variability in projections."
        "</span></para>"
    )

    para = Paragraph(summary_text, styles["Justify"]) 
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    para_width, para_height = para.wrapOn(self.c, available_width, self.height)
    # Text oben platzieren
    para_top_y = einfuegehoehe_top - para_height
    para.drawOn(self.c, self.text_offset_links, para_top_y)

    # Danach: Elemente gleichmäßig verteilen: zwei Grafiken + zwei Captions im verbleibenden Bereich
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    bottom_margin = 2 * cm
    start_y = para_top_y - self.kleiner_abstand

    # Caption-Texte vorab definieren und Höhen bestimmen
    caption_text = (
        "<b>Figure 8:</b> Projected evolution of mean annual precipitation [mm/day] for " + self.region + " from 1971 to 2098 based on CORDEX AFR22 \
        regional climate model realizations under RCP2.6 (blue) and RCP8.5 (red) scenarios. Solid lines represent the ensemble median, \
        while shaded areas indicate the range between minimum and maximum values across all models, illustrating uncertainty. "
    )

    caption = Paragraph(caption_text, self.caption_style)
    _, cap_height = caption.wrapOn(self.c, available_width, self.height)
        

    # Zweite Grafik: ts_DD_anomaly (Tage > 40°C) darunter platzieren und skalieren
    caption_text2 = (
        "<b>Figure 9:</b> Projected evolution of mean annual number of dry days (daily precipitation amount < 1 mm) for " + self.region + " \
        from 1971 to 2098 based on CORDEX AFR22 \
        regional climate model realizations under RCP2.6 (blue) and RCP8.5 (red) scenarios. Solid lines represent the ensemble median, \
        while shaded areas indicate the range between minimum and maximum values across all models, illustrating uncertainty."
    )
    caption2 = Paragraph(caption_text2, self.caption_style)
    _, cap_height2 = caption2.wrapOn(self.c, available_width, self.height)
    

    # Verfügbarer Platz: gleichmäßig verteilen
    gaps_between_blocks = 3  # gap after summary, between caption1 and image2, and before final bottom margin
    gap_size = self.kleiner_abstand
    available_height_total = start_y - bottom_margin - (gap_size * gaps_between_blocks) - cap_height - cap_height2
    image_height_each_max = max(1 * cm, available_height_total / 2.0)

    # Seitenverhältnisse prüfen und Höhe ggf. durch Breite begrenzen
    img_reader1 = utils.ImageReader(self.ts_RRm_anomaly)
    iw1, ih1 = img_reader1.getSize()
    aspect1 = ih1 / float(iw1)
    target_height1 = min(16.5 * cm, image_height_each_max, available_width * aspect1)

    img_reader2 = utils.ImageReader(self.ts_DD_anomaly)
    iw2, ih2 = img_reader2.getSize()
    aspect2 = ih2 / float(iw2)
    target_height2 = min(16.5 * cm, image_height_each_max, available_width * aspect2)

    # Beide Bilder sollen gleich groß sein: nimm das kleinere der beiden Zielhöhen
    equal_height = min(target_height1, target_height2)

    # Erstes Bild zeichnen
    map_image = get_image(self.ts_RRm_anomaly, height=equal_height)
    map_image.wrapOn(self.c, self.width, self.height)
    img1_y = start_y - map_image.drawHeight
    map_image.drawOn(self.c, self.text_offset_links, img1_y)
    # Caption 1 direkt darunter
    caption_y = img1_y - gap_size
    caption.drawOn(self.c, self.text_offset_links, caption_y - cap_height)

    # Zweites Bild zeichnen, unter Caption 1
    second_start_y = caption_y - cap_height - gap_size
    map_image2 = get_image(self.ts_DD_anomaly, height=equal_height)
    map_image2.wrapOn(self.c, self.width, self.height)
    img2_y = second_start_y - map_image2.drawHeight
    map_image2.drawOn(self.c, self.text_offset_links, img2_y)
    # Caption 2 darunter
    caption2_y = img2_y - gap_size
    caption2.drawOn(self.c, self.text_offset_links, caption2_y - cap_height2)