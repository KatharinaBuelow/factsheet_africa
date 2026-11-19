from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils


def insert_page3_temperature(self):
    """
    Create a page with temperature and heatdays projections for the specified region.
    """
    # Beispielbild und Text
    # Zuerst: Seitentitel und Zusammenfassungstext über der Grafik
    einfuegehoehe_top = self.height - 2 * cm

    # Titel: Temperature (shared Header1 style)
    title_text = "TEMPERATURE" if self.sprache == 'english' else "TEMPERATUR"
    title_h = self.draw_header(title_text, einfuegehoehe_top)

    # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    if self.sprache == 'english':
        summary_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "The graphs show the projected evolution of mean number of heat days (maximum temperature > 35°C) and mean number of heat days (maximum temperature > 40°C) \
            for "+self.region+" from 1971 to 2098, based on CORDEX AFR22\
            regional climate model realizations under two emission scenarios: RCP2.6 (blue) and RCP8.5 (red). The solid lines represent \
            the median of the model ensemble for each scenario, while the shaded areas indicate the range between the minimum and maximum \
            values across all models. The historical reference period (1991–2020) is highlighted. The projections reveal a clear warming trend, with RCP8.5 showing a \
            strong increase toward the end of the century, while RCP2.6 stabilizes at a lower \
            level after mid-century. The shaded ranges illustrate the uncertainty among models, with wider bands indicating greater \
            variability in projections."
            "</span></para>"
        )
    else:
        summary_text = (
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "Les graphiques montrent l'évolution projetée de la température moyenne annuelle et du "
            "nombre moyen de jours de forte chaleur (température maximale > 40°C) pour "+self.region+" "
            "entre 1971 et 2098, sur la base des simulations des modèles climatiques régionaux CORDEX "
            "AFR22 selon deux scénarios d'émissions : RCP2.6 (bleu) et RCP8.5 (rouge). Les lignes continues "
            "représentent la médiane de l'ensemble des modèles pour chaque scénario, tandis que les zones ombrées "
            "indiquent l'intervalle compris entre les valeurs minimales et maximales de l'ensemble des modèles. "
            "La période de référence historique (1991–2020) est mise en évidence. Les projections montrent une "
            "nette tendance au réchauffement, le scénario RCP8.5 affichant une forte augmentation vers la fin "
            "du siècle, tandis que le scénario RCP2.6 se stabilise à un niveau plus faible après le milieu "
            "du siècle. Les zones ombrées illustrent l'incertitude entre les modèles, "
            "des bandes plus larges indiquant une plus grande variabilité des projections."
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
    if self.sprache == 'english':
        caption_text = (
            "<b>Figure 6:</b> Projected evolution of mean annual number of heatdays (maximum temperature >35 °C) for " + self.region + " \
            from 1971 to 2098 based on CORDEX AFR22 \
            regional climate model realizations under RCP2.6 (blue) and RCP8.5 (red) scenarios. Solid lines represent the ensemble median, \
            while shaded areas indicate the range between minimum and maximum values across all models, illustrating uncertainty."
        )   
    else:
        caption_text = (
            "<b>Figure 6:</b>Évolution projetée du nombre moyen annuel de jours de forte chaleur (température maximale >35 °C) pour " + self.region + " entre "
            "1971 et 2098, sur la base des simulations des modèles climatiques régionaux CORDEX AFR22 selon les "
            "scénarios RCP2.6 (bleu) et RCP8.5 (rouge). Les lignes continues représentent la médiane de l'ensemble "
            "des modèles, tandis que les zones ombrées indiquent l'intervalle compris entre les valeurs minimales "
            "et maximales de l'ensemble des modèles, illustrant l'incertitude des projections."
    )
    caption = Paragraph(caption_text, self.caption_style)
    _, cap_height = caption.wrapOn(self.c, available_width, self.height)

    # Zweite Grafik: ts_SU40_anomaly (Tage tmax> 40°C) darunter platzieren und skalieren
    
    if self.sprache == 'english':
        caption_text2 = (
            "<b>Figure 7:</b> Projected evolution of mean annual number of heatdays (maximum temperature >40 °C) for " + self.region + " \
            from 1971 to 2098 based on CORDEX AFR22 \
            regional climate model realizations under RCP2.6 (blue) and RCP8.5 (red) scenarios. Solid lines represent the ensemble median, \
            while shaded areas indicate the range between minimum and maximum values across all models, illustrating uncertainty."
        )
    else:
        caption_text2 = (
            "<b>Figure 7:</b> Évolution projetée du nombre moyen annuel de jours de forte chaleur (température maximale > 40 °C) "
            "pour " + self.region + " entre 1971 et 2098, sur la base des simulations des modèles climatiques régionaux CORDEX "
            "AFR22 selon les scénarios RCP2.6 (bleu) et RCP8.5 (rouge). Les lignes continues représentent la médiane de l'ensemble "
            "des modèles, tandis que les zones ombrées indiquent l'intervalle compris entre les valeurs minimales et maximales "
            "de l'ensemble des modèles, illustrant l'incertitude des projections."
        )

    caption2 = Paragraph(caption_text2, self.caption_style)
    _, cap_height2 = caption2.wrapOn(self.c, available_width, self.height)

    # Verfügbarer Platz: gleichmäßig verteilen
    gaps_between_blocks = 3  # gap after summary, between caption1 and image2, and before final bottom margin
    gap_size = self.kleiner_abstand
    available_height_total = start_y - bottom_margin - (gap_size * gaps_between_blocks) - cap_height - cap_height2
    image_height_each_max = max(1 * cm, available_height_total / 2.0)

    # Seitenverhältnisse prüfen und Höhe ggf. durch Breite begrenzen
    img_reader1 = utils.ImageReader(self.ts_SU35_anomaly)
    iw1, ih1 = img_reader1.getSize()
    aspect1 = ih1 / float(iw1)
    target_height1 = min(16.5 * cm, image_height_each_max, available_width * aspect1)

    img_reader2 = utils.ImageReader(self.ts_SU40_anomaly)
    iw2, ih2 = img_reader2.getSize()
    aspect2 = ih2 / float(iw2)
    target_height2 = min(16.5 * cm, image_height_each_max, available_width * aspect2)

    # Beide Bilder sollen gleich groß sein: nimm das kleinere der beiden Zielhöhen
    equal_height = min(target_height1, target_height2)

    # Erstes Bild zeichnen
    map_image = get_image(self.ts_SU35_anomaly, height=equal_height)
    map_image.wrapOn(self.c, self.width, self.height)
    img1_y = start_y - map_image.drawHeight
    map_image.drawOn(self.c, self.text_offset_links, img1_y)
    # Caption 1 direkt darunter
    caption_y = img1_y - gap_size
    caption.drawOn(self.c, self.text_offset_links, caption_y - cap_height)

    # Zweites Bild zeichnen, unter Caption 1
    second_start_y = caption_y - cap_height - gap_size
    map_image2 = get_image(self.ts_SU40_anomaly, height=equal_height)
    map_image2.wrapOn(self.c, self.width, self.height)
    img2_y = second_start_y - map_image2.drawHeight
    map_image2.drawOn(self.c, self.text_offset_links, img2_y)
    # Caption 2 darunter
    caption2_y = img2_y - gap_size
    caption2.drawOn(self.c, self.text_offset_links, caption2_y - cap_height2)