from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors

class PageModelsData:
    def __init__(self, c, story, styles, width, height, text_offset_links, text_offset_rechts, sprache='english'):
        self.c = c
        self.story = story
        self.styles = styles
        self.width = width
        self.height = height
        self.text_offset_links = text_offset_links
        self.text_offset_rechts = text_offset_rechts
        self.sprache = sprache

    def insert_page_with_models_data(self):
        """
        Create a page with a table of simulations and citation of ERA5
        """
        #------------------ Seitenumbruch auf Impressum Seite
        self.c.showPage()
        einfuegehoehe_top = self.height - 2 * cm

        #--------------------------
        # Titel: 
        #-------------------------
        title_text = "List of climate simulations" if self.sprache == 'english' else "Liste der Klimasimulationen"
        title_para = Paragraph(
            f"<para><span name=Helvetica-Bold size=12>{title_text}</span></para>",
            self.styles.get('Heading', getSampleStyleSheet()['Heading1'])
        )
        title_w, title_h = title_para.wrapOn(
            self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height
        )
        title_para.drawOn(self.c, self.text_offset_links, einfuegehoehe_top - title_h)

        # -----------------------------------------
        # Intro Text
        # -----------------------------------------
        text = """
        The climate simulations for Africa are based on <i>CORDEX-CORE_AFR22</i> data. 
        More information about CORDEX-CORE is described in the following papers [1], [2], [3], [4].<br/><br/>
        The data is available on 0.22° horizontal resolution and can be downloaded from the 
        Earth System Grid Federation (ESGF). Model details and information on the data format 
        can be found online. More general information on climate models and 
        model diagnostics is documented in Diez-Sierra et al. (2022).<br/><br/>

        The following table documents the high-resolution climate models available for Africa.
        """
        self.story.append(Paragraph(text, self.styles["BodyText"]))
        self.story.append(Spacer(1, 12))

        # -----------------------------------------
        # Table Data
        # -----------------------------------------
        data = [
            ["Regional Climate Model", "Global Climate Model", "Scenario", "Realisation"],
            ["CLMcom-KIT-CCLM5-0-15", "MOHC-HadGEM2-ES", "RCP2.6, RCP8.5", "r1i1p1"],
            ["CLMcom-KIT-CCLM5-0-15", "MPI-M-MPI-ESM-LR", "RCP2.6, RCP8.5", "r1i1p1"],
            ["CLMcom-KIT-CCLM5-0-15", "NCC-NorESM1-M", "RCP2.6, RCP8.5", "r12i1p1"],
            ["GERICS-REMO2015", "MOHC-HadGEM2-ES", "RCP2.6, RCP8.5", "r1i1p1"],
            ["GERICS-REMO2015", "MPI-M-MPI-ESM-LR", "RCP2.6, RCP8.5", "r1i1p1"],
            ["GERICS-REMO2015", "NCC-NorESM1-M", "RCP2.6, RCP8.5", "r12i1p1"],
            ["ICTP-RegCM4-7", "MOHC-HadGEM2-ES", "RCP2.6, RCP8.5", "r1i1p1"],
            ["ICTP-RegCM4-7", "MPI-M-MPI-ESM-MR", "RCP2.6, RCP8.5", "r1i1p1"],
            ["ICTP-RegCM4-7", "NCC-NorESM1-M", "RCP2.6, RCP8.5", "r12i1p1"],
        ]

        # -----------------------------------------
        # Build Table
        # -----------------------------------------
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.black),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 12))

        # -----------------------------------------
        # Caption
        # -----------------------------------------
        caption = Paragraph("<b>Tabelle 1:</b> List of climate simulations used.", self.styles["BodyText"])
        self.story.append(caption)
