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
def insert_leseanleitung_abbildungen(self, y_pos='', language='english'):
       # back = Image(self.background)
       # if language == 'english':
       #     back.drawHeight = self.height - 5. * cm
       # else:
       #     back.drawHeight = self.height - 5. * cm
       # back.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts
       # back.wrapOn(self.c, self.width, self.height)
       # if language == 'english':
       #     back.drawOn(self.c, self.text_offset_links, 3. * cm)
       # else:
       #     back.drawOn(self.c, self.text_offset_links, 2. * cm)
        einfuegehoehe = self.height - 3.5 * cm
        self.c.setFont('Helvetica-Bold', 14)
        self.c.setFillColor(self.cs_orange)
        index = 0
        image_height = 5.*cm
        far_future = str(self.end_year_1)+'-'+str(self.end_year_2)
        dum_im = self.path_pre_s +'/'+ self.region_nuts_in_file+ "/Klimaausblick_FD_"+self.region_nuts_in_file+"_topfigure_indexpage_deutsch_1950_2098_fill_all_range_sep_periods.png"
        dum_im2 = self.path_pre_b +'/'+self.region_nuts_in_file+ "/Klimaausblick_FD_"+self.region_nuts_in_file+"_boxplot_deutsch_seasons_YEAR_period_"+far_future+".png"
        example_figure_new = get_image(dum_im, height = image_height)
        example_figure_new.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts, self.height)
        fig_height = self.height - 3.5 * cm - example_figure_new.drawHeight
        example_figure_new.drawOn(self.c, self.text_offset_links + 0.5*cm, fig_height)

#        example_figure = Image(dum_im)
#        example_figure.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts - 6.*cm
#        example_figure.drawHeight = example_figure.drawWidth * 1800./6600.
#        #example_figure.wrapOn(self.c, self.width, self.height)
#        example_figure.drawOn(self.c, self.text_offset_links + 0.5*cm, fig_height)

        #box_figure = Image(dum_im2)
        box_figure = get_image(dum_im2, height = image_height)
#        box_figure.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts - 1.*cm - example_figure.drawWidth
#        box_figure.drawHeight = box_figure.drawWidth * 1800./6600.
        box_figure.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts -example_figure_new.drawWidth , self.height)
