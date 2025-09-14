from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from utils_image import get_image


def insert_page_with_table(self):
    """
    Create a page with a table
    """
    # Beispielbild und Text
    # tabelle clima indicatoren
    einfuegehoehe_table = self.height - 2*cm
    map_image = get_image(self.table_cc, height = 16.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe_table - map_image.drawHeight)

    styles = getSampleStyleSheet()
    for i in range(5):
        text = f"Dies ist Beispielzeile {i+1} für den Text unter der Tabelle."
        para = Paragraph(text, styles["Normal"])
        para.wrapOn(self.c, self.width - 2 * self.text_offset_links, self.height)
        para.drawOn(self.c, self.text_offset_links, einfuegehoehe_table - map_image.drawHeight - (i+1)*20)