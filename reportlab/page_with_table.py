from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image


def insert_page_with_table(self):
    """
    Create a page with a table
    """
    # Beispielbild und Text
    # Zuerst: Zusammenfassungstext über der Tabelle
    einfuegehoehe_top = self.height - 2 * cm
    # Titel: Climate indicators
    
    title_text = "CLIMATE INDICATORS" if self.sprache == 'english' else "INDICATEURS CLIMATIQUES"
    title_para = Paragraph(f"<para><span name=Helvetica-Bold size=14>{title_text}</span></para>", self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, title_h = title_para.wrapOn(
    #    self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #title_para.drawOn(self.c, self.text_offset_links, einfuegehoehe_top - title_h)
    title_h = self.draw_header(title_text, einfuegehoehe_top)

    # Reduce spacing between title and summary
    einfuegehoehe_top = einfuegehoehe_top - title_h - self.kleiner_abstand

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    if self.sprache == 'english':
        summary_text = (
            "<para><span name=Helvetica size='"+str(self.schrift_fliesstext)+"'>"
            "The table presents projected climate indicators for " + self.region + " under two emission "
            "scenarios (RCP2.6 and RCP8.5) across different time periods, compared to the historical "
            "baseline (1991–2020). It includes temperature, precipitation, and wind metrics, "
            "along with extremes. The left column of the table shows the area-mean values "
            "for " + self.region + " based on ERA5 data for the reference period (1991–2020). "
            "Overall, the table highlights significant warming and more frequent extreme heat events, "
            "while precipitation changes are less pronounced."
            "</span></para>"
        )
    else:
        summary_text = (
            "<para><span name=Helvetica size='"+str(self.schrift_fliesstext)+"'>"
            "Le tableau présente les indicateurs climatiques projetés pour " + self.region + 
            " selon deux scénarios d'émissions (RCP2.6 et RCP8.5) pour différentes périodes, "
            "par rapport à la période de référence historique (1991–2020). Il comprend des indicateurs "
            "de température, de précipitations et de vent, ainsi que des indices relatifs aux événements "
            "extrêmes. La colonne de gauche du tableau présente les valeurs moyennes spatiales "
            "pour " + self.region + " basées sur les données ERA5 pour la période de référence "
            "(1991–2020). Dans l'ensemble, le tableau met en évidence un réchauffement important "
            "et une augmentation de la fréquence des épisodes de chaleur extrême, tandis que les "
            "changements de précipitations sont moins marqués."
           "</span></para>"
        )

    para = Paragraph(summary_text, styles["Justify"]) 
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    para_width, para_height = para.wrapOn(self.c, available_width, self.height)
    # Text oben platzieren
    para.drawOn(self.c, self.text_offset_links, einfuegehoehe_top - para_height)

    # position of the table below the summary text
    einfuegehoehe_table = einfuegehoehe_top - para_height - self.kleiner_abstand

    map_image = get_image(self.table_cc, height=17.3 * cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_table - map_image.drawHeight)

    # Bildunterschrift direkt unter der Tabelle
    if self.sprache == 'english':
        caption_text = (
            "<b>Table 1:</b> Projected climate indicators for " + self.region + " under the RCP2.6 and RCP8.5 "
            "scenarios for different time periods compared to the 1991–2020 baseline. The left column shows "
            "the area-mean values for " + self.region + " based on ERA5 data for the reference period (1991–2020). "
            "Climate change estimates are derived from a multi-model ensemble. The values shown represent the "
            "median, with half of the models projecting higher values and half projecting lower values. "
            "The ranges (Min–Max) indicate the minimum and maximum values across all models. "
            "The level of robustness of the climate change signal is depicted by the intensity of the grey shading."
        )
    else:
        caption_text = (
            "<b>Tabelle 1:</b> Indicateurs climatiques projetés pour " + self.region + " selon les scénarios "
            "RCP2.6 et RCP8.5 pour différentes périodes, comparées à la période de référence 1991–2020. La colonne "
            "de gauche présente les valeurs moyennes spatiales pour " + self.region + ", basées sur les données ERA5 "
            "pour la période de référence (1991–2020). Les estimations des changements climatiques sont issues d'un ensemble "
            "multi-modèles. Les valeurs présentées correspondent à la médiane, avec la moitié des modèles projetant des "
            "valeurs plus élevées et l'autre moitié des valeurs plus faibles. Les plages (Min–Max) indiquent les valeurs "
            "minimales et maximales observées parmi l'ensemble des modèles. Le degré de robustesse du signal de changement "
            "climatique est représenté par l'intensité de la trame grise."    
        )               
    caption = Paragraph(caption_text, self.caption_style)
    _, cap_height = caption.wrapOn(self.c, available_width, self.height)

    caption_y = einfuegehoehe_table - map_image.drawHeight- self.kleiner_abstand - cap_height
    caption.drawOn(self.c, self.text_offset_links, caption_y)