#        fig_height = self.height - 3.5 * cm - box_figure.drawHeight
        box_figure.drawOn(self.c, self.text_offset_links + example_figure_new.drawWidth + 1.5*cm, fig_height)
        dumnum = create_number_box_with_colored_back(self, '1', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum.wrapOn(self.c, self.width, self.height)
        dumnum.drawOn(self.c, 3.0 *cm, fig_height + 2.5* cm)
        dumnum2 = create_number_box_with_colored_back(self,'2', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum2.wrapOn(self.c, self.width, self.height)
        dumnum2.drawOn(self.c, 5.5 *cm, fig_height - 0.5* cm)
        dumnum3 = create_number_box_with_colored_back(self,'3', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum3.wrapOn(self.c, self.width, self.height)
        dumnum3.drawOn(self.c, 6. *cm, fig_height + 1.0* cm)
        dumnum4 = create_number_box_with_colored_back(self,'4', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum4.wrapOn(self.c, self.width, self.height)
        dumnum4.drawOn(self.c, 10. *cm, fig_height + 2.0* cm)
        dumnum5 = create_number_box_with_colored_back(self,'5', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum5.wrapOn(self.c, self.width, self.height)
        dumnum5.drawOn(self.c, 14.5 *cm, fig_height - 1.0* cm)

        if language == 'english':
            dumleg1 = create_number_box_with_colored_back(self, 'Time series diagram', self.cs_orange, 3.*cm, 0.5*cm, font_size = '8')
        else:
            dumleg1 = create_number_box_with_colored_back(self, 'Zeitreihendiagramm', self.cs_orange, 3.*cm, 0.5*cm, font_size = '8')
        dumleg1.wrapOn(self.c, self.width, self.height)
        dumleg1.drawOn(self.c, 7.5 *cm, fig_height - 1.0* cm)


        if language == 'english':
            dumleg2 = create_number_box_with_colored_back(self, 'Boxplot diagram', self.cs_orange, 2.75*cm, 0.5*cm, font_size = '8')
        else:
            dumleg2 = create_number_box_with_colored_back(self, 'Balkendiagramm', self.cs_orange, 2.75*cm, 0.5*cm, font_size = '8')
            
        dumleg2.wrapOn(self.c, self.width, self.height)
        dumleg2.drawOn(self.c, 15.5 *cm, fig_height - 1.0* cm)
        
        text_top_height = fig_height - 2.5* cm
        
        if language == 'english':
            p1 = Paragraph("<span name=Helvetica color=black size = 10>Scale and units of the projected changes for the respective parameter.</span>", style=self.styles['Justify'])
        else:
            p1 = Paragraph("<span name=Helvetica color=black size = 10>Skala und Einheit der simulierten Änderungen des jeweiligen Klimakennwertes.</span>", style=self.styles['Justify'])
        breitep1, hoehep1 = p1.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p2 = Paragraph("<span name=Helvetica color=black size = 10>Time scale: years for the time series diagram and 30-year periods for the boxplot diagrams.</span>", style=self.styles['Justify'])
        else:
            p2 = Paragraph("<span name=Helvetica color=black size = 10>Zeitachse eingeteilt in historischen Zeitraum mit beobachteten Treibhausgasen und Szenarienzeitraum.</span>", style=self.styles['Justify'])

        breitep2, hoehep2 = p2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p3 = Paragraph("<span name=Helvetica color=black size = 10>Legend for the time series and boxplot diagrams. Colors are indicating the underlying emission scenarios, where RCP denotes Representative Concentration Pathways.\
                RCP8.5: Pathway for a scenario with high greenhouse gas emissions. RCP4.5: scenario with medium amount of greenhouse gas emissions. RCP2.6: scenario, with smaller\
                or even negative greenhouse gas emissions. The numbers in brackets indicate the number of simulations entering the analysis for the respective index and scenario. As some variables were not provided for all model simulations,\
                this numbers slightly differ for some of the indices from the total number of simulations available.</span>", style=self.styles['Justify'])
        else:
            p3 = Paragraph("<span name=Helvetica color=black size = 10>Legende für Zeitreihendiagramm mit Farben zur Kennzeichnung der zugrunde\
                liegenden Emissionsszenarien (rechts), Legende zur Darstellung der beobachteten Jahreswerte (links).</span>", style=self.styles['Justify'])
        breitep3, hoehep3 = p3.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p4 = Paragraph('<span name=Helvetica color=black size = 10>The </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>time series diagram </span><span name=Helvetica color=black size = 10>shows the projected 30-years running mean changes of the respective index with respect to the climate reference period of the years 1971 to 2000.\
                       The values are centered around the 16th year of each 30-years period, i.e. each value represents the mean value of the 30 years around this year. Each line belongs to a specific model simulation. \
                       They are colored as indicated in the legend in three colors, corresponding to the three emission scenarios. In addition, the range between the smallest and the largest changes projected by each of the three scenarios\
                       is shown by the respective background color.  </span>', style=self.styles['Justify'])
        else:
            p4 = Paragraph('<span name=Helvetica color=black size = 10>Im </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>Zeitreihendiagramm </span><span name=Helvetica color=black size = 10>sind die fortlaufenden 30-jährigen Mittel der simulierten Änderungen\
                       des jeweiligen Klimakennwertes jeweils im Vergleich zur Referenzperiode 1971\u202F-\u202F2000 dargestellt.\
                       Die Werte sind auf das 16. Jahr der 30-Jahres-Perioden abgebildet. Die Bereiche zwischen dem 15. und 85. Perzentil \
                       sind farblich für jedes Emissionsszenario hinterlegt. Zudem sind im Hintergrund absolute Maxima und Minima der Änderungen einzelner Jahre des Projektionsensembles dargestellt.\
                       Blaue und rote Balken zeigen positive und negative Abweichungen der beobachteten Jahreswerte vom beobachteten 30-jährigen Mittelwert von 1971-2000.</span>', style=self.styles['Justify'])

        breitep4, hoehep4 = p4.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p5 = Paragraph('<span name=Helvetica color=black size = 10>In the </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>boxplot diagram </span><span name=Helvetica color=black size = 10> the range of the projected changes is shown for two specific time periods relative to the climate reference period of 1971 to 2000: \
                       The middle of the 21st century is represented by the years '+ self.mid_year_1+' to '+ self.mid_year_2+', the end of the 21st century by the period from '+ self.end_year_1+' to '+ self.end_year_2+'. The bars show some characteristics of the ensemble of projections.\
                       </span>', style=self.styles['Justify'])
        else:
            p5 = Paragraph('<span name=Helvetica color=black size = 10>Im </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>Balkendiagramm </span><span name=Helvetica color=black size = 10> sind die Spannbreiten der simulierten Änderungen für zwei 30-Jahres-Perioden\
                       jeweils im Vergleich zur Referenzperiode 1971\u202F-\u202F2000 dargestellt: '+ self.mid_year_1+'\u202F-\u202F'+ self.mid_year_2+' als Zeitperiode „zur Mitte des 21. Jahrhunderts“\
                       und '+ self.end_year_1+'\u202F-\u202F'+ self.end_year_2+' als Zeitperiode „zum Ende des 21. Jahrhunderts“. Die Balken illustrieren jeweils charakteristische Kennwerte des Ensembles der\
                       verfügbaren Modelle: </span>', style=self.styles['Justify'])
        breitep5, hoehep5 = p5.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        content = []
        heights = (max(hoehep1+ 0.75*cm, 1.2 * cm), max(hoehep2+ 0.75*cm, 1.2 * cm), max(hoehep3 + 0.75*cm, 1.2 * cm),
                   max(hoehep4 + 0.75*cm, 1.2 * cm), max(hoehep5 + 0.75*cm, 1.2 * cm))
        breiten = (1.5*cm, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm)
        content.append((dumnum, p1))
        content.append((dumnum2, p2)) 
        content.append((dumnum3, p3)) 
        content.append((dumnum4, p4)) 
        content.append((dumnum5, p5)) 
        table = Table((content), colWidths=breiten, rowHeights=heights)
        table.setStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        #("GRID", (0,0), (1,0), 0.25, colors.gray),
                        #('BACKGROUND', (0, 0), (0, 0), color)
                        ])
        table.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts,  self.height)
        table.drawOn(self.c, self.text_offset_links + 0.5 * cm, text_top_height - numpy.sum(heights) + 1.*cm)
        im = Image(self.balken_image_legend)
        im.drawHeight = 2.5 * cm
        im.drawWidth = im.drawHeight * 112./356
        im.wrapOn(self.c, self.width, self.height)
        im.drawOn(self.c, self.text_offset_links + 2.7 * cm, text_top_height - numpy.sum(heights) - im.drawHeight + 1.*cm)
        #horiz. striche von unten nach oben
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.1*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.1*cm)
        t1 = Paragraph('<span name=Helvetica color=black size = 8>Minimum</span>', style=self.styles['Justify'])
        t1.wrapOn(self.c, self.width, self.height)        
        t1.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 0.9*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.45*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.45*cm)
        t2 = Paragraph('<span name=Helvetica color=black size = 8>15%</span>', style=self.styles['Justify'])
        t2.wrapOn(self.c, self.width, self.height)        
        t2.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.25*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.*cm)
        t3 = Paragraph('<span name=Helvetica color=black size = 8>Median</span>', style=self.styles['Justify'])
        t3.wrapOn(self.c, self.width, self.height)        
        t3.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.8*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.8*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.8*cm)
        t4 = Paragraph('<span name=Helvetica color=black size = 8>85%</span>', style=self.styles['Justify'])
        t4.wrapOn(self.c, self.width, self.height)        
        t4.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.6*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 3.3*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 3.3*cm)
        t5 = Paragraph('<span name=Helvetica color=black size = 8>Maximum</span>', style=self.styles['Justify'])
        t5.wrapOn(self.c, self.width, self.height)        
        t5.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 3.1*cm)
        
        if language == 'english':
            tex = Paragraph('<span name=Helvetica color=black size = 10> The total range of projections is found between the minimum and maximum value indicated in the bars.\
                The median denotes the simulation of which the value of projected changes is located in the center of the entire bandwith of the ensemble.\
                In addition, those values are marked where 15% of the ensemble project changes below or above this value.</span>', style=self.styles['Justify'])
        else:
            tex = Paragraph('<span name=Helvetica color=black size = 10> Zwischen Minimum und Maximum liegt die gesamte Spannbreite der Ergebnisse.\
                Der Median ist der Wert der Simulation, welche in der Mitte des Ensembles liegt.\
                Zudem sind noch die Werte des Ensembles gekennzeichnet, unter denen 15% bzw. 85% der Simulationen liegen. </span>', style=self.styles['Justify'])
            
        bt, ht =tex.wrapOn(self.c, self.width  - self.text_offset_links - self.text_offset_links - 5.1 * cm - im.drawWidth, self.height)        
        tex.drawOn(self.c, self.text_offset_links + 5. * cm + im.drawWidth, text_top_height - numpy.sum(heights) - ht + 1.*cm)

        if language == 'english':
            tex2 = Paragraph('<span name=Helvetica color=black size = 10> Red color stands for the high emission scenario (RCP8.5), RCP4.5 is given in blue and RCP2.6 in gray colors. </span>', style=self.styles['Justify'])
        else:
            tex2 = Paragraph('<span name=Helvetica color=black size = 10> Die Balken sind für das Szenario  mit niedrigen Emissionen (RCP2.6) grün dargestellt, für das mittlere  Emissionsszenario\
                (RCP4.5) in orange und für das Szenario mit hohen Emissionen (RCP8.5) in violett. Unter den Balken sind die zugehörigen Symbole der Robustheit der Projektionen angegeben.\
                Für einige Klimakennwerte werden die Balkendiagramme zusätzlich auch für alle\
                vier Jahreszeiten gezeigt. </span>', style=self.styles['Justify'])
            
        bt2, ht2 =tex2.wrapOn(self.c, self.width  - self.text_offset_links - self.text_offset_links - 2.4 * cm , self.height)        
        if language == 'english':
            tex2.drawOn(self.c, self.text_offset_links + 2.4*cm, text_top_height - numpy.sum(heights) - ht - im.drawHeight + 2.*cm)
        else:
            tex2.drawOn(self.c, self.text_offset_links + 2.4*cm, text_top_height - numpy.sum(heights) - ht - im.drawHeight)

