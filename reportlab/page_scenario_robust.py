from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils


def insert_page_explain(self):
    """
    Create a page with explaining line plot and boxplot graphics
    for the projected evolution of mean annual temperature and mean 
    number of heat days for the specified region, based on CORDEX AFR22 regional 
    climate model realizations under RCP2.6 and RCP8.5 scenarios, 
    including ERA5 reanalysis data for comparison. The page includes a title, a 
    summary text, two graphics with captions, and is formatted for clarity and readability.
    """
    ##################################################################################

###########################################################################
def insert_hintergrundinformation_rcps(self, y_pos='', language='english'):

        #einfuegehoehe = y_pos - 0.5 * cm
        einfuegehoehe_top = self.height - 2 * cm
        
        self.c.setFont('Helvetica-Bold', 14)
        self.c.setFillColor(self.cs_orange)
        index = 0
        if language == 'english':
            tit = 'Climate Projections and Scenarios'
        else:
            tit = 'Klimaprojektionen und Szenarien'
        content1 = []
        #rcp_image = Image(self.rcp_dummy_im)
        #rcp_image = get_image(self.rcp_dummy_im, height = 5.*cm)

        figure_caption2 = Paragraph('<span name=Helvetica color=black size = 8>* Datenquelle:\
            <link href="http://www.pik-potsdam.de/~mmalte/rcps/index.htm#Download">http://www.pik-potsdam.de/~mmalte/rcps/index.htm#Download</link> </span>', style=self.styles['Justify'])
        figure_caption1 = Paragraph('<span name=Helvetica color=black size = 16>*</span>', style=self.styles['Justify'])
        figure_caption1.wrapOn(self.c, self.width, self.height)
        figure_caption2.wrapOn(self.c, self.width, self.height)

        text1 = Paragraph('<span name=Helvetica color=black size = 10>\
                Mit Klimamodellen können Projektionen für das zukünftige Klima berechnet werden. Diese liefern Antworten auf die Frage:\
                „Was wäre, wenn?“ Verschiedene Annahmen, z. B. zur Bevölkerungsentwicklung, dem technologischen Fortschritt oder der Wirtschaftsleistung,\
                führen zu verschiedenen Entwicklungspfaden von Emissionen und Konzentrationen an Treibhausgasen. Solche Szenarien sind keine Vorhersagen,\
                sondern beschreiben verschiedene plausible Entwicklungen. Mit Klimamodellen werden dann die Auswirkungen der Emissionen\
                und der damit verbundenen veränderten Zusammensetzung der Atmosphäre auf das Klimasystem der Erde simuliert. </span>', style=self.styles['Justify'])
        #content1.append((rcp_image,'', text1))
        table1 = Table(content1, colWidths=(5.0 * cm, 1.*cm, (self.width - self.text_offset_links - self.text_offset_rechts- 5.*cm - 2.5*cm + 0.1*cm)),
                       rowHeights=rcp_image.drawHeight)
        table1.setStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ])
        table1.wrapOn(self.c, self.width- self.text_offset_links - self.text_offset_rechts - 1.5*cm, self.height)

        content2 = []
        if language == 'english':
            text2 = Paragraph('<span name=Helvetica color=black size = 10>\
                Climate models can be used to calculate projections for future climate. These provide answers to the question: "What if?"\
                                      How will the climate develop under certain conditions, for example if humans emit additional greenhouse gases into the atmosphere?\
                                      To this end, emission scenarios for the 21<sup>st</sup> century are developed based on various assumptions, e.g. on the development of population, human culture,\
                                      technology and the economy. Representative Concentration Pathways" (RCPs) are widely used today. They are defined by the radiative forcing at the end of the\
                                      21<sup>st</sup> century and represent different development paths of greenhouse gas concentrations and associated emissions.\
                                      For example, the representative concentration path "RCP4.5" leads to a radiative forcing of about 4.5\u202FW/m<sup>2</sup> at the end of the 21st century.\
                                      This physical threshold value can be reached by various socio-economic developments, which also take into account climate policy measures, for example.\
                                      The concentration path of RCP2.6 includes very ambitious measures to reduce greenhouse gas emissions and even "negative emissions" by the end of the 21<sup>st</sup>\
                                      century. It leads to a radiative forcing of about 3\u202FW/m<sup>2</sup> around 2040 and then decreases to a value of 2.6\u202FW/m<sup>2</sup> towards the end of the 21<sup>st</sup> century.\
                                      RCP2.6 thus represents a path with lower emissions compared to other RCPs. RCP8.5, on the other hand, describes a continuous increase in greenhouse gas emissions,\
                                      reaching a radiative forcing of 8.5\u202FW/m<sup>2</sup> by the end of the 21st century.</span>', style=self.styles['Justify'])
        else:
            text2 = Paragraph('<span name=Helvetica color=black size = 10>Im Rahmen des fünften IPCC-Sachstandsberichts wurden die\
                    „Representative  Concentration Pathways“ (RCPs) als Szenarien verwendet. Drei davon wurden für diesen Bericht ausgewählt: RCP8.5, RCP4.5 und\
                    RCP2.6. Das Szenario RCP8.5 beschreibt einen weiterhin kontinuierlichen Anstieg der Treibhausgasemissionen mit einer Stabilisierung der\
                    Emissionen auf einem sehr hohen Niveau zum Ende des 21. Jahrhunderts. Das mittlere Szenario, RCP4.5, geht davon aus, dass die Emissionen bis\
                    zur Mitte des 21. Jahrhunderts noch etwas ansteigen und danach wieder sinken. Dieser Pfad kann durch verschiedene sozioökonomische \
                    Entwicklungen erreicht werden, die z. B. auch klimapolitische Maßnahmen berücksichtigen. Das Klimaschutz-Szenario, RCP2.6, beinhaltet sehr\
                    ambitionierte Maßnahmen zur Reduktion von  Treibhausgasemissionen und zum Ende des 21. Jahrhunderts sogar „negative Emissionen“ (eine\
                    netto-Entnahme von CO<sub rise=2 size=8>2</sub> aus der Atmosphäre).\
                    </span>', style=self.styles['Justify'])
        
        breite, hoehe = text2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 1.0 *cm, self.height)

        self.c.drawString(self.text_offset_links + 0.5 *cm, einfuegehoehe - 0.25 * cm, tit)
        back = Image(self.background)
        back.drawHeight = hoehe + rcp_image.drawHeight + 1.5 * cm + 0.25 * cm + 0.5*cm
        back.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts
        back.wrapOn(self.c, self.width, self.height)
        back.drawOn(self.c, self.text_offset_links, y_pos - back.drawHeight)
        self.c.drawString(self.text_offset_links + 0.5 *cm, einfuegehoehe - 0.25 * cm, tit)
        table1.drawOn(self.c, self.text_offset_links + 1.1*cm, einfuegehoehe - rcp_image.drawHeight - self.abstand_zu_subtitle + 0.5*cm)

        text2.wrapOn(self.c, self.width -self.text_offset_links - self.text_offset_rechts - 1.*cm, self.height)
        text2.drawOn(self.c, self.text_offset_links + 0.5*cm, einfuegehoehe - rcp_image.drawHeight -1.* self.abstand_zu_subtitle - hoehe)
