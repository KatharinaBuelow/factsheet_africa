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
    
    title_text = "CLIMATE INDICATORS" if self.sprache == 'english' else "KLIMATISCHE INDIKATOREN"
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
    summary_text = (
        "<para><span name=Helvetica size='"+str(self.schrift_fliesstext)+"'>"
        "The table presents projected climate indicators for Burkina Faso under two emission scenarios (RCP2.6 and RCP8.5) across different time periods, compared to the historical baseline (1991–2020). It includes temperature, precipitation, and wind metrics, along with extremes. "
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

    map_image = get_image(self.table_cc, height=17.3 * cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_table - map_image.drawHeight)

    # Bildunterschrift direkt unter der Tabelle
    caption_text = (
        "<b>Table 1:</b> Projected climate indicators for Burkina Faso under RCP2.6 and RCP8.5 scenarios for different time periods compared to the 1991–2020 baseline. "
        "The left column shows the area-mean values for Burkina Faso based on ERA5 data for the reference period (1991–2020). "
        "Climate change estimates are derived from a multi-model ensemble. The values shown represent the median, with half of the models projecting higher and half lower values. "
        "The ranges (Min–Max) indicate the minimum and maximum across all models."
    )

    caption = '<para><span name=Helvetica color=black size='+str(self.schrift_caption)+'>'+caption_text+'</span></para>'
    caption = Paragraph(caption, styles['Justify'])

    cap_width, cap_height = caption.wrapOn(self.c, available_width, self.height)
    caption_y = einfuegehoehe_table - map_image.drawHeight- self.kleiner_abstand - cap_height
    caption.drawOn(self.c, self.text_offset_links, caption_y)