########################################################################################################
def insert_leseanleitung_abbildungen_teil2(self, y_pos='', language='english'):
        back = Image(self.background)
        if language == 'english':
            back.drawHeight = self.height - 5. * cm
        else:
            back.drawHeight = self.height - 5. * cm
        back.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts
        back.wrapOn(self.c, self.width, self.height)
        if language == 'english':
            back.drawOn(self.c, self.text_offset_links, 3. * cm)
        else:
            back.drawOn(self.c, self.text_offset_links, 2. * cm)
        einfuegehoehe = self.height - 3.5 * cm
        self.c.setFont('Helvetica-Bold', 14)
        self.c.setFillColor(self.cs_orange)
        index = 0
        dum_im = self.path_pre_s +'/'+ self.region_nuts_in_file+ "/Klimaausblick_FD_"+self.region_nuts_in_file+"_topfigure_indexpage_deutsch_1950_2098_fill_all_range_sep_periods.png"
#        dum_im = self.path_pre_s +'/'+ self.region_nuts_in_file + '/Klimaausblick_FD_'+self.region_nuts_in_file+'_climate_change_timeseries_plot_deutsch_k.png'
        example_figure = Image(dum_im)
        example_figure.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts - 1.*cm
        example_figure.drawHeight = example_figure.drawWidth * 1800./6600.
        example_figure.wrapOn(self.c, self.width, self.height)
        fig_height = self.height - 3.5 * cm - example_figure.drawHeight
        example_figure.drawOn(self.c, self.text_offset_links + 0.5*cm, fig_height)
        dumnum = create_number_box_with_colored_back(self, '1', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum.wrapOn(self.c, self.width, self.height)
        dumnum.drawOn(self.c, 3.0 *cm, fig_height + 2.5* cm)
        dumnum2 = create_number_box_with_colored_back(self,'2', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum2.wrapOn(self.c, self.width, self.height)
        dumnum2.drawOn(self.c, 5.5 *cm, fig_height - 0.5* cm)
        dumnum3 = create_number_box_with_colored_back(self,'3', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum3.wrapOn(self.c, self.width, self.height)
        dumnum3.drawOn(self.c, 6.5 *cm, fig_height + 1.0* cm)
        dumnum4 = create_number_box_with_colored_back(self,'4', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum4.wrapOn(self.c, self.width, self.height)
        dumnum4.drawOn(self.c, 10. *cm, fig_height + 2.0* cm)
        dumnum5 = create_number_box_with_colored_back(self,'5', self.cs_orange, 0.5*cm, 0.5*cm, font_size = '8')
        dumnum5.wrapOn(self.c, self.width, self.height)
        dumnum5.drawOn(self.c, 15. *cm, fig_height + 1.0* cm)

        if language == 'english':
            dumleg1 = create_number_box_with_colored_back(self, 'Time series diagram', self.cs_orange, 3.*cm, 0.5*cm, font_size = '8')
        else:
            dumleg1 = create_number_box_with_colored_back(self, 'Zeitreihendiagramm', self.cs_orange, 3.*cm, 0.5*cm, font_size = '8')
        dumleg1.wrapOn(self.c, self.width, self.height)
        dumleg1.drawOn(self.c, 7.5 *cm, fig_height - 1.0* cm)


        if language == 'english':
            dumleg2 = create_number_box_with_colored_back(self, 'Boxplot diagram', self.cs_orange, 2.75*cm, 0.5*cm, font_size = '8')
        else:
            dumleg2 = create_number_box_with_colored_back(self, 'Balkendiagramm', self.cs_orange, 2.75*cm, 0.5*cm, font_size = '8')

        dumleg2.wrapOn(self.c, self.width, self.height)
        dumleg2.drawOn(self.c, 15. *cm, fig_height - 1.0* cm)

        text_top_height = fig_height - 2.5* cm

        if language == 'english':
            p1 = Paragraph("<span name=Helvetica color=black size = 10>Scale and units of the projected changes for the respective parameter.</span>", style=self.styles['Justify'])
        else:
            p1 = Paragraph("<span name=Helvetica color=black size = 10>Skala und Einheit der simulierten Änderungen des jeweiligen Klimakennwertes.</span>", style=self.styles['Justify'])
        breitep1, hoehep1 = p1.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p2 = Paragraph("<span name=Helvetica color=black size = 10>Time scale: years for the time series diagram and 30-year periods for the boxplot diagrams.</span>", style=self.styles['Justify'])
        else:
            p2 = Paragraph("<span name=Helvetica color=black size = 10>Zeitachse: Jahre für das Zeitreihendiagramm, 30-Jahres-Perioden für die Balkendiagramme.</span>", style=self.styles['Justify'])

        breitep2, hoehep2 = p2.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p3 = Paragraph("<span name=Helvetica color=black size = 10>Legend for the time series and boxplot diagrams. Colors are indicating the underlying emission scenarios, where RCP denotes Representative Concentration Pathways.\
                RCP8.5: Pathway for a scenario with high greenhouse gas emissions. RCP4.5: scenario with medium amount of greenhouse gas emissions. RCP2.6: scenario, with smaller\
                or even negative greenhouse gas emissions. The numbers in brackets indicate the number of simulations entering the analysis for the respective index and scenario. As some variables were not provided for all model simulations,\
                this numbers slightly differ for some of the indices from the total number of simulations available.</span>", style=self.styles['Justify'])
        else:
            p3 = Paragraph("<span name=Helvetica color=black size = 10>Legende für Zeitreihen- und Balkendiagramm mit Farben zur Kennzeichnung der zugrunde\
                liegenden Emissionsszenarien: RCP steht für „Representative Concentration Pathway“; RCP8.5: Pfad für ein Szenario mit weiter zunehmenden\
                Treibhausgasemissionen, RCP4.5: Pfad für ein Szenario mit mittleren Treibhausgasemissionen, RCP2.6: Pfad für ein Szenario mit\
                geringen Treibhausgasemissionen. In Klammern nach den RCPs steht jeweils die Anzahl der verwendeten Simulationen (nach Verfügbarkeit der bereitgestellten\
                Parameter).</span>", style=self.styles['Justify'])
        breitep3, hoehep3 = p3.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p4 = Paragraph('<span name=Helvetica color=black size = 10>The </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>time series diagram </span><span name=Helvetica color=black size = 10>shows the projected 30-years running mean changes of the respective index with respect to the climate reference period of the years 1971 to 2000.\
                       The values are centered around the 16th year of each 30-years period, i.e. each value represents the mean value of the 30 years around this year. Each line belongs to a specific model simulation. \
                       They are colored as indicated in the legend in three colors, corresponding to the three emission scenarios. In addition, the range between the smallest and the largest changes projected by each of the three scenarios\
                       is shown by the respective background color.  </span>', style=self.styles['Justify'])
        else:
            p4 = Paragraph('<span name=Helvetica color=black size = 10>Im </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>Zeitreihendiagramm </span><span name=Helvetica color=black size = 10>sind die fortlaufenden 30-jährigen Mittel der simulierten Änderungen\
                       des jeweiligen Klimakennwertes jeweils im Vergleich zur Referenzperiode 1971\u202F-\u202F2000 dargestellt.\
                       Die Werte sind immer auf das 16. Jahr der 30-Jahres-Perioden abgebildet. Die einzelnen Linien zeigen\
                       die Ergebnisse für jede einzelne Modellsimulation, die in die Auswertungen für den Klima-Ausblick eingegangen sind.\
                       Sie sind entsprechend des zugrunde liegenden Emissionsszenarios farblich markiert. Zudem sind die Bereiche zwischen der jeweils geringsten und höchsten\
                       simulierten Änderung entsprechend farblich für jedes Emissionsszenario hinterlegt.</span>', style=self.styles['Justify'])

        breitep4, hoehep4 = p4.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        if language == 'english':
            p5 = Paragraph('<span name=Helvetica color=black size = 10>In the </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>boxplot diagram </span><span name=Helvetica color=black size = 10> the range of the projected changes is shown for two specific time periods relative to the climate reference period of 1971 to 2000: \
                       The middle of the 21st century is represented by the years '+ self.mid_year_1+' to '+ self.mid_year_2+', the end of the 21st century by the period from '+ self.end_year_1+' to '+ self.end_year_2+'. The bars show some characteristics of the ensemble of projections.\
                       </span>', style=self.styles['Justify'])
        else:
            p5 = Paragraph('<span name=Helvetica color=black size = 10>Im </span><span name=Helvetica-bold color="rgb('+str(int(self.cs_orange.red * 255.))+','+str(int(self.cs_orange.green * 255.))+', '+str(int(self.cs_orange.blue * 255.))+')"\
                       size = 10>Balkendiagramm </span><span name=Helvetica color=black size = 10> sind die Spannbreiten der simulierten Änderungen nochmal für zwei 30-Jahres-Perioden\
                       jeweils im Vergleich zur Referenzperiode 1971\u202F-\u202F2000 dargestellt: '+ self.mid_year_1+'\u202F-\u202F'+ self.mid_year_2+' als Zeitperiode „zur Mitte des 21. Jahrhunderts“\
                       und '+ self.end_year_1+'\u202F-\u202F'+ self.end_year_2+' als Zeitperiode „zum Ende des 21. Jahrhunderts“. Die Balken illustrieren jeweils charakteristische Kennwerte des Ensembles der\
                       verfügbaren Modelle: </span>', style=self.styles['Justify'])
        breitep5, hoehep5 = p5.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm, self.height)

        content = []
        heights = (max(hoehep1+ 0.75*cm, 1.2 * cm), max(hoehep2+ 0.75*cm, 1.2 * cm), max(hoehep3 + 0.75*cm, 1.2 * cm),
                   max(hoehep4 + 0.75*cm, 1.2 * cm), max(hoehep5 + 0.75*cm, 1.2 * cm))
        breiten = (1.5*cm, self.width - self.text_offset_links - self.text_offset_rechts - 2.5*cm)
        content.append((dumnum, p1))
        content.append((dumnum2, p2))
        content.append((dumnum3, p3))
        content.append((dumnum4, p4))
        content.append((dumnum5, p5))
        table = Table((content), colWidths=breiten, rowHeights=heights)
        table.setStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        #("GRID", (0,0), (1,0), 0.25, colors.gray),
                        #('BACKGROUND', (0, 0), (0, 0), color)
                        ])
        table.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts,  self.height)
        table.drawOn(self.c, self.text_offset_links + 0.5 * cm, text_top_height - numpy.sum(heights) + 1.*cm)
        im = Image(self.balken_image_legend)
        im.drawHeight = 2.5 * cm
        im.drawWidth = im.drawHeight * 112./356
        im.wrapOn(self.c, self.width, self.height)
        im.drawOn(self.c, self.text_offset_links + 2.7 * cm, text_top_height - numpy.sum(heights) - im.drawHeight + 1.*cm)
        #horiz. striche von unten nach oben
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.1*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.1*cm)
        t1 = Paragraph('<span name=Helvetica color=black size = 8>Minimum</span>', style=self.styles['Justify'])
        t1.wrapOn(self.c, self.width, self.height)
        t1.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 0.9*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.45*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.45*cm)
        t2 = Paragraph('<span name=Helvetica color=black size = 8>15%</span>', style=self.styles['Justify'])
        t2.wrapOn(self.c, self.width, self.height)
        t2.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.25*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.*cm)
        t3 = Paragraph('<span name=Helvetica color=black size = 8>Median</span>', style=self.styles['Justify'])
        t3.wrapOn(self.c, self.width, self.height)
        t3.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 1.8*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.8*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.8*cm)
        t4 = Paragraph('<span name=Helvetica color=black size = 8>85%</span>', style=self.styles['Justify'])
        t4.wrapOn(self.c, self.width, self.height)
        t4.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 2.6*cm)
        self.c.line(self.text_offset_links + 2.9 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 3.3*cm,
                    self.text_offset_links + 3.2 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 3.3*cm)
        t5 = Paragraph('<span name=Helvetica color=black size = 8>Maximum</span>', style=self.styles['Justify'])
        t5.wrapOn(self.c, self.width, self.height)
        t5.drawOn(self.c, self.text_offset_links + 3.4 * cm + im.drawWidth, text_top_height - numpy.sum(heights) - im.drawHeight + 3.1*cm)

        if language == 'english':
            tex = Paragraph('<span name=Helvetica color=black size = 10> The total range of projections is found between the minimum and maximum value indicated in the bars.\
                The median denotes the simulation of which the value of projected changes is located in the center of the entire bandwith of the ensemble.\
                In addition, those values are marked where 15% of the ensemble project changes below or above this value.</span>', style=self.styles['Justify'])
        else:
            tex = Paragraph('<span name=Helvetica color=black size = 10> Zwischen Minimum und Maximum liegt die gesamte Spannbreite der Ergebnisse.\
                Der Median ist der Wert der Simulation, welche in der Mitte des Ensembles liegt.\
                Zudem sind noch die Werte des Ensembles gekennzeichnet, unter denen 15% bzw. 85% der Simulationen liegen. </span>', style=self.styles['Justify'])

        bt, ht =tex.wrapOn(self.c, self.width  - self.text_offset_links - self.text_offset_links - 5.1 * cm - im.drawWidth, self.height)
        tex.drawOn(self.c, self.text_offset_links + 5. * cm + im.drawWidth, text_top_height - numpy.sum(heights) - ht + 1.*cm)

        if language == 'english':
            tex2 = Paragraph('<span name=Helvetica color=black size = 10> Red color stands for the high emission scenario (RCP8.5), RCP4.5 is given in blue and RCP2.6 in gray colors. </span>', style=self.styles['Justify'])
        else:
            tex2 = Paragraph('<span name=Helvetica color=black size = 10> Die Balken sind für das Szenario mit hohen Emissionen (RCP8.5) in rot, für das mittlere  Emissionsszenario\
                (RCP4.5) in blau und für das Szenario mit niedrigen Emissionen (RCP2.6) in grau dargestellt. Für einige Klimakennwerte werden die Balkendiagramme zusätzlich auch für alle\
                vier Jahreszeiten gezeigt. </span>', style=self.styles['Justify'])

        bt2, ht2 =tex2.wrapOn(self.c, self.width  - self.text_offset_links - self.text_offset_links - 2.4 * cm , self.height)
        if language == 'english':
            tex2.drawOn(self.c, self.text_offset_links + 2.4*cm, text_top_height - numpy.sum(heights) - ht - im.drawHeight + 2.*cm)
        else:
            tex2.drawOn(self.c, self.text_offset_links + 2.4*cm, text_top_height - numpy.sum(heights) - ht - im.drawHeight + 0.5*cm)