#        figure_caption1.drawOn(self.c, self.text_offset_links + 1.*cm, einfuegehoehe - rcp_image.drawHeight - self.abstand_zu_subtitle + 0.5*cm)
        figure_caption1.drawOn(self.c, self.text_offset_links + 0.25*cm, einfuegehoehe - rcp_image.drawHeight - self.abstand_zu_subtitle)
        figure_caption2.drawOn(self.c, self.text_offset_links + 0.25*cm, einfuegehoehe - rcp_image.drawHeight -1.* self.abstand_zu_subtitle - hoehe - 0.65 * cm)

        return back.drawHeight




    

 ###########################################################################
def insert_leseanleitung_pfeile(self, y_pos='', language='english'):
        
        einfuegehoehe = y_pos - 0.5 * cm
        self.c.setFont('Helvetica-Bold', 14)
        self.c.setFillColor(self.cs_orange)
        index = 0
        if language == 'english':
            tit = 'Symbols of the expert judgement on the robustness of the projections'
        else:
            tit = 'Symbole der Experteneinschätzung zur Belastbarkeit der Projektionen'            
        content = []
        columnwidths = (1.*cm, (self.width - self.text_offset_links - self.text_offset_rechts - 2.*cm - 1. *cm)/2.,
                        1.*cm, (self.width - self.text_offset_links - self.text_offset_rechts - 2.*cm - 1. *cm)/2.)
        pfeil1 = Image(self.pfeil_dir + '/ryi_sy.png')
        pfeil1.drawHeight = (1.5 * cm)
        pfeil1.drawWidth = 2 / 5. * pfeil1.drawHeight
        pfeil2 = Image(self.pfeil_dir + '/ryi_sn.png')
        pfeil2.drawHeight = (1.5 * cm)
        pfeil2.drawWidth = 2 / 5. * pfeil1.drawHeight
        pfeil3 = Image(self.pfeil_dir + '/ryd_sy.png')
        pfeil3.drawHeight = (1.5 * cm)
        pfeil3.drawWidth = 2 / 5. * pfeil1.drawHeight
        pfeil4 = Image(self.pfeil_dir + '/ryd_sn.png')
        pfeil4.drawHeight = (1.5 * cm)
        pfeil4.drawWidth = 2 / 5. * pfeil1.drawHeight
        pfeil5 = Image(self.pfeil_dir + '/rn_sy.png')
        pfeil5.drawHeight = (1.5 * cm)
        pfeil5.drawWidth = 2 / 5. * pfeil1.drawHeight
        pfeil6 = Image(self.pfeil_dir + '/rn_sn.png')
        pfeil6.drawHeight = (1.5 * cm)
        pfeil6.drawWidth = 2 / 5. * pfeil1.drawHeight

        heights = [2.*cm, 2.*cm, 2.*cm ]
        if language == 'english':
            content.append((pfeil1, Paragraph('<span name=Helvetica-bold color=black size = 10>Increase: </span><span name=Helvetica color=black size = 10>The majority of the simulations projects significant increases</span>', style=self.styles['Justify']),
                        pfeil2, Paragraph('<span name=Helvetica-bold color=black size = 10>Tendency towards an increase: </span><span name=Helvetica color=black size = 10>The majority of the simulations projects non-significant increases</span>', style=self.styles['Justify'])))
            content.append((pfeil3, Paragraph('<span name=Helvetica-bold color=black size = 10>Decrease : </span><span name=Helvetica color=black size = 10>The majority of the simulations projects significant decreases</span>', style=self.styles['Justify']),
                        pfeil4, Paragraph('<span name=Helvetica-bold color=black size = 10>Tendency towards a decrease: </span><span name=Helvetica color=black size = 10>The majority of the simulations projects non-significant decreases</span>', style=self.styles['Justify'])))
            content.append((pfeil5, Paragraph('<span name=Helvetica-bold color=black size = 10>Unclear: </span><span name=Helvetica color=black size = 10>The majority of the simulations projects significant changes, but do not agree on the direction of changes</span>', style=self.styles['Justify']),
                        pfeil6, Paragraph('<span name=Helvetica-bold color=black size = 10>No changes: </span><span name=Helvetica color=black size = 10>The majority of the simulations projects non-significant changes, with no preferred direction of changes</span>', style=self.styles['Justify'])))
        else:
            content.append((pfeil1, Paragraph('<span name=Helvetica-bold color=black size = 10>Zunahme: </span><span name=Helvetica color=black size = 10>\
                Mindestens 2/3 der Simulationen zeigen eine Zunahme und mindestens 50% der Simulationen sogar eine signifikante Zunahme.</span>', style=self.styles['Justify']),
                        pfeil2, Paragraph('<span name=Helvetica-bold color=black size = 10>Tendenz zur Zunahme: </span><span name=Helvetica color=black size = 10>\
                            Mindestens 2/3 der Simulationen zeigen eine Zunahme, aber weniger als 50% der Simulationen eine signifikante Zunahme.</span>', style=self.styles['Justify'])))
            content.append((pfeil3, Paragraph('<span name=Helvetica-bold color=black size = 10>Abnahme: </span><span name=Helvetica color=black size = 10>\
                Mindestens 2/3 der Simulationen zeigen eine Abnahme und mindestens 50% der Simulationen sogar eine signifikante Abnahme. </span>', style=self.styles['Justify']),
                        pfeil4, Paragraph('<span name=Helvetica-bold color=black size = 10>Tendenz zur Abnahme: </span><span name=Helvetica color=black size = 10>\
                            Mindestens 2/3 der Simulationen zeigen eine Abnahme, aber weniger als 50% der Simulationen eine signifikante Abnahme. </span>', style=self.styles['Justify'])))
            content.append((pfeil5, Paragraph('<span name=Helvetica-bold color=black size = 10>Unklar: </span><span name=Helvetica color=black size = 10>\
                Keine 2/3-Mehrheit bezüglich der Richtung der Änderungen, aber mindestens 50% der Simulationen zeigen signifikante Änderungen.</span>', style=self.styles['Justify']),
                        pfeil6, Paragraph('<span name=Helvetica-bold color=black size = 10>Keine Änderungen: </span><span name=Helvetica color=black size = 10>\
                            Keine 2/3-Mehrheit bezüglich der Richtung der Änderungen; weniger als 50% der Simulationen zeigen signifikante Änderungen.</span>', style=self.styles['Justify'])))
            
        table = Table(content, colWidths=columnwidths, rowHeights=heights)
        table.setStyle([#("VALIGN", (0, 0), (1, 0), "TOP"),
                        ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("ALIGN", (0, 0), (0, -1), "LEFT"),
                        ("ALIGN", (1, 0), (1, -1), "LEFT"),
                        ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                        ("ALIGN", (3, 0), (3, -1), "LEFT"),
                        #("GRID", (0,0), (-1,-1), 0.25, colors.gray),
                        ('BACKGROUND', (0, 0), (-1, -1), (colors.Color(255 / 255., 255 / 255., 255 / 255., 1)))])
        table.wrapOn(self.c, self.width, self.height)
        
        content2 = []
        if language == 'english':
            text2 = Paragraph('<span name=Helvetica color=black size = 10>\
                Climatic differences from one time period to the next are due to two causes:\
                1. the natural variability from year to year. Due to the chaotic fluctuations of the weather, climate properties are never identical in different time periods,\
                even in absence of any climatic change. The result therefore always has a random component. \
                < /br> 2. the long-term, systematic influence of external factors, for example the emission of greenhouse gases.\
                In order to assess whether climatic differences have such a systematic cause or whether they are just random fluctuations, statistical significance tests are applied. \
                In this report, a climate change is labeled as significant if its chance to be a random fluctuation is below 5%, based on a Mann-Whitney-u-test.\
                Filled arrows indicate that more than half of the simulations show a significant change in the direction of the arrow (increase or decrease).<br />\
                All indices which are given in units of <it>days/year</it>, <it>days</it>, or <it>nights/year</it> are\
                rounded to full days, the other values are rounded to the first decimal place.</span>', style=self.styles['Justify'])
        else:
            text2 = Paragraph('<span name=Helvetica color=black size = 10>\
                Klimatische Unterschiede von einer Zeitperiode zur nächsten sind durch zwei Ursachen geprägt: <br /> \
                1. Natürliche Schwankungen von Jahr zu Jahr. Da das Wetter ständigen chaotischen Schwankungen unterliegt, sind auch Klimagrößen über verschiedene Zeiträume nie identisch,\
                auch ohne Klimawandel. <br /> \
                2. Der langfristige, systematische Einfluss externer Faktoren, z.B. der Ausstoß von Treibhausgasen. \
                Um statistisch zu bewerten, ob Unterschiede einer Klimagröße eine solche systematische Ursache haben oder mit kurzfristigen, zufälligen Schwankungen erklärbar sind,\
                wird für jede Simulation die statistische Signifikanz berechnet. Wir definieren eine Klimaänderung als signifikant, wenn sie gemäß eines sogenannten Mann-Whitney-U-Tests\
                mit einer Wahrscheinlichkeit von unter 5% mit zufälligen Schwankungen erklärbar ist. Farblich ausgefüllte Pfeile bedeuten, dass mehr als 50% der Simulationen eine signifikante Änderung\
                in die angegebene Richtung zeigen (Zunahme oder Abnahme).<br /> Alle Kennwerte sowie ihre projizierten Änderungen sind auf die erste bzw. zweite Dezimalstelle gerundet.</span>', style=self.styles['Justify'])
        #content2.append(('', text2))
        breite, hoehe = text2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 1.0 *cm, self.height)
        

        text2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 1.*cm, self.height)
        back = Image(self.background)
        back.drawHeight = numpy.sum(heights) + 1. * cm + hoehe + 1. * cm
        back.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts
        back.wrapOn(self.c, self.width, self.height)
        back.drawOn(self.c, self.text_offset_links, y_pos - back.drawHeight)
        self.c.drawString(self.text_offset_links + 0.5 *cm, einfuegehoehe - 0.25 * cm, tit)
        table.drawOn(self.c, self.text_offset_links + 0.5*cm, einfuegehoehe -0.75 * cm - numpy.sum(heights))
        text2.drawOn(self.c, self.text_offset_links + 0.5*cm, einfuegehoehe + 0.25 * cm- numpy.sum(heights)- hoehe - self.abstand_zu_subtitle - self.kleiner_abstand)
        #table2.drawOn(self.c, self.text_offset_links + 0.5*cm, einfuegehoehe -0.25 * cm - numpy.sum(heights)- hoehe - self.abstand_zu_subtitle - self.kleiner_abstand)
        
        return back.drawHeight


