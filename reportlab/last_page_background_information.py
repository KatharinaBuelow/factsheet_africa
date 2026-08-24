import os
import sys
import numpy
import scipy
import scipy.stats
import collections
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table, Flowable, PageBreak, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import ListItem, ListFlowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from utils_image import get_image
from six import string_types
from netCDF4 import Dataset
import re
import pandas as pd

def insert_impressum(self):
    #------------------ Seitenumbruch auf Impressum Seite
    #self.c.showPage()
    #  
    #logos at the top:
    #
    einfuegehoehe = self.height - 0.2 * cm    
    map_image = get_image(self.bmbf_logo, height = 1.6*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links , einfuegehoehe - map_image.drawHeight)
    # hereon
    einfuegehoehe = self.height - 0.2 * cm
    map_image2 = get_image(self.hereon_logo, height = 1.4*cm)
    logo_breite2 = map_image2.drawWidth
    # Draw HEREON logo at the top right corner
    map_image2.wrapOn(self.c, self.width, self.height)
    map_image2.drawOn(self.c, self.width - self.text_offset_rechts - logo_breite2, einfuegehoehe - map_image2.drawHeight)
    einfuegehoehe_top = self.height - 2 * cm

    #--------------------------
    # Titel: 
    #-------------------------
    title_text = "BACKGROUND INFORMATION" if self.sprache == 'english' else "Hintergrundinformationen"
    title_h = self.draw_header(title_text, einfuegehoehe_top)

    #title_para = Paragraph(f"<para><span name=Helvetica-Bold size=14>{title_text}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, title_h = title_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #title_para.drawOn(self.c, self.text_offset_links, einfuegehoehe_top - title_h)
    
    # Reduce spacing between title and summary
    einfuegehoehe = einfuegehoehe_top - title_h - self.kleiner_abstand
    #einfuegehoehe = self.height - 3.5*cm - self.kleiner_abstand
    
    #---------------------------------------
    # Link to github repository
    # --------------------------------------   
    #einfuegehoehe = einfuegehoehe_top - title_h - self.kleiner_abstand*0.5

    Inf_text = "INFORMATION, LITERATURE, SOFTWARE" if self.sprache == 'english' else "Hintergrundinformationen"
    title_info = self.draw_header2(Inf_text, einfuegehoehe)
    #info_para = Paragraph(f"<para><span name=Helvetica size=12>{Inf_text}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, info_h = info_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #info_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - info_h)
    # Add the link_text below the info title
    einfuegehoehe = einfuegehoehe - title_info - self.kleiner_abstand*0.2
    
    if self.sprache == 'english':
        link_text = Paragraph('<para><span name=Helvetica color=blue size=10><link href="https://github.com/climate-service-center">https://github.com/climate-service-center</link></span></para>',
            self.styles['Justify'], encoding='utf8')
    else:
        link_text = Paragraph('<para><span name=Helvetica color=blue size=10><u><link href="https://github.com/climate-service-center">https://github.com/climate-service-center</link></u></span></para>',
            self.styles['Justify'], encoding='utf8')
    link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height)

    # --------------------------------------
    # Reference needs to be adjusted
    #---------------------------------------

    einfuegehoehe = einfuegehoehe - link_height - self.kleiner_abstand*0.5

    Ref_text = "REFERENCE" if self.sprache == 'english' else "REFERENZ"
    title_R = self.draw_header2(Ref_text, einfuegehoehe)

    #ref_para = Paragraph(f"<para><span name=Helvetica size=12>{Ref_text}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, ref_h = ref_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #ref_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - ref_h)
    # Add the reference below the title
    einfuegehoehe = einfuegehoehe - title_R - self.kleiner_abstand*0.2
    if self.sprache == 'english':
        ref_text = Paragraph('<para> <span name=Helvetica color=black size = 11>\
                THIS WILL BE REPLACED WITH THE FINAL DOI, Climate Service Center Germany (GERICS)\
                </span></para>',
                self.styles['Justify'], encoding='utf8')
    else:
        ref_text = Paragraph('<para><span name=Helvetica color=blue size=10><u><link href="https://www.gerics.de/climate-service-center">https://www.gerics.de/climate-service-center</link></u></span></para>',
            self.styles['Justify'], encoding='utf8')
    ref_width, ref_height = ref_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    ref_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - ref_height)

    # --------------------------
    # Authors / Issuer section
    #---------------------------
    einfuegehoehe = einfuegehoehe - ref_height - self.kleiner_abstand*0.5

    issuer_title = "ISSUER" if self.sprache == 'english' else "AUTORINNEN UND AUTOREN"
    title_issu = self.draw_header2(issuer_title, einfuegehoehe)
    #issuer_para = Paragraph(f"<para><span name=Helvetica size=12>{issuer_title}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, issuer_h = issuer_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #issuer_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - issuer_h)
    # Add the issuer below the title
    einfuegehoehe = einfuegehoehe - title_issu - self.kleiner_abstand*0.2

    if self.sprache == 'english':
        issuer_text = Paragraph('<para> <span name=Helvetica color=black size = 11>\
            Climate Service Center Germany (GERICS), an Institution of the Helmholtz-Zentrum Hereon GmbH, Fischertwiete 1, 20095 Hamburg, Germany, and\n WASCAL (West African Science Service Center on Climate Change and Adapted Land Use), Accra, Ghana.\
            </span></para>',
            self.styles['Justify'], encoding='utf8')
    else:
        issuer_text = Paragraph('<para> <span name=Helvetica color=black size = 11>\
            Climate Service Center Germany (GERICS), an Institution of the Helmholtz-Zentrum Hereon GmbH, Fischertwiete 1, 20095 Hamburg, Germany, and WASCAL (West African Science Service Center on Climate Change and Adapted Land Use), Accra, Ghana.\
            </span></para>',
            self.styles['Justify'], encoding='utf8')
    issuer_width, issuer_height = issuer_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    issuer_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - issuer_height)
    
    # --------------------------
    # contact information section
    #---------------------------
    einfuegehoehe = einfuegehoehe - issuer_height - self.kleiner_abstand *0.5

    contact_title = "CONTACT INFORMATION" if self.sprache == 'english' else "KONTAKTINFORMATIONEN"
    title_contact = self.draw_header2(contact_title, einfuegehoehe)

    #contact_para = Paragraph(f"<para><span name=Helvetica size=12>{contact_title}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, contact_h = contact_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #contact_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - contact_h)
    # Add the contact information below the title
    einfuegehoehe = einfuegehoehe - title_contact - self.kleiner_abstand*0.2

    if self.sprache == 'english':
        contact_text = Paragraph('<para> <span name=Helvetica color=black size = 11>Torsten Weber torsten.weber@hereon.de, Seyni Salack salack.s@wascal.org</span></para>',self.styles['Justify'], encoding='utf8')
    else:
        contact_text = Paragraph('<para> <span name=Helvetica color=black size = 11>Torsten Weber torsten.weber@hereon.de, Seyni Salack salack.s@wascal.org</span></para>',self.styles['Justify'], encoding='utf8')
    issuer_width, contact_height = contact_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    contact_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - contact_height)

    # --------------------------------------
    # Disclaimer chapter
    #---------------------------------------
    einfuegehoehe = einfuegehoehe - contact_height - self.kleiner_abstand*0.5
    dis_title = "DISCLAIMER" if self.sprache == 'english' else "HAFTUNGSAUSSCHLUSS"
    title_dis = self.draw_header2(dis_title, einfuegehoehe)

    #dis_para = Paragraph(f"<para><span name=Helvetica size=12>{dis_title}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, dis_h = dis_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #dis_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - dis_h)
    # Add the disclaimer below the title
    einfuegehoehe = einfuegehoehe - title_dis - self.kleiner_abstand*0.2

    if self.sprache == 'english':
        text_disclaimer = Paragraph('<para><span name=Helvetica color=black size = 11> This Regional Climate Factsheet was developed by Climate Service Center Germany (GERICS), an institution of the  Helmholtz-Zentrum hereon GmbH. The content provided in this factsheet and the underlying data correspond to the current state of knowledge. All data have been carefully prepared and checked by the Climate Service Center Germany (GERICS). However, GERICS has only carried out part of the regional climate projections itself. All climate projections not carried out by GERICS were obtained from the publicly accessible copernicus climate data store. GERICS does not take over guarantee for the topicality, correctness, completeness or quality of the provided information. GERICS also assumes no liability for decisions and their consequences, which are based on the use of this Regional Climate Factsheet. </span></para>', self.styles['Justify'], encoding='utf8')
    else:
        self.c.drawString(self.text_offset_links, einfuegehoehe, "HAFTUNGSAUSSCHLUSS:")
        text_disclaimer = Paragraph('<para><span name=Helvetica color=black size=10> Dieses Climate Factsheet dient ausschließlich Informationszwecken. Trotz sorgfältiger Zusammenstellung der Daten und Analysen übernehmen Herausgeber und Autorinnen/Autoren keine Gewähr für Vollständigkeit oder Richtigkeit und haften nicht für Entscheidungen oder Handlungen, die auf Grundlage dieses Dokuments getroffen werden.</span></para>', self.styles['Justify'], encoding='utf8')
    link_width, dis_height = text_disclaimer.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    text_disclaimer.drawOn(self.c, self.text_offset_links, einfuegehoehe-dis_height)    

    # --------------------------------------
    # Acknowledgements chapter
    #---------------------------------------
    einfuegehoehe = einfuegehoehe - dis_height - self.kleiner_abstand*0.5
    ack_title = "ACKNOWLEDGEMENTS" if self.sprache == 'english' else "DANKSAGUNGEN"
    title_ack= self.draw_header2(ack_title, einfuegehoehe)
    #ack_para = Paragraph(f"<para><span name=Helvetica size=12>{ack_title}</span></para>",self.styles.get('Heading', getSampleStyleSheet()['Heading1']))
    #title_w, ack_h = ack_para.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    #ack_para.drawOn(self.c, self.text_offset_links, einfuegehoehe - ack_h)
    # Add the disclaimer below the title
    einfuegehoehe = einfuegehoehe - title_ack - self.kleiner_abstand*0.2

    if self.sprache == 'english':
        text_ack = Paragraph(
            """<para><span name=Helvetica color=black size = 11>
            We thank the Working Group on Regional Climate of the World Climate Research Programme (WCRP) and the Working Group on Coupled Modelling, the former coordinating body of CORDEX and the responsible panel for CMIP5. We also thank the CORDEX climate modelling groups for producing and providing their model results.<br/>
            Our thanks go to the Copernicus Climate Change Service (C3S) for providing access to the CORDEX and the ERA5 data through the Copernicus Climate Data Store.<br/>
            The content of this factsheet was collaboratively shaped during the workshop on Co-development and co-design of prototype climate fact sheets on single and compound climate extremes (May, 2025), and we would like to express our sincere gratitude to all contributors, including:<br/>
            Those from Togo: Agence Nationale de la Protection Civile (ANPC), Agence Nationale de la Gestion de l’Environnement (ANGE), Agence Régionale pour l’Agriculture et l’Alimentation (ARAA), Direction des Ressources en Eau (DRE), Agence Nationale de la Météorologie du Togo (ANAMET), Direction de l'Environnement (DE), Institut du Conseil et d'appui Technique (ICAT), Direction de l'Assainissement, Institut Togolais de Recherche Agronomique (ITRA), FURIFLOOD project, Croix Rouge Togolaise (CRT).<br/>
            Those from Côte d’Ivoire: Société d'Exploitation et de Développement Aéroportuaire, Aéronautique et Météorologique (SODEXAM), Ministère de l'Hydraulique/Direction de l’Hydrologie, Direction Générale des Ressources en Eau (DGRE), Agence National d'Appui eu Développement Rural (ANADER) , Programme National Changements Climatiques (PNCC).<br/>
            Those from Burkina Faso: Faitière des Caisses Populaires du Burkina (FCBP), Direction Générale des Productions Végétales (DGPV), Secrétariat Permanent du Conseil National pour le Développement Durable (SP/CNDD), Secrétariat Permanent du Conseil National de Sécurité Alimentaire (SP/ CNSA), Direction Générale des Ressources Halieutiques (DGRH), Conseil National de Secours d’Urgence et de Réhabilitation (CONASUR), Union Internationale pour la Conservation de la Nature (UICN), Agence Nationale de la Météorologie du Burkina Faso (ANAM-BF), Comité Inter-état de Lutte contre la Sécheresse dans le Sahel (CILSS), Croix-Rouge Burkina Faso (CRBF).</span></para>""",
            self.styles['Justify'],
            encoding='utf8'
        )
    else:
        self.c.drawString(self.text_offset_links, einfuegehoehe, "Haftungsausschluss:")
        text_ack = Paragraph('<para><span name=Helvetica color=black size=10> Dieses Climate Factsheet dient ausschließlich Informationszwecken. Trotz sorgfältiger Zusammenstellung der Daten und Analysen übernehmen Herausgeber und Autorinnen/Autoren keine Gewähr für Vollständigkeit oder Richtigkeit und haften nicht für Entscheidungen oder Handlungen, die auf Grundlage dieses Dokuments getroffen werden.</span></para>', self.styles['Justify'], encoding='utf8')
    link_width, acc_height = text_ack.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    text_ack.drawOn(self.c, self.text_offset_links, einfuegehoehe-acc_height)    
    
    
    # ---------------------------------
    # Version section at the very bottom of the page
    # Move version section to bottom of page above footbar
    # -----------------------------------------------------
    einfuegehoehe = self.text_offset_unten + self.kleiner_abstand *4.5
    if self.sprache == 'english':
        link_text = Paragraph('<para> <span name=Helvetica color=black size = 11>\
                    <b>XXXXX 2026, Version 1.0 </b><br></br> <i>This factsheet was developed within the framework of the project\
                    “Customized and Integrated Climate Services for Improved Resilience and Sustainable\
                    Socio-Economic Development in West Africa (CICLES)”,\
                    funded by the Federal Ministry of Research, Technology and Space (BMFTR),\
                    founding number: 01LG2292A</i></span></para>',
                    self.styles['Justify'], encoding='utf8')
    else:
        link_text = Paragraph('<para> <span name=Helvetica color=black size = 11>\
                <b>xxx 2026, Version 1.0 </b><br></br> <i>Cette fiche d’information a été élaborée\
                dans le cadre du projet Customized and Integrated Climate Services for\
                Improved Resilience and Sustainable Socio-Economic Development in West Africa (CICLES) »,\
                financé par le Ministère fédéral de la Recherche, de la Technologie et de l’Espace (BMFTR),\
                numéro de financement : 01LG2292A<i></span></para>',
                self.styles['Justify'], encoding='utf8')
    link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
    
    link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height )
    