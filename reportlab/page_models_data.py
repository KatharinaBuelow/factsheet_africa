from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors

def insert_page_with_models_data(self):
    """
    Create a page with a table of simulations and citation of ERA5
    """
    #------------------ Seitenumbruch auf Impressum Seite
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
    The climate projections for Africa are based on <i>CORDEX-CORE_AFR22</i> data. 
    More information about CORDEX-CORE is described in the following papers Giorgi (2022), Remedio (2019), Teichmann (2021) and Coppola (2021b).<br/><br/>
    The data is available on 0.22° horizontal resolution. The multi-model ensemble from AFR22-CORDEX is 
    based on 3 regional climate models (RCMs), 
    which are driven by 3 different global climate models (GCMs) under the RCP2.6 and RCP8.5 scenarios, 
    resulting in a total of 18 simulations for each variable and region. 
    The table below provides an overview of the RCM-GCM combinations used for the projections.<br/><br/>
    Data access: Copernicus Climate Data Store (DOI: 10.24381/cds.adbb2d47). More general information on climate models and 
    model diagnostics is documented in Diez-Sierra et al. (2022).<br/><br/>

    """

# Diez-Sierra, J., and Coauthors, 2022: The Worldwide C3S CORDEX Grand Ensemble: A Major Contribution to Assess Regional Climate Change in the IPCC AR6 Atlas. Bull. Amer. Meteor. Soc., 103, E2804–E2826, https://doi.org/10.1175/BAMS-D-22-0111.1. 

    intro_para = Paragraph(text, self.styles["BodyText"])
    intro_w, intro_h = intro_para.wrapOn(
        self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height
    )
    einfuegehoehe = einfuegehoehe_top - title_h - intro_h - self.kleiner_abstand
    intro_para.drawOn(self.c, self.text_offset_links, einfuegehoehe)
    
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
    
    # Calculate table position
    table_x = self.text_offset_links

    table_w, table_h = table.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    einfuegehoehe = einfuegehoehe - self.kleiner_abstand - table_h
    table.drawOn(self.c, table_x, einfuegehoehe)

    # -----------------------------------------
    # Caption
    # -----------------------------------------
    caption = Paragraph("<b>Tabelle 1:</b> List of climate simulations used.", self.styles["BodyText"])
    caption_w, caption_h = caption.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    einfuegehoehe = einfuegehoehe - caption_h - self.kleiner_abstand
    caption.drawOn(self.c, self.text_offset_links, einfuegehoehe)
    self.story.append(table)
    self.story.append(Spacer(1, 12))

    # --------------------------------------
    # Data source section
    # -----------------------------------
    #--------------------------
    # Titel: 
    #-------------------------
    title_text = "Data source" if self.sprache == 'english' else "Datenquelle"
    title_para = Paragraph(
        f"<para><span name=Helvetica-Bold size=12>{title_text}</span></para>",
        self.styles.get('Heading', getSampleStyleSheet()['Heading1'])
    )
    title_w, title2_h = title_para.wrapOn(
        self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height
    )
    einfuegehoehe = einfuegehoehe - self.kleiner_abstand*2 - title2_h
    title_para.drawOn(self.c, self.text_offset_links, einfuegehoehe)

    
    #data_title = "Data source" if self.sprache == 'english' else "Datenquelle"
    #data_para = Paragraph(f"<para><span name=Helvetica size=12>{data_title}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, data_h = data_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #data_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - data_h)
    # Add the reference below the title
    
    if self.sprache == 'english':
        data_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
        Observational baseline: ERA5 ( Hersbach H, Bell B, Berrisford P, et al.\
        The ERA5 global reanalysis. Q J R Meteorol Soc. 2020; 146: 1999–2049. https://doi.org/10.1002/qj.3803).</span></para>',self.styles['Justify'], encoding='utf8')
    else:
        data_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
            Beobachtungsgrundlage: ERA5 ( Hersbach H, Bell B, Berrisford P, et al.\
            The ERA5 global reanalysis. Q J R Meteorol Soc. 2020; 146: 1999–2049. https://doi.org/10.1002/qj.3803). \nKlimaprojektionen: Multi-Modell-Ensemble aus AFR22-CORDEX basierend auf den Szenarien RCP2.6 und RCP8.5. \nDatenzugang: Copernicus Climate Data Store (DOI: 10.24381/cds.adbb2d47).\
            </span></para>',
            self.styles['Justify'], encoding='utf8')
    link_width, data_height = data_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    einfuegehoehe = einfuegehoehe - data_height - self.kleiner_abstand
    data_text.drawOn(self.c, self.text_offset_links, einfuegehoehe)


# Giorgi, F., and Coauthors, 2022: The CORDEX-CORE EXP-I Initiative: Description and Highlight Results from the Initial Analysis. Bull. Amer. Meteor. Soc., 103, E293–E310, https://doi.org/10.1175/BAMS-D-21-0119.1.


# Remedio, A.R.; Teichmann, C.; Buntemeyer, L.; Sieck, K.; Weber, T.; Rechid, D.; Hoffmann, P.; Nam, C.; Kotova, L.; Jacob, D. Evaluation of New CORDEX Simulations Using an Updated Köppen–Trewartha Climate Classification. Atmosphere 2019, 10, 726. https://doi.org/10.3390/atmos10110726*

# Teichmann, C., Jacob, D., Remedio, A.R. et al. Assessing mean climate change signals in the global CORDEX-CORE ensemble. Clim Dyn 57, 1269–1292 (2021). https://doi.org/10.1007/s00382-020-05494-x*

# Coppola, E., and Coauthors, 2021b: Climate hazard indices projections based on CORDEX-CORE, CMIP5 and CMIP6 ensemble. Climate Dyn., 57, 1293–1383, https://doi.org/10.1007/s00382-021-05640-z.

    