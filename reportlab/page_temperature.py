from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils


def insert_page_temperature(self):
    """
    Create a page with a table
    """
    # Beispielbild und Text
    # Zuerst: Seitentitel und Zusammenfassungstext über der Grafik
    einfuegehoehe_top = self.height - 2 * cm

    # Titel: Temperature
    title_text = "Temperature" if self.sprache == 'english' else "Temperatur"
    title_para = Paragraph(f"<para><span name=Helvetica-Bold size=12>{title_text}</span></para>", self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    title_w, title_h = title_para.wrapOn(
        self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    title_para.drawOn(self.c, self.text_offset_links, einfuegehoehe_top - title_h)
    # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    summary_text = (
        "<para><span name=Helvetica size=10>"
        "The graphs show the projected evolution of mean annual temperature and mean number of heat days (Maximum temperature > 40°C) \
        for "+self.region+" from 1971 to 2098, based on CORDEX AFR22\
         regional climate model realizations under two emission scenarios: RCP2.6 (blue) and RCP8.5 (red). The solid lines represent \
         the median of the model ensemble for each scenario, while the shaded areas indicate the range between the minimum and maximum \
         values across all models. The historical reference period (1991–2020) is highlighted. The projections reveal a clear warming trend, with RCP8.5 showing a \
         strong increase toward the end of the century, while RCP2.6 stabilizes at a lower \
         level after mid-century. The shaded ranges illustrate the uncertainty among models, with wider bands indicating greater \
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
        "<para><span name=Helvetica size=9>"
        "<b>Figure 2:</b> Projected evolution of mean annual temperature for " + self.region + " from 1971 to 2098 based on CORDEX AFR22 \
        regional climate model realizations under RCP2.6 (blue) and RCP8.5 (red) scenarios. Solid lines represent the ensemble median, \
        while shaded areas indicate the range between minimum and maximum values across all models, illustrating uncertainty. "
        "</span></para>"
    )
    caption = Paragraph(caption_text, styles['Justify'])
    _, cap_height = caption.wrapOn(self.c, available_width, self.height)

    # Zweite Grafik: ts_SU40_anomaly (Tage tmax> 40°C) darunter platzieren und skalieren
    caption_text2 = (
        "<para><span name=Helvetica size=9>"
        "<b>Figure 3:</b> Projected evolution of mean annual number of heatdays (maximum temperature >40 °C) for " + self.region + " \
        from 1971 to 2098 based on CORDEX AFR22 \
        regional climate model realizations under RCP2.6 (blue) and RCP8.5 (red) scenarios. Solid lines represent the ensemble median, \
        while shaded areas indicate the range between minimum and maximum values across all models, illustrating uncertainty."
        "</span></para>"
    )
    caption2 = Paragraph(caption_text2, styles['Justify'])
    _, cap_height2 = caption2.wrapOn(self.c, available_width, self.height)

    # Verfügbarer Platz: gleichmäßig verteilen
    gaps_between_blocks = 3  # gap after summary, between caption1 and image2, and before final bottom margin
    gap_size = self.kleiner_abstand
    available_height_total = start_y - bottom_margin - (gap_size * gaps_between_blocks) - cap_height - cap_height2
    image_height_each_max = max(1 * cm, available_height_total / 2.0)

    # Seitenverhältnisse prüfen und Höhe ggf. durch Breite begrenzen
    img_reader1 = utils.ImageReader(self.ts_TG_anomaly)
    iw1, ih1 = img_reader1.getSize()
    aspect1 = ih1 / float(iw1)
    target_height1 = min(16.5 * cm, image_height_each_max, available_width * aspect1)

    img_reader2 = utils.ImageReader(self.ts_su40_anomaly)
    iw2, ih2 = img_reader2.getSize()
    aspect2 = ih2 / float(iw2)
    target_height2 = min(16.5 * cm, image_height_each_max, available_width * aspect2)

    # Beide Bilder sollen gleich groß sein: nimm das kleinere der beiden Zielhöhen
    equal_height = min(target_height1, target_height2)

    # Erstes Bild zeichnen
    map_image = get_image(self.ts_TG_anomaly, height=equal_height)
    map_image.wrapOn(self.c, self.width, self.height)
    img1_y = start_y - map_image.drawHeight
    map_image.drawOn(self.c, self.text_offset_links, img1_y)
    # Caption 1 direkt darunter
    caption_y = img1_y - gap_size
    caption.drawOn(self.c, self.text_offset_links, caption_y - cap_height)

    # Zweites Bild zeichnen, unter Caption 1
    second_start_y = caption_y - cap_height - gap_size
    map_image2 = get_image(self.ts_su40_anomaly, height=equal_height)
    map_image2.wrapOn(self.c, self.width, self.height)
    img2_y = second_start_y - map_image2.drawHeight
    map_image2.drawOn(self.c, self.text_offset_links, img2_y)
    # Caption 2 darunter
    caption2_y = img2_y - gap_size
    caption2.drawOn(self.c, self.text_offset_links, caption2_y - cap_height2)