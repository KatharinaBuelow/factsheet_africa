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

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    summary_text = (
        "<para><span name=Helvetica size=10>"
        "The table presents projected climate indicators for Burkina Faso under two emission scenarios (RCP2.6 and RCP8.5) across different time periods, compared to the historical baseline (1991–2020). It includes temperature, precipitation, and wind metrics, along with extremes.<br/><br/> "
        "The left column of the table shows the area-mean values for Burkina Faso based on ERA5 data for the reference period (1991–2020)."
        "Overall, the table highlights significant warming and more frequent extreme heat events, while precipitation changes are less pronounced."
        "</span></para>"
    )

    para = Paragraph(summary_text, styles["Justify"]) 
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    para_width, para_height = para.wrapOn(self.c, available_width, self.height)
    # Text oben platzieren
    para.drawOn(self.c, self.text_offset_links, einfuegehoehe_top - para_height)

    # Danach: Tabelle direkt unter dem Text platzieren
    einfuegehoehe_table = einfuegehoehe_top - para_height - self.kleiner_abstand
    map_image = get_image(self.table_cc, height=16.5 * cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_table - map_image.drawHeight)

    # Bildunterschrift direkt unter der Tabelle
    caption_text = (
        "<para><span name=Helvetica size=9>"
        "<b>Table 1:</b> Projected climate indicators for Burkina Faso under RCP2.6 and RCP8.5 scenarios for different time periods compared to the 1991–2020 baseline. "
        "The left column shows the area-mean values for Burkina Faso based on ERA5 data for the reference period (1991–2020). "
        "Climate change estimates are derived from a multi-model ensemble. The values shown represent the median, with half of the models projecting higher and half lower values. "
        "The ranges (Min–Max) indicate the minimum and maximum across all models."
        "</span></para>"
    )
    caption = Paragraph(caption_text, styles['Justify'])
    cap_width, cap_height = caption.wrapOn(self.c, available_width, self.height)
    caption_y = (einfuegehoehe_table - map_image.drawHeight) - self.kleiner_abstand
    caption.drawOn(self.c, self.text_offset_links, caption_y - cap_height)