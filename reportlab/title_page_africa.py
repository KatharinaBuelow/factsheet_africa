#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
'''
import numpy
from reportlab.lib.units import mm, inch, cm
from reportlab.platypus import Image, Paragraph, Table, Flowable, PageBreak, TableStyle
from reportlab.lib import colors
from reportlab.lib import utils
from skimage import img_as_float, img_as_ubyte, io
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Flowable
from reportlab.lib import colors
from utils_image import get_image
from reportlab.platypus import Table, TableStyle

def insert_title_page(self):
    # KB Achtung die 8 hängt an der organgen box, noch ändern, wenn die Boxhöhe angepasst wird
    titleheight_page1 = self.height - 8 * cm
    #logos at the top:
    # gerics
    einfuegehoehe = self.height - 0.2 * cm    
    map_image = get_image(self.gerics_logo, height = 1.5*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links , einfuegehoehe - map_image.drawHeight)
    # bmbf
    einfuegehoehe = self.height - 0.2 * cm
    map_image = get_image(self.bmbf_logo, height = 1.9*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +7 *cm, einfuegehoehe - map_image.drawHeight)
    # wascal
    einfuegehoehe = self.height - 0.2 * cm
    map_image = get_image(self.wascal_logo, height = 1.6*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +16 *cm, einfuegehoehe - map_image.drawHeight)
        
    # Orange block (title_pic)
    self.draw_orange_box_with_text(100, 600, 250, 9*cm)
    
    # Country map
    einfuegehoehe_map = self.height - 6 * cm
    map_image = get_image(self.title_image, height = 7*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links +11.6 *cm, einfuegehoehe_map - map_image.drawHeight)

    # Technical introduction
    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))

    if self.sprache == 'english':
        abstract = Paragraph("<span name=Helvetica color=black size="+str(self.schrift_fliesstext)+">"
                             "The Regional Climate Factsheet summarizes possible climate developments "
                             "for "+self.region+" throughout the 21st century. "
                             "It is based on results from %s regional climate model simulations that use two Representative "
                             "Concentration Pathways (RCPs): RCP8.5, a high-emission scenario, and RCP2.6, a low-emission scenario. "
                             "The factsheet presents 11 key climate parameters relevant for different sectors of society. "
                             "It also highlights the likelihood of certain co-occurring extreme events and "
                             "includes expert assessments of how reliable the projected changes are.</span>"
                             , styles['Justify'], encoding='utf8')
    else:
        abstract = Paragraph("<span name=Helvetica color=black size="+str(self.schrift_fliesstext)+
                             ">La fiche climatique régionale présente les évolutions climatiques possibles pour "+self.region+" "
                             "au cours du XXIe siècle. Elle repose sur les résultats de %s simulations réalisées à "
                             "l'aide de modèles climatiques régionaux utilisant deux trajectoires représentatives de "
                             "concentration (RCP) : le RCP8.5, un scénario à fortes émissions, et le RCP2.6, un scénario "
                             "à faibles émissions. La fiche présente 11 paramètres climatiques clés pertinents pour différents "
                             "secteurs de la société. Elle met également en évidence la probabilité de certains événements extrêmes "
                             "concomitants et inclut des évaluations d'experts sur la fiabilité des changements projetésDas Regional. </span>",
                             styles['Justify'], encoding='utf8')
                             
    abstract_width, abstract_height = \
        abstract.wrapOn(self.c, self.width - self.text_offset_rechts - self.text_offset_links - 5.8*cm, self.height)
    abstract.drawOn(self.c, 
                    self.text_offset_links, titleheight_page1 - self.kleiner_abstand - abstract_height)
    
    # Distance for next element: 
    offsettop = titleheight_page1 - self.kleiner_abstand *1.5 - abstract_height #- self.kleiner_abstand
    
    # Introduction to country-specific context and key messages
    if self.sprache == 'english':
        print('english')

        if self.region == 'Burkina Faso':
            col1_text = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>'
            + self.region + ' is a central West African country whose economy '
            'relies heavily on natural resources, including rain-fed agriculture '
            'and livestock (World Bank Group, 2021). Its flat landscape is drained '
            "by three major river basins which store all the country's surface water. "
            'The tropical climate is shaped by the Intertropical Convergence Zone (ITCZ) '
            'and Harmattan winds, resulting in a long, hot dry season (October–May) '
            'and a short rainy season (June–September). Notably, rainfall follows a strict '
            'north-south gradient, dividing the country into three distinct climatic zones: '
            'the arid Sahelian zone, the transitional Sudano-Sahelian zone and the humid '
            'Sudanian zone. Ultimately, this gradient determines ecological viability and '
            'shapes the distribution of farming systems (Zongo et al., 2015). In recent '
            'years, the country faces extreme weather events, including flooding in 2009, '
            'heatwaves in 2023, and windstorms that severely impact farmers and their livelihoods '
            '(USAID; 2017).</span>', styles['Justify']
            )
        elif self.region == 'Togo':
            col1_text = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>'
            + self.region + ' is a coastal country in West Africa, located along the Gulf of Guinea. '
            'The terrain ranges from gently rolling savannah in the north, to a hilly central region, '
            'to a southern plateau meeting the coastal plain. With a humid tropical climate in the '
            'south and a semi-arid north, the country is facing critical challenges at the '
            'intersection of climate change and water security, driven by increasing rainfall '
            'variability and rising temperatures. National assessments reveal that substantial '
            'infrastructure deficiencies pose a major risk to the long-term availability of '
            'water (IMF, 2025). The capital, Lomé, is becoming increasingly vulnerable to flooding '
            'and saltwater intrusion into shallow aquifers, threats which are being exacerbated '
            'by rising sea levels (World Bank, 2025). Consequently, current strategic frameworks '
            'prioritise the rehabilitation of hydrological monitoring systems and enhanced '
            'transboundary cooperation in the Mono River basin to build resilience against '
            'extreme climatic events (Adaptation Fund, 2022).</span>', styles['Justify']
            )
        elif self.region == 'Ivory Coast':
            col1_text = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>'
            'The landscape transitions from dense tropical forests and coastal lagoons in the south to drier, '
            'rolling savannah in the north. With a humid equatorial climate in the south and a semi-arid climate '
            'in the north, the country is facing critical health challenges at the intersection of climate change '
            'and disease dynamics. These are driven by intense rainy seasons and rising average temperatures. '
            'The southern as well as the northern parts of the country are increasingly vulnerable to the resurgence '
            'of waterborne diseases such as cholera and vector-borne diseases such as malaria due to rising sea levels, '
            'temperature, and intense rainfall which create a conducive environment (CGA, 2025). </span>', styles['Justify']
            )
        else:
            col1_text = (
            self.region +' is located in Africa.'
        )
    else:
        print('french')
        if self.region == 'Burkina Faso':
            col1_text = Paragraph('<span name=Helvetica color=black size='+str(self.schrift_fliesstext)+'>'
            + self.region + ' est un pays d’Afrique de l’Ouest dont l’économie dépend fortement des ressources naturelles, '
            'notamment l’agriculture pluviale et l’élevage (Groupe de la Banque mondiale, 2021). Son paysage plat est drainé '
            "par trois grands bassins fluviaux qui stockent toute l'eau de surface du pays. Le climat tropical est "
            "façonné par la zone de convergence intertropicale (ZCIT) et les vents d'Harmattan, ce qui entraîne une "
            "longue saison sèche chaude (octobre-mai) et une courte saison des pluies (juin-septembre). Notamment, "
            "les précipitations suivent un gradient strict nord-sud, divisant le pays en trois zones climatiques distinctes : "
            "la zone sahélienne aride, la zone soudano-sahélienne transitoire et la zone soudanienne humide. En fin de compte, "
            "ce gradient détermine la viabilité écologique et façonne la répartition des systèmes agricoles (Zongo et al., 2015). "
            "Ces dernières années, le pays est confronté à des événements météorologiques extrêmes, notamment des inondations en 2009, "
            "des vagues de chaleur en 2023 et des tempêtes de vent qui ont un impact sévère sur les agriculteurs et leurs moyens de subsistance "
            "(USAID ; 2017).</span>", styles['Justify']
            )
        elif self.region == 'Togo':
            col1_text = Paragraph("<span name=Helvetica color=black size="+str(self.schrift_fliesstext)+">"
            "Le " + self.region + " est un pays côtier d'Afrique de l'Ouest situé le long du golfe de Guinée. "
            "Le relief s'étend des savanes légèrement vallonnées du nord à une région centrale plus montagneuse, "
            "puis à un plateau méridional rejoignant la plaine côtière. Avec un climat tropical humide au sud "
            "et un climat semi-aride au nord, le pays est confronté à des défis majeurs à l'intersection du "
            "changement climatique et de la sécurité hydrique, sous l'effet d'une variabilité croissante des "
            "précipitations et de la hausse des températures. Les évaluations nationales montrent que "
            "d'importantes insuffisances en matière d'infrastructures constituent un risque majeur "
            "pour la disponibilité à long terme des ressources en eau (FMI, 2025). La capitale, Lomé, "
            "est de plus en plus vulnérable aux inondations et à l'intrusion d'eau salée dans les aquifères "
            "peu profonds, des menaces aggravées par l'élévation du niveau de la mer (Banque mondiale, 2025). "
            "En conséquence, les cadres stratégiques actuels accordent la priorité à la réhabilitation "
            "des systèmes de suivi hydrologique et au renforcement de la coopération transfrontalière "
            "dans le bassin du Mono afin d'accroître la résilience face aux événements climatiques "
            "extrêmes (Fonds d’adaptation, 2022).</span>", styles['Justify']
            )
        elif self.region == 'Côte d’Ivoire':
            col1_text = Paragraph("<span name=Helvetica color=black size="+str(self.schrift_fliesstext)+">"
            "Le paysage passe de forêts tropicales denses et de lagunes côtières au sud à des savanes plus sèches "
            "et vallonnées au nord. Avec un climat équatorial humide au sud et un climat semi-aride au nord, "
            "le pays est confronté à des défis sanitaires majeurs à l'intersection du changement climatique "
            "et de la dynamique des maladies. Ceux-ci sont alimentés par des saisons des pluies intenses et "
            "une augmentation des températures moyennes. Les parties sud et nord du pays sont de plus en plus "
            "vulnérables à la résurgence de maladies hydriques telles que le choléra et de maladies vectorielles "
            "telles que le paludisme en raison de l'élévation du niveau de la mer, de la température et des "
            "précipitations intenses qui créent un environnement propice (CGA, 2025).</span>", styles['Justify']
            )
        else:
            col1_text = (
            self.region +' est situé en Afrique.'
        )       
            
    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))

    total_width = self.width - self.text_offset_links - self.text_offset_rechts #- 0.5*cm
    textbox_y = offsettop - abstract_height - self.kleiner_abstand 
    if isinstance(col1_text, Paragraph):
        p1 = col1_text
    else:
        p1 = Paragraph(col1_text, styles['Justify'])
    p1.wrapOn(self.c, total_width, self.height)
    p1.drawOn(self.c, self.text_offset_links, textbox_y)
             
    # Distance for next element: 
    offsettop = offsettop - textbox_y - self.kleiner_abstand*1.5

    # draw plot left and caption of figure right at the bottom of the page, 
    # Text to figure 1 (ERA5 anomalies)
    if self.sprache == 'english':
        col2_text = (
        '<b>Figure 1</b> shows annual temperature and precipitation anomalies '
        'for '+self.region+' from 1941–2023 based on ERA5 reanalysis data. The anomalies are calculated relative to the mean of the '
        '1991–2020 reference period, which is indicated by the vertical dashed lines. '
        'Temperatures show a clear long-term warming trend, with mostly positive anomalies since the 2000s. '
        'Precipitation varies strongly: early decades were wetter, the 1980s drought is distinct, '
        'and recent years show mixed patterns. Data source: ERA5 global reanalysis (Hersbach et al., 2020).'
    )   
    else:
        col2_text = (
        '<b>Figure 1</b> montre les anomalies annuelles de température et de précipitations '
        'pour '+self.region+' de 1941 à 2023, basées sur les données de réanalyse ERA5. Les anomalies sont calculées par rapport à la moyenne de la '
        'période de référence 1991–2020, indiquée par les lignes pointillées verticales. '
        'Les températures montrent une tendance claire au réchauffement à long terme, avec principalement des anomalies positives depuis les années 2000. '
        'Les précipitations varient fortement : les premières décennies étaient plus humides, la sécheresse des années 1980 est distincte, '
        'et les années récentes montrent des schémas mixtes. Source des données : réanalyse globale ERA5 (Hersbach et al., 2020).'
    )
    
    col2_text = '<para><span name=Helvetica color=black size='+str(self.schrift_caption)+'>'+col2_text+'</span></para>'

    # Annual anomaly for precipitation and Temperature
    
    map_image = get_image(self.box_era5, height = 10*cm)
    map_image.wrapOn(self.c, self.width, self.height)
    # Place image so its bottom aligns with self.text_offset_unten
    img_y = self.text_offset_unten -0.2 * cm
    map_image.drawOn(self.c, self.text_offset_links, img_y)
    # Place col2_text right beside the box_era5 at the same height as the top of era5 box
    col2_width = self.width - self.text_offset_links - self.text_offset_rechts - map_image.drawWidth - 1*cm
    col2_x = self.text_offset_links + map_image.drawWidth + 0.5*cm
    col2_y = img_y + map_image.drawHeight  # Top of era5 box

    p2 = Paragraph(col2_text, styles['Justify'])
    p2_width, p2_height = p2.wrap(col2_width, self.height)
    p2.drawOn(self.c, col2_x, col2_y - p2_height)

   

    


    
