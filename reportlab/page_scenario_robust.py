from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.units import cm
from utils_image import get_image
from reportlab.lib import utils


def insert_page_explain(self):
    """
    Create a page with explaining scenarios rcp2.6, rcp8.5 and explaining robustness.
    """
    einfuegehoehe_top = self.height - 2 * cm
    
    title_text = "CLIMATE PROJECTIONS AND SCENARIOS" if self.sprache == 'english' else "FRENCH"
    title_h = self.draw_header(title_text, einfuegehoehe_top)

    # Reduce spacing between title and summary
    einfuegehoehe = einfuegehoehe_top - title_h - self.kleiner_abstand
    
    styles = getSampleStyleSheet()
    if 'Justify' not in styles.byName:
        styles.add(ParagraphStyle(name='Justify', parent=styles['Normal'], alignment=TA_JUSTIFY))
    if 'LeftAlign' not in styles.byName:
        styles.add(ParagraphStyle(name='LeftAlign', parent=styles['Normal'], alignment=TA_LEFT))
    if 'BulletHang' not in styles.byName:
        styles.add(ParagraphStyle(
            name='BulletHang',
            parent=styles['LeftAlign'],
            leftIndent=12,
            firstLineIndent=-10,
            spaceBefore=0,
            spaceAfter=2,
        ))
    if 'DefAfterBullet' not in styles.byName:
        styles.add(ParagraphStyle(
            name='DefAfterBullet',
            parent=styles['LeftAlign'],
            leftIndent=36,
            firstLineIndent=-36,
            spaceBefore=0,
            spaceAfter=2,
        ))
    if self.sprache == 'english':
        rcptext = (
        "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
        "With climate models, projections for the future climate can be calculated. "
        "Different assumptions for "
        "example about population growth, technological progress, or economic performance lead "
        "to different pathways for emissions and greenhouse gas concentrations. "
        "Such scenarios are not predictions; instead, they describe various plausible future developments. "
        "</span></para>"
        ) 
        #,self.styles['Justify'])
    else:
        rcptext =(
        "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
        "FRENCH.</span></para>"
        )
        #,self.styles['Justify'])    

    #rcps figure is missing, figure need to get defined same as for figure box_era5
    map_image = get_image(self.rcp_image, height = 6*cm)
    
    map_image.wrapOn(self.c, self.width, self.height)
    map_image.drawOn(self.c, self.text_offset_links, einfuegehoehe - map_image.drawHeight)#- self.kleiner_abstand)

    # Draw the caption below the RCP image
    rcp_figure_caption = Paragraph(
        '<span name=Helvetica color=grey size=10>* Data source: <link href="http://www.pik-potsdam.de/~mmalte/rcps/index.htm">http://www.pik-potsdam.de/~mmalte/rcps/index.htm</link></span>',
        style=styles['Justify']
    )
    _, caption_height = rcp_figure_caption.wrap(self.width, self.height)
    rcp_figure_caption.drawOn(
        self.c,
        self.text_offset_links,
        einfuegehoehe - map_image.drawHeight - caption_height
    )


    col2_width = self.width - self.text_offset_links - self.text_offset_rechts - map_image.drawWidth - 0.2*cm
    col2_x = self.text_offset_links + map_image.drawWidth + 0.2*cm
    

    rcptext_para = Paragraph(rcptext, style=styles['Justify'])
    _, p2_height = rcptext_para.wrap(col2_width, self.height)
    rcptext_para.drawOn(self.c, col2_x, einfuegehoehe - p2_height) #- self.kleiner_abstand)

    einfuegehoehe = einfuegehoehe - map_image.drawHeight - self.kleiner_abstand*0.8

    if self.sprache == 'english':
        text2 = Paragraph(
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "Climate models are then used to simulate the impacts of these emissions and "
            "the resulting changes in the composition of the atmosphere on the "
            "Earth's climate system. <br />"
            "In the Fifth IPCC Assessment Report, the Representative Concentration Pathways (RCPs) "
            "were used as scenarios. Two of them were selected for this report: RCP8.5 and RCP2.6. "
            "RCP8.5 describes a scenario with continued high greenhouse gas emissions, leading to significant climate change "
            "at a very high level by the end of the 21st century. The climate protection scenario, "
            "RCP2.6, involves very ambitious measures to reduce greenhouse gas emissions and even includes "
            "negative emissions by the end of the 21st century meaning a net "
            "removal of CO<sub rise=2 size=8>2</sub> from the atmosphere."
            "</span></para>",
            style=styles['Justify'])
    else:
        text2 = Paragraph(
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "FRENCH."
            "</span></para>",
            style=styles['Justify'])

    available_width = self.width - self.text_offset_links - self.text_offset_rechts
    para_width, para_height = text2.wrapOn(self.c, available_width, self.height)
    text2.drawOn(self.c, self.text_offset_links, einfuegehoehe - para_height) 
    einfuegehoehe = einfuegehoehe - para_height - self.kleiner_abstand

 ###########################################################################
 # Part 2: ROBUSTNESS OF THE PROJECTIONS
 ###########################################################################
    
    if self.sprache == 'english':
        tit2 = 'ROBUSTNESS OF THE PROJECTIONS'
    else:
        tit2 = 'FRENCH'
    title2_y = einfuegehoehe - self.kleiner_abstand
    if 'Header14BoldOrange' not in self.styles.byName:
        self.styles.add(ParagraphStyle(
            name='Header14BoldOrange',
            parent=self.styles['Header14Bold'],
            textColor=self.cs_orange,
        ))
    title2_para = Paragraph(tit2, self.styles['Header14BoldOrange'])
    _, title2_h = title2_para.wrapOn(
        self.c,
        self.width - self.text_offset_links - self.text_offset_rechts,
        self.height,
    )
    title2_para.drawOn(self.c, self.text_offset_links, title2_y - title2_h)
    
    # Reduce spacing between title and summary
    einfuegehoehe = title2_y - title2_h - self.kleiner_abstand

    robust_width = self.width - self.text_offset_links - self.text_offset_rechts
    if self.sprache == 'english':
        intro3 = Paragraph(
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "Climatic differences from one time period to the next are shaped by two causes: "
            "Natural year-to-year variability. Because weather is subject to constant chaotic fluctuations, "
            "climatic variables are never identical across different time periods, even in the absence of climate change. "
            "The long-term, systematic influence of external factors, such as the emission of greenhouse gases."
            "</span></para>",
            style=styles['Justify'])
        _, intro_h = intro3.wrapOn(self.c, robust_width, self.height)
        intro3.drawOn(self.c, self.text_offset_links, einfuegehoehe - intro_h)
        einfuegehoehe = einfuegehoehe - intro_h - self.kleiner_abstand *0.5

        text3 = Paragraph(
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "To statistically assess whether differences in a climatic variable have such a systematic cause or "
            "can be explained by short-term, random fluctuations, statistical significance is calculated for "
            "each simulation. We define a climate change as significant if, according to a so-called Mann–Whitney U test, "
            "it can be explained by random fluctuations with a probability of less than 5%."
            "</span></para>",
            style=styles['Justify'])
        _, hoehe = text3.wrapOn(self.c, robust_width, self.height)
        text3.drawOn(self.c, self.text_offset_links, einfuegehoehe - hoehe)
        einfuegehoehe = einfuegehoehe - hoehe - self.kleiner_abstand * 0.5

        robust_def = Paragraph(
            "<span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>Robust:</b> We assumed that an ensemble depicts a robust increase "
            "if at least 2/3 of the climate projections show an increase and at "
            "least 1/2 of the climate projections show a significant increase. "
            "The definition of a robust decrease is analogous."
            "</span>",
            style=styles['DefAfterBullet'])
        _, rd_h = robust_def.wrapOn(self.c, robust_width, self.height)
        robust_def.drawOn(self.c, self.text_offset_links, einfuegehoehe - rd_h)
        einfuegehoehe = einfuegehoehe - rd_h - self.kleiner_abstand * 0.5

        tendency_def = Paragraph(
            "<span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>Tendency:</b> We assumed that an ensemble depicts a tendency for an "
            "increase if at least 2/3 of the climate projections show an increase, "
            "but fewer than 1/2 of the climate projections show a significant increase. "
            "The definition of a tendency for decrease is analogous."
            "</span>",
            style=styles['DefAfterBullet'])
        _, td_h = tendency_def.wrapOn(self.c, robust_width, self.height)
        tendency_def.drawOn(self.c, self.text_offset_links, einfuegehoehe - td_h)
        einfuegehoehe = einfuegehoehe - td_h - self.kleiner_abstand * 0.5

        unclear_def = Paragraph(
            "<span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>Unclear:</b> No 2/3 majority exists regarding the direction of change, "
            "but at least 1/2 of the projections show a significant change."
            "</span>",
            style=styles['DefAfterBullet'])
        _, ud_h = unclear_def.wrapOn(self.c, robust_width, self.height)
        unclear_def.drawOn(self.c, self.text_offset_links, einfuegehoehe - ud_h)
        einfuegehoehe = einfuegehoehe - ud_h - self.kleiner_abstand * 0.5

        none_def = Paragraph(
            "<span name=Helvetica size="+str(self.schrift_fliesstext)+">"
            "<b>None:</b> No 2/3 majority exists regarding the direction of change, "
            "and fewer than 1/2 of the projections show a significant change."
            "</span>",
            style=styles['DefAfterBullet'])
        _, nd_h = none_def.wrapOn(self.c, robust_width, self.height)
        none_def.drawOn(self.c, self.text_offset_links, einfuegehoehe - nd_h)
        einfuegehoehe = einfuegehoehe - nd_h - self.kleiner_abstand * 0.5

    else:
        text3 = Paragraph(
            "<para><span name=Helvetica size="+str(self.schrift_fliesstext)+">"
                'Klimatische Unterschiede von einem Zeitraum zum anderen werden durch zwei Ursachen gepr\u00e4gt: <br />'
                '1. Natürliche Jahr-zu-Jahr-Variabilität. Da das Wetter ständigen chaotischen Schwankungen unterliegt, sind klimatische Variablen auch ohne Klimawandel nie in verschiedenen Zeiträumen identisch. <br />'
                '2. Der langfristige systematische Einfluss externer Faktoren, wie z.B. die Emission von Treibhausgasen. <br />'
                'Um statistisch zu beurteilen, ob Unterschiede in einer klimatischen Variable eine solche systematische Ursache haben oder durch kurzfristige, zuf\u00e4llige Schwankungen erkl\u00e4rt werden k\u00f6nnen, wird f\u00fcr jede Simulation die statistische Signifikanz berechnet. Wir definieren eine Klimaver\u00e4nderung als signifikant, wenn sie laut eines sogenannten Mann-Whitney-U-Tests mit einer Wahrscheinlichkeit von weniger als 5% durch zuf\u00e4llige Schwankungen erkl\u00e4rt werden kann. Alle Indikatoren sowie ihre projizierten Ver\u00e4nderungen werden auf die erste oder zweite Dezimalstelle gerundet.',
                 "</span></para>",
                 style=styles['Justify'])
        _, hoehe = text3.wrapOn(self.c, robust_width, self.height)
        text3.drawOn(self.c, self.text_offset_links, einfuegehoehe - hoehe)

    return
 
 


