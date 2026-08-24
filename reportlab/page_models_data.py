from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
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
    title_text = "LIST OF CLIMATE SIMULATIONS" if self.sprache == 'english' else "LISTE DER KLIMASIMULATIONEN"
    title_h = self.draw_header(title_text, einfuegehoehe_top)
    # Reduce spacing between title and summary
    einfuegehoehe= einfuegehoehe_top - title_h - self.kleiner_abstand

    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
         
    # -----------------------------------------
    # Intro Text
    # -----------------------------------------
    intro_text_data = (
        f"<para><span name='Helvetica' size='{self.schrift_fliesstext}'>"
        "The climate projections for Africa are based on <i>CORDEX-CORE AFR22</i> data. "
        "More information about CORDEX-CORE is described in the following papers Giorgi (2022), "
        "Remedio (2019), Teichmann (2021) and Coppola (2021)."
        "<br/><br/>"
        "The data is available on 0.22° horizontal resolution. The multi-model ensemble is "
        "based on 3 regional climate models (RCMs), which are driven by 3 different global climate models (GCMs) "
        "under the RCP2.6 and RCP8.5 scenarios, resulting in a total of 18 simulations for each variable and region. "
        "The table below provides an overview of the RCM-GCM combinations used for the projections."
        "<br/><br/>"
        "Data access: Copernicus Climate Data Store (DOI: 10.24381/cds.adbb2d47). "
        "More general information on climate models and model diagnostics is documented in Diez-Sierra et al. (2022)."
        "</span></para>"
    )

    intro_para = Paragraph(intro_text_data, styles["Justify"])
    intro_w, intro_h = intro_para.wrapOn(
        self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height
    )
    intro_para.drawOn(self.c, self.text_offset_links, einfuegehoehe -intro_h)

    einfuegehoehe = einfuegehoehe- intro_h - self.kleiner_abstand
    
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
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    # Make columns 3 and 4 thinner while keeping full table width
    col_weights = [1.2, 1.1, 0.85, 0.6]
    weight_sum = sum(col_weights)
    col_widths = [available_width * (w / weight_sum) for w in col_weights]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.black),
            ("ALIGN", (0,0), (-1,-1), "LEFT"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
            ("FONTSIZE", (0,0), (-1,-1), 12),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
    
    # Calculate table position
    table_x = self.text_offset_links

    table_w, table_h = table.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    table.drawOn(self.c, table_x, einfuegehoehe - table_h)
    einfuegehoehe= einfuegehoehe - table_h - self.kleiner_abstand

    # -----------------------------------------
    # Caption
    # -----------------------------------------
    table2 ='<b>Tabelle 3:</b> List of climate simulations used.'
    
    caption_size = max(self.schrift_caption, self.schrift_fliesstext)
    caption_table2 = '<para><span name=Helvetica color=black size='+str(caption_size)+'>'+table2+'</span></para>'
    caption_table2 = Paragraph(caption_table2, styles['Justify'])
    _, caption_h = caption_table2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    caption_table2.drawOn(self.c, self.text_offset_links, einfuegehoehe - caption_h)
    self.story.append(table)
    self.story.append(Spacer(1, 12))

    einfuegehoehe= einfuegehoehe - caption_h - self.kleiner_abstand * 2

    # --------------------------------------
    # Data source section
    # -----------------------------------
    title_text2 = "DATA SOURCE" if self.sprache == 'english' else "DATENQUELLE"
    title2_h = self.draw_header(title_text2, einfuegehoehe)

    einfuegehoehe = einfuegehoehe - title2_h - self.kleiner_abstand

    # Suggestion: build paragraph text as one complete string to avoid unclosed tags
    if self.sprache == 'english':
        obs_body = (
            "Observational baseline: ERA5 (Hersbach H, Bell B, Berrisford P, et al. "
            "The ERA5 global reanalysis. Q J R Meteorol Soc. 2020; 146: 1999–2049. "
            "https://doi.org/10.1002/qj.3803)."
        )
    else:
        obs_body = (
            "Beobachtungsgrundlage: ERA5 (Hersbach H, Bell B, Berrisford P, et al. "
            "The ERA5 global reanalysis. Q J R Meteorol Soc. 2020; 146: 1999–2049. "
            "https://doi.org/10.1002/qj.3803)."
        )

    obs_text = (
        f"<para><span name='Helvetica' size='{self.schrift_fliesstext}'>"
        f"{obs_body}"
        "</span></para>"
    )

    para = Paragraph(obs_text, styles["Justify"])
    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    _, data_height = para.wrapOn(self.c, available_width, self.height)
    para.drawOn(self.c, self.text_offset_links, einfuegehoehe - data_height)
    einfuegehoehe = einfuegehoehe - data_height - self.kleiner_abstand

    # --------------------------------------
    # Literature chapter (bottom of page)
    # --------------------------------------

    literature_title = "LITERATURE" if self.sprache == 'english' else "LITERATUR"
    literature_title_h = self.draw_header(literature_title, einfuegehoehe)
    einfuegehoehe = einfuegehoehe - literature_title_h - self.kleiner_abstand

    literature_entries = [
        "Coppola, E., and Coauthors, 2021: Climate hazard indices projections based on CORDEX-CORE, CMIP5 and CMIP6 ensemble. Climate Dyn., 57, 1293–1383, https://doi.org/10.1007/s00382-021-05640-z.",
        "Diez-Sierra, J., and Coauthors, 2022: The Worldwide C3S CORDEX Grand Ensemble: A Major Contribution to Assess Regional Climate Change in the IPCC AR6 Atlas. Bull. Amer. Meteor. Soc., 103, E2804–E2826, https://doi.org/10.1175/BAMS-D-22-0111.1.",
        "Giorgi, F., and Coauthors, 2022: The CORDEX-CORE EXP-I Initiative: Description and Highlight Results from the Initial Analysis. Bull. Amer. Meteor. Soc., 103, E293–E310, https://doi.org/10.1175/BAMS-D-21-0119.1.",
        "Remedio, A.R.; Teichmann, C.; Buntemeyer, L.; Sieck, K.; Weber, T.; Rechid, D.; Hoffmann, P.; Nam, C.; Kotova, L.; Jacob, D. Evaluation of New CORDEX Simulations Using an Updated Köppen–Trewartha Climate Classification. Atmosphere 2019, 10, 726. https://doi.org/10.3390/atmos10110726*",
        "Teichmann, C., Jacob, D., Remedio, A.R. et al. Assessing mean climate change signals in the global CORDEX-CORE ensemble. Clim Dyn 57, 1269–1292 (2021). https://doi.org/10.1007/s00382-020-05494-x",
        
    ]

    formatted_entries = []
    for entry in literature_entries:
        first_author, rest = entry.split(",", 1)
        formatted_entries.append(f"<b>{first_author}</b>,{rest}")
    literature_body = "<br/>".join(formatted_entries)
    literature_text = (
        "<para>"
        f"<span name='Helvetica' size='11'>{literature_body}</span>"
        "</para>"
    )

    literature_para = Paragraph(literature_text, styles["Justify"])
    _, literature_h = literature_para.wrapOn(self.c, available_width, self.height)
    literature_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - literature_h)

    