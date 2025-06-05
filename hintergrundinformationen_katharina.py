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
from six import string_types
from netCDF4 import Dataset
import re
import pandas as pd

def insert_datasource_disclaimer_acknowledgement(self):
        if self.sprache == 'english':
            head_14 = self.add_headline(colors.Color(t_title_orange[0] / 255., t_title_orange[1] /255. , t_title_orange[2] / 255., 1),
                ' ', 'Background information',)
        else:
            head_14 = self.add_headline(colors.Color(t_title_orange[0] / 255., t_title_orange[1] /255. , t_title_orange[2] / 255., 1),
                ' ', 'Hintergrundinformationen',)
# ------------ Fusszeile Seite 5
        foot_19 = self.add_footline('ungerade_odd')

        einfuegehoehe = self.height - 3.5*cm
        self.c.setFont('Helvetica-Bold', 12)
        self.c.setFillColor(cs_schwarz)
        if self.region_type == 'Bundesland':
            reg_insert = 'des Bundeslandes'
        elif self.region_type == 'Landkreis':
            if self.modus == 'single':
                if self.region_wen in ('Hamburg', 'Berlin'):
                    reg_insert = 'von'
                else:
                    reg_insert = 'des Landkreises'
            elif self.modus == 'region':
                if self.region_wen.startswith('Landkreis '):
                    reg_insert = ''
                else:
                    reg_insert = 'von '
        elif self.region_type == 'Stadt':
            reg_insert = 'der kreisfreien Stadt'
        elif self.region_type == 'other':
            reg_insert = 'von'
        else:
            reg_insert = 'der Region'
        self.c.setFont('Helvetica-Bold', 10)
        self.c.setFillColor(cs_schwarz)
        if self.sprache == 'english':
            self.c.drawString(text_offset_links, einfuegehoehe,
                          "Data sources for the information on observed climate")
        else:
            self.c.drawString(text_offset_links, einfuegehoehe,
                          "Datengrundlage")
        if self.sprache == 'english':
            text_daten = Paragraph('<para> <span name=Helvetica color=black size = 8> Information about the present and past climate are based on the E-OBS v29.0 dataset the EU-FP6 project UERRA (http://www.uerra.eu) \
                and the Copernicus Climate Change Service, and the data providers in the ECA&D project (https://www.ecad.eu).\
                Peer-reviewed article about the dataset: Cornes, R., G. van der Schrier, E.J.M. van den Besselaar, and P.D.\
                Jones. 2018: An Ensemble Version of the E-OBS Temperature and Precipitation Datasets, J. Geophys.\
                Res. Atmos., 123. doi:10.1029/2017JD028200</span></para>', self.styles['Justify'], encoding='utf8')
        else:
            text_daten = Paragraph('<para> <span name=Helvetica color=black size = 8> Informationen zum heutigen und \
                vergangenen Klima basieren auf Daten des E-OBS v29.0 Datensatzes aus dem EU-FP6-Projekt UERRA\
                (http://www.uerra.eu) und dem Copernicus Climate Change Service sowie den Datenanbietern im ECA&D-Projekt\ (https://www.ecad.eu).<br></br> Fachartikel zum Datensatz: Cornes, R., G. van der Schrier, E.J.M. van den\
                Besselaar, and P.D. Jones. 2018: An Ensemble Version of the E-OBS Temperature and Precipitation Datasets,\
                J. Geophys. Res. Atmos., 123. doi:10.1029/2017JD028200.</span></para>', self.styles['Justify'], encoding='utf8')

        t1width, t1height = text_daten.wrapOn(self.c, self.width - text_offset_links - text_offset_rechts, self.height)
        text_daten.drawOn(self.c, text_offset_links, einfuegehoehe - abstand_zu_subtitle + self.kleiner_abstand
                           -  t1height)
        anzahl_simulationen_gesamt = str(len(self.sims_dict_rcp85.keys()) +\
                                 len(self.sims_dict_rcp45.keys()) +\
                                 len(self.sims_dict_rcp26.keys()))

        anzahl_simulationen_rcp85 = str(len(self.sims_dict_rcp85.keys()))
        anzahl_simulationen_rcp45 = str(len(self.sims_dict_rcp45.keys()))
        anzahl_simulationen_rcp26 = str(len(self.sims_dict_rcp26.keys()))
        gcms = []
        rcms = []
        for line in self.sims_dict_rcp85.items():
            gcms.append(line[1][0])
            rcms.append(line[1][1])
        for line in self.sims_dict_rcp45.items():
            gcms.append(line[1][0])
            rcms.append(line[1][1])
        for line in self.sims_dict_rcp26.items():
            gcms.append(line[1][0])
            rcms.append(line[1][1])
        #print(numpy.unique(numpy.array(gcms)))
        number_RCMs = replace_number_by_literal(len(numpy.unique(numpy.array(rcms))), sprache = self.sprache)
        number_GCMs = replace_number_by_literal(len(numpy.unique(numpy.array(gcms))), sprache = self.sprache)
        replace_number_by_literal
        self.c.setFont('Helvetica-Bold', 10)
        self.c.setFillColor(cs_schwarz)
        if self.sprache == 'english':
            hedd = "Data sources for the climate projections"
        else:
            hedd = "Datengrundlage für Klimaprojektionen"
        #self.c.drawString(text_offset_links, einfuegehoehe - (2.*abstand_zu_subtitle) -  kleiner_abstand - t1height, hedd)
        if self.region.startswith('Stadtkreis '):
            reg_insert = 'im'
            bl_artikel1 = 'Der '
            bl_praep = ''
        elif self.region.startswith('kreisfreie '):
            reg_insert = 'in der'
            bl_artikel1 = ''
            bl_praep = ' '
        else:
            reg_insert = 'im Landkreis'
            bl_artikel1 = 'Der Landkreis '
            bl_praep = 'den '
        if self.sprache == 'english':
            text_daten2 = Paragraph('<para> <span name=Helvetica color=black size = 8> The projected climate changes presented in this\
                Regional Climate Fact Sheet are based on regional climate projections, which are presented in the framework of the EURO-CORDEX\
                initiative (</span><span name=Helvetica color=blue size = 8><link href="http://www.euro-cordex.net">http://www.euro-cordex.net.</link></span><span name=Helvetica color=black size = 8>)\
                The EURO-CORDEX simulations are available on a grid with a spatial horizontal resolution of 12.5 km x 12.5 km. The climate change signals for the different\
                variables presented in this regional climate fact sheet are calculated as the mean value for all grid cells located in this region. \
                The climate projections in this fact sheet are based on the Representative Concentration Pathways (RCPs), of which the RCP8.5 represents a high emission scenario and RCP2.6 a low emission scenario. '+anzahl_simulationen_gesamt+' climate projections were obtained in May 2020 from the ESGF data portal via the data node at the German\
                Climate Computing Centre (</span><span name=Helvetica color=blue size = 8>\
                <link href="https://esgf-data.dkrz.de">https://esgf-data.dkrz.de</link></span><span name=Helvetica color=black size = 8> ). Of these, '+str(len(self.sims_dict_rcp26.keys()))+' simulations for the low emission scenario (RCP2.6), '+str(len(self.sims_dict_rcp45.keys()))+'\
                simulations for the medium emission (RCP4.5) and  '+str(len(self.sims_dict_rcp85.keys()))+' simulations\
                for the high emission scenario (RCP8.5) are available. The table on the following page provides an overview of the regional climate models\
                and their respective global forcing data. More Information about the RCP scenarios in: <br />\
                M. Meinshausen, S. Smith et al. "The RCP greenhouse gas concentrations and their extension from 1765 to 2500" (2011), Climate Change, Special RCP Issue. <br />\
                </span></para>', self.styles['Justify'], encoding='utf8')
        else:
            if self.modus == 'single':
                text_daten2 = Paragraph('<para> <span name=Helvetica color=black size = 8> Die projizierten\
                Klimaänderungen, die im Klimaausblick für %s %s präsentiert werden, basieren auf regionalen Klimaprojektionen, die im Rahmen der\
                EURO-CORDEX-Initiative\
                (</span><span name=Helvetica color=blue size = 8><link href="http://www.euro-cordex.net">http://www.euro-cordex.net</link></span><span name=Helvetica color=black size = 8>)\
                erstellt wurden.\
                Die EURO-CORDEX Simulationen liegen auf einem Gitter mit einer räumlichen horizontalen Auflösung von 12,5 km x 12,5 km vor.\
                Die Klimaprojektionen im Klimaausblick basieren auf den „Representative Concentration Pathways" (RCPs). RCP8.5 repräsentiert ein Szenario mit hohen Emissionen,\
                RCP4.5 ein Szenario mit mittleren Emissionen und RCP2.6 ein Szenario mit niedrigen Emissionen. %s Klimaprojektionen wurden bis  %s\
                aus dem ESGF-Datenportal über den Datenknoten am Deutschen Klimarechenzentrum \
                (</span><span name=Helvetica color=blue size = 8><link href="https://esgf-data.dkrz.de">https://esgf-data.dkrz.de</link></span><span name=Helvetica color=black size = 8>)\
                heruntergeladen und analysiert.\
                Davon beziehen sich %s Simulationen auf das Szenario RCP8.5, %s Simulationen auf das Szenario RCP4.5, sowie %s auf das Szenario RCP2.6.\
                Für alle drei Szenarien wurden die Simulationen mit %s\
                verschiedenen regionalen Klimamodellen (RCMs) erstellt. Die Antriebsdaten für diese %s RCMs kamen von %s verschiedenen Simulationen verschiedener globaler Klimamodelle\
                (GCMs). Eine Übersicht über die regionalen Klimamodelle und deren jeweilige globale Antriebsdaten gibt die Tabelle auf der folgenden Seite. <br />\
                Die Berechnung der Mehrzahl der Indizes basiert auf den Definitionen des „CCl/CLIVAR/JCOMM Expert Team (ET) on Climate Change Detection and Indices (ETCCDI)",\
                sowie auf der Veröffentlichung von Sillmann et al: <br />\
                Sillmann, J.; Kharin, V. V.; Zhang, X.; Zwiers, F. W. & Bronaugh, 2013. Climate extremes indices in the CMIP5 multi-model ensemble: Part 1.\
                Model evaluation in the present climate. Journal of Geophysical Research Atmospheres, 2013, 118, 1716-1733.</span></para>' % (bl_praep, self.region_wen,
                 anzahl_simulationen_gesamt,
                self.Zeitstempel_Daten, anzahl_simulationen_rcp85, anzahl_simulationen_rcp45, anzahl_simulationen_rcp26, str(number_RCMs), str(number_RCMs), str(number_GCMs)), self.styles['Justify'], encoding='utf8')
            elif self.modus == 'region':
                text_daten2 = Paragraph('<para> <span name=Helvetica color=black size = 8> Die projizierten\
                    Klimaänderungen, die im Klimaausblick für %s %s präsentiert werden, basieren auf regionalen Klimaprojektionen, die im Rahmen der EURO-CORDEX Initiative\
                    (</span><span name=Helvetica color=blue size = 8><link href="http://www.euro-cordex.net">http://www.euro-cordex.net</link></span><span name=Helvetica color=black size = 8>)\
                    erstellt wurden.\
                    Die EURO-CORDEX Simulationen liegen auf einem Gitter mit einer räumlichen horizontalen Auflösung von 12,5 km x 12,5 km vor.\
                    Die Klimaprojektionen im Klimaausblick basieren auf den „Representative Concentration Pathways" (RCPs). RCP8.5 repräsentiert ein Szenario mit hohen Emissionen,\
                    RCP4.5 ein Szenario mit mittleren Emissionen und RCP2.6 ein Szenario mit niedrigen Emissionen. %s Klimaprojektionen wurden bis  %s\
                    aus dem ESGF-Datenportal über den Datenknoten am Deutschen Klimarechenzentrum \
                    (</span><span name=Helvetica color=blue size = 8><link href="https://esgf-data.dkrz.de">https://esgf-data.dkrz.de</link></span><span name=Helvetica color=black size = 8>)\
                    heruntergeladen und analysiert.\
                    Davon beziehen sich %s Simulationen auf das Szenario RCP8.5, %s Simulationen auf das Szenario RCP4.5, sowie %s auf das Szenario RCP2.6.\
                    Für alle drei Szenarien wurden die Simulationen mit %s\
                    verschiedenen regionalen Klimamodellen (RCMs) erstellt. Die Antriebsdaten für diese %s RCMs kamen von Simulationen %s verschiedener globaler Klimamodelle\
                    (GCMs). Eine Übersicht über die regionalen Klimamodelle und deren jeweilige globale Antriebsdaten gibt die Tabelle auf der folgenden Seite.\
                    Die Berechnung der Mehrzahl der Kennwerte basiert auf den Definitionen des „CCl/CLIVAR/JCOMM Expert Team (ET) on Climate Change Detection and Indices (ETCCDI)",\
                    sowie auf der Veröffentlichung von Sillmann et al: <br />\
                    Sillmann, J.; Kharin, V. V.; Zhang, X.; Zwiers, F. W. & Bronaugh, 2013. Climate extremes indices in the CMIP5 multi-model ensemble: Part 1.\
                    Model evaluation in the present climate. Journal of Geophysical Research Atmospheres, 2013, 118, 1716-1733.</span></para>' % (bl_praep,
                    self.region_wen,
                    anzahl_simulationen_gesamt,
                   self.Zeitstempel_Daten, anzahl_simulationen_rcp85, anzahl_simulationen_rcp45, anzahl_simulationen_rcp26,
                   str(number_RCMs), str(number_RCMs), str(number_GCMs)), self.styles['Justify'], encoding='utf8')

        t2width, t2height = text_daten2.wrapOn(self.c, self.width - text_offset_links - text_offset_rechts, self.height)
        text_daten2.drawOn(self.c, text_offset_links, einfuegehoehe +
                          (0.5* kleiner_abstand) - (1.*abstand_zu_subtitle) - t1height - t2height)

        if self.sprache == 'english':
            text_daten3 = Paragraph('<para> <span name=Helvetica color=black size = 8> blablabla</span></para>', self.styles['Justify'], encoding='utf8')
        else:
            if self.modus == 'single':
                text_daten3 = Paragraph('<para> <span name=Helvetica color=black size = 8> Die geographischen Informationen werden vom\
                    statistische Amt der Europäischen Union (eurostat) zur Verfügung gestellt und stehen dort auf dem Datenserver zum Download\
                    zur Verfügung:<br></br> (https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics).\
                   </span></para>', self.styles['Justify'], encoding='utf8')
            elif self.modus == 'region':
                nr_regs = len(self.all_LK_names)
                ins_str = self.all_LK_names[0]
                for kk in range(1, nr_regs):
                    ins_str = ins_str + ', ' +self.all_LK_names[kk]
                text_daten3 = Paragraph('<para> <span name=Helvetica color=black size = 8>  Die geographischen Informationen werden vom \
                    Bundesamt für Kartographie und Geodäsie zur Verfügung gestellt und stehen dort auf dem Datenserver zum Download \
                    zur Verfügung (&copy; GeoBasis-DE / BKG 2021). Für Landkreise mit einer Fläche von weniger\
                    als 400 Quadratkilometern wird der Landkreis mit allen angrenzenden Landkreisen zu einer Region zusammengefasst.\
                    Dies ist nötig, da kleine Landkreise von der Modellgitterauflösung nicht ausreichend aufgelöst werden können.\
                    Für den vorliegenden Klimaausblick wurden die Klimaänderungen als gewichtetes Mittel über die folgenden Landkreise\
                    bzw. kreisfreien Städte berechnet: '+ins_str+'.\
                    </span></para>', self.styles['Justify'], encoding='utf8')

        t3width, t3height = text_daten3.wrapOn(self.c, self.width - text_offset_links - text_offset_rechts, self.height)
        text_daten3.drawOn(self.c, text_offset_links, einfuegehoehe - (1.*abstand_zu_subtitle) - t1height - t2height - t3height)

        einfuegehoehe = einfuegehoehe -  (2.*abstand_zu_subtitle) - t1height - t2height -t3height
        self.c.setFont('Helvetica-Bold', 10)
        self.c.setFillColor(cs_schwarz)
        if self.sprache == 'english':
            disc = "Disclaimer"
        else:
            disc = "Haftungsausschluss"
        if self.region == '07338':
            einfuegehoehe = einfuegehoehe + 0.5 * self.kleiner_abstand
        self.c.drawString(text_offset_links, einfuegehoehe , disc)
        if self.sprache == 'english':
            text_disclaimer = Paragraph('<para>\
                <span name=Helvetica color=black size = 8> This Regional Climate Fact Sheet was developed by Helmholtz-Zentrum hereon GmbH, Climate Service CEnter Germany (GERICS).\
                The content provided in this fact sheet and the underlying data correspond to the current state of knowledge. All data have been carefully prepared and checked by the\
                Climate Service Center Germany (GERICS). However, GERICS has only carried out part of the regional climate projections itself. All climate projections not carried out by\
                GERICS were obtained from the publicly accessible ESGF data archive. GERICS does not take over guarantee for the topicality, correctness, completeness or quality of the provided information.\
                GERICS also assumes no liability for decisions and their consequences, which are based on the use of this Regional Climate Fact Sheet. </span></para>', self.styles['Justify'], encoding='utf8')
        else:
            text_disclaimer = Paragraph('<para>\
                <span name=Helvetica color=black size = 8> Der\
                Klimaausblick für '+bl_praep + self.region_wen+ ' wurde durch das Climate Service Center Germany (GERICS), einer Einrichtung der Helmholtz-Zentrum hereon GmbH, erstellt. Die Inhalte des \
                Klimaausblicks sowie die verwendeten Daten entsprechen dem aktuellen \
                Wissensstand. Alle Daten wurden von GERICS sorgfältig\
                aufbereitet und geprüft. Das GERICS hat jedoch nur einen Bruchteil der verwendeten \
                Klimaprojektionen selbst durchgeführt. Die zusätzlich \
                verwendeten Klimaprojektionen wurden aus dem öffentlich zugänglichen ESGF-Datenarchiv \
                bezogen. GERICS übernimmt keine Gewähr für die Aktualität, Richtigkeit, Vollständigkeit\
                oder Qualität der bereitgestellten Informationen. GERICS übernimmt ebenfalls keine \
                Haftung für Entscheidungen und deren Folgen, die auf der Verwendung des Klimaausblicks beruhen.\
                </span></para>', self.styles['Justify'], encoding='utf8')

        tdcwidth, tdcheight = text_disclaimer.wrapOn(self.c, self.width - text_offset_links - text_offset_rechts, self.height)
        text_disclaimer.drawOn(self.c, text_offset_links, einfuegehoehe - tdcheight - kleiner_abstand*0.75)

        # ------------ Acknowledgements
        einfuegehoehe = einfuegehoehe - tdcheight - kleiner_abstand*0.75 - abstand_zu_subtitle
        self.c.setFont('Helvetica-Bold', 10)
        self.c.setFillColor(cs_schwarz)
        if self.sprache == 'english':
            disc = "Acknowledgements"
        else:
            disc = "Danksagungen"
        if self.region == '07338':
            einfuegehoehe = einfuegehoehe + 0.5 * self.kleiner_abstand
        self.c.drawString(text_offset_links, einfuegehoehe , disc)
        if self.sprache == 'english':
            text_acknowledgements = Paragraph('<para>\
                <span name=Helvetica color=black size = 8> We thank the working group for regional climate of the\
                World Climate Research Programme (WCRP) and the Working Group on Coupled Modelling, the former\
                CORDEX coordinating body and responsible body for CMIP5. We also thank the \
                EURO-CORDEX climate modelling groups for the creation and provision of their model results.\
                We also thank the Earth System Grid Federation-Infrastructure, an international effort\
                led by the US Department of Energy\'s Climate Model Diagnosis and Comparison Program,\
                the European Network for Earth System Modelling and other partners in the "Global Organisation for\
                Earth System SciencePortals (GO-ESSP)".\
                We thank the German Weather Service (DWD) for providing the HYRAS observation data.\
                The Climate Outlook Brandenburg, which is published in 2018 in cooperation with the Brandenburg Ministry\
                for Rural Development, Environment and Agriculture, Department Environment, Climate Protection and \
                Sustainability (MLUL) served as the basis for the present series of regional\
                climate fact sheets. </span></para>', self.styles['Justify'], encoding='utf8')
        else:
            text_acknowledgements = Paragraph('<para>\
                <span name=Helvetica color=black size = 8> Wir danken der Arbeitsgruppe für regionales Klima des\
                Weltklimaforschungsprogramms (WCRP) und der Arbeitsgruppe für gekoppelte Modellierung, dem früheren\
                Koordinationsorgan von CORDEX und verantwortlichen Gremium für CMIP5. Wir danken auch den \
                EURO-CORDEX Klimamodellierungsgruppen für die Erstellung und Bereitstellung ihrer Modellergebnisse.\
                Ebenso danken wir der Earth System Grid Federation-Infrastructure, einer internationalen Initiative\
                unter der Leitung des Programms für Klimamodelldiagnose und -vergleiche des US-Energieministeriums,\
                des Europäischen Netzwerks für Erdsystemmodellierung und anderer Partner in der „Global Organisation for\
                Earth System SciencePortals (GO-ESSP)".\
                Für die Bereitstellung des E-OBS-Datensatzes danken wir dem EU-FP6-Projekt UERRA (http://www.uerra.eu) und dem Copernicus Climate Change Service sowie den Datenanbietern im ECA&D-Projekt (https://www.ecad.eu).\
                Der Klimaausblick Brandenburg, der im Jahr 2018 in Kooperation mit der Abteilung  Umwelt,  Klimaschutz  und \
                Nachhaltigkeit des Brandenburgischen Ministeriums für Landwirtschaft, Umwelt und Klimaschutz \
                (MLUK) erstellt wurde, diente als Grundlage für die durch GERICS erstellte Serie regionaler\
                Klimaausblicke. Für den Klimaausblick auf Landkreisebene bedanken wir uns für Anregungen und \
                Feedback von der Kreisverwaltung Segeberg.</span></para>', self.styles['Justify'], encoding='utf8')

        tdcwidth, tdcheight = text_acknowledgements.wrapOn(self.c, self.width - text_offset_links - text_offset_rechts, self.height)
        text_acknowledgements.drawOn(self.c, text_offset_links, einfuegehoehe - tdcheight - self.kleiner_abstand*0.75)


def insert_simulation_list(self):
#------------------ Seitenumbruch
        self.c.showPage()
# -------Header Seite 5
        if self.sprache == 'english':
            head_14 = self.add_headline(colors.Color(t_title_orange[0] / 255., t_title_orange[1] /255. , t_title_orange[2] / 255., 1),
                ' ', 'Background information',)
        else:
            head_14 = self.add_headline(colors.Color(t_title_orange[0] / 255., t_title_orange[1] /255. , t_title_orange[2] / 255., 1),
                ' ', 'Hintergrundinformationen',)
# ------------ Fusszeile Seite 5
        foot_19 = self.add_footline('gerade_even')
        einfuegehoehe = self.height - 3.5*cm
        self.c.setFont('Helvetica-Bold', 12)
        self.c.setFillColor(cs_schwarz)
        zellenhoehe = 0.42 * cm
        if self.sprache == 'english':
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Simulation List")
        else:
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Liste der verwendeten Simulationen")

def insert_impressum(self):
#------------------ Seitenumbruch auf Impressum Seite
        self.c.showPage()
# -------Header Seite 5
#        if self.sprache == 'english':
#            head_14 = self.add_headline(colors.Color(t_title_orange[0] / 255., t_title_orange[1] /255. , t_title_orange[2] / 255., 1),
#                ' ', 'Background information',)
#        else:
#            head_14 = self.add_headline(colors.Color(t_title_orange[0] / 255., t_title_orange[1] /255. , t_title_orange[2] / 255., 1),
#                ' ', 'Hintergrundinformationen',)
# ------------ Fusszeile Seite 5
        foot_19 = self.add_footline('ungerade_odd')
        einfuegehoehe = self.height - 3.5*cm - self.kleiner_abstand
        self.c.setFont('Helvetica-Bold', 12)
        self.c.setFillColor(self.cs_schwarz)
        # -------------
        if self.sprache == 'english':
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Information, Literature and Weblinks:")
            link_text = Paragraph('<para><span name=Helvetica color=blue size = 10>\
                <link href="https://www.gerics.de/klimaausblick-landkreise">https://www.gerics.de/klimaausblick-landkreise</link></span></para>',
                self.styles['Justify'], encoding='utf8')
        else:
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Weiterführende Information, Literatur und Weblinks zum Thema unter:")
            link_text = Paragraph('<para> <span name=Helvetica color=blue size = 10>\
                <u><link href="https://www.gerics.de/klimaausblick-landkreise">https://www.gerics.de/klimaausblick-landkreise</link></u></span></para>',
                self.styles['Justify'], encoding='utf8')
        link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height - self.kleiner_abstand*0.75)
        # --------------------------------------
        einfuegehoehe = einfuegehoehe -  link_height - self.kleiner_abstand*0.75 - self.abstand_zu_subtitle
        if self.sprache == 'english':
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Authors:")
            link_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
                Dr.&nbsp;Torsten Weber, Dr.&nbsp;Katharina Bülow, Dr.&nbsp;Susanne Pfeifer | Helmholtz-Zentrum hereon GmbH, Climate Service Center Germany (GERICS)</span></para>',
                self.styles['Justify'], encoding='utf8')
        else:
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Autorinnen und Autoren:")
            link_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
                Dr.&nbsp;Torsten Weber, Dr.&nbsp;Katharina Bülow, Dr.&nbsp;Susanne Pfeifer | Helmholtz-Zentrum hereon GmbH, Climate Service Center Germany (GERICS)</span></para>',
                self.styles['Justify'], encoding='utf8')
        link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height - self.kleiner_abstand*0.75)
        # --------------------------------------
        einfuegehoehe = einfuegehoehe -  link_height - self.kleiner_abstand*0.75 - self.abstand_zu_subtitle
        if self.sprache == 'english':
            self.c.drawString(self.text_offset_links, einfuegehoehe, "LEGAL INFORMATION:")
            link_text = Paragraph('<para> <span name=Helvetica-Bold color=black size = 10>\
                Herausgeber:</span><span name=Helvetica color=black size = 10> <br></br>Helmholtz-Zentrum hereon GmbH<br></br>Climate Service Center Germany (GERICS)<br></br> Fischertwiete 1<br></br>\
                20095 Hamburg<br></br>www.climate-service-center.de<br></br>+49 (0) 40 226 338 0</span></para>',
                self.styles['Justify'], encoding='utf8')
        else:
            self.c.drawString(self.text_offset_links, einfuegehoehe, "IMPRESSUM:")
            link_text = Paragraph('<para> <span name=Helvetica-Bold color=black size = 10>\
                Herausgeber:</span><span name=Helvetica color=black size = 10> <br></br>Helmholtz-Zentrum hereon GmbH<br></br>Climate Service Center Germany (GERICS)<br></br> Fischertwiete 1<br></br>\
                20095 Hamburg<br></br>www.climate-service-center.de<br></br>+49 (0) 40 226 338 0</span></para>',
                self.styles['Justify'], encoding='utf8')
        link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height - self.kleiner_abstand*0.75)
       # ----------------------------------------
        einfuegehoehe = einfuegehoehe -  link_height - self.kleiner_abstand*0.75 - self.abstand_zu_subtitle
        #print(self.license_link)
        # if self.sprache == 'english':
        #     self.c.drawString(self.text_offset_links, einfuegehoehe, "Photograph Credits:")
        #     link_text = Paragraph('<para><span name=Helvetica color=black size = 10>\
        #         Title page: '+self.bildreferenz+'</span></para>',
        #         self.styles['Justify'], encoding='utf8')
        # else:
        #     self.c.drawString(self.text_offset_links, einfuegehoehe, "Bildnachweis:")
        #     link_text = Paragraph('<para><span name=Helvetica color=black size = 10>\
        #         Vorderseite des Berichts: <br></br>'+self.bildreferenz +'</span><span name=Helvetica color=black size = 10>\
        #              ' + self.license_link +'</span></para>',
        #         self.styles['Justify'], encoding='utf8')
        # link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        # link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height - self.kleiner_abstand*0.75)
        # --------------------------------------
        einfuegehoehe = einfuegehoehe -  link_height - self.kleiner_abstand*0.75 - self.abstand_zu_subtitle
        website_link = '<u><link href=\"' +  'https://www.gerics.de/imperia/md/assets/gerics/files/klimaausblick/gerics_klimaausblick_'+self.region+'_version_1.0_deutsch.pdf'+'">'+'https://www.gerics.de/imperia/md/assets/gerics/files/klimaausblick/gerics_klimaausblick_'+self.region+'_version_1.0_deutsch.pdf'+'</link></u>'
        website_link = '<u><link href=\"' +  'https://www.gerics.de/klimaausblick-landkreise'+'">'+'https://www.gerics.de/klimaausblick-landkreise'+'</link></u>'
        if self.sprache == 'english':
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Reference:")
            link_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
                Dr.&nbsp;Torsten Weber, Dr.&nbsp;Katharina Bülow, Dr.&nbsp;Susanne Pfeifer; Climate Factsheet '+self.region+'. August 2025, Climate Service Center Germany (GERICS), eine Einrichtung der Helmholtz-Zentrum hereon GmbH.\
                <br></br></span><span name=Helvetica color=blue size = 10>' + website_link + '<br></br> </span></para>',
                self.styles['Justify'], encoding='utf8')
        else:
            self.c.drawString(self.text_offset_links, einfuegehoehe, "Zitierhinweis:")
            link_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
                Dr.&nbsp;Torsten Weber, Dr.&nbsp;Katharina Bülow, Dr.&nbsp;Susanne Pfeifer: Climate Factsheet '+self.regions+'. Juni 2025, Climate Service Center Germany (GERICS), eine Einrichtung der Helmholtz-Zentrum hereon GmbH.\
                <br></br></span><span name=Helvetica color=blue size = 10>' + website_link + '<br></br> </span></para>',
                self.styles['Justify'], encoding='utf8')
        link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height - self.kleiner_abstand*0.75)
         # ---------------------------------
        einfuegehoehe = einfuegehoehe - link_height - self.kleiner_abstand*0.75 - self.abstand_zu_subtitle
        if self.sprache == 'english':
            link_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
                August 2025 <br></br> Version 1.0 <br></br> &copy; Climate Service Center Germany (GERICS)\
                 <br></br> Alle Rechte vorbehalten</span></para>',
                self.styles['Justify'], encoding='utf8')
        else:
            link_text = Paragraph('<para> <span name=Helvetica color=black size = 10>\
                März 2025 <br></br> Version 1.1 <br></br> &copy; Climate Service Center Germany (GERICS)\
                 <br></br> Alle Rechte vorbehalten</span></para>',
                self.styles['Justify'], encoding='utf8')
        link_width, link_height = link_text.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        link_text.drawOn(self.c, self.text_offset_links, einfuegehoehe - link_height - self.kleiner_abstand*0.75)

