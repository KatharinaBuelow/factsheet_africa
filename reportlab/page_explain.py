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

###########################################################################
def insert_hintergrundinformation_rcps(self, y_pos='', language='english'):

        einfuegehoehe = y_pos - 0.5 * cm
        self.c.setFont('Helvetica-Bold', 14)
        self.c.setFillColor(self.cs_orange)
        index = 0
        if language == 'english':
            tit = 'Climate Projections and Scenarios'
        else:
            tit = 'Klimaprojektionen und Szenarien'
        content1 = []
        rcp_image = Image(self.rcp_dummy_im)
        rcp_image = get_image(self.rcp_dummy_im, height = 5.*cm)

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
        content1.append((rcp_image,'', text1))
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


def insert_glossar_page(self, glossar_dict, variables):
        back = Image(self.background)
        back.drawHeight = self.height - 4.75 * cm
        back.drawWidth = self.width - self.text_offset_links - self.text_offset_rechts
        back.wrapOn(self.c, self.width, self.height)
        back.drawOn(self.c, self.text_offset_links, 1.75 * cm)
        
        einfuegehoehe = self.height - 2.85 * cm
        self.c.setFont('Helvetica-Bold', 14)
        self.c.setFillColor(self.cs_orange)
        index = 0
        var_col_width = 4.*cm
        content = []
        columnwidths = (var_col_width, self.width - self.text_offset_links - self.text_offset_rechts - var_col_width - 0.5 *cm)
        #heights = [0.45 * cm] * (len(variables))
        heights = []
        heights.insert(0, 1. * cm)
        font_size = 10
        font_size2 = 8
        content.append((Paragraph('<span name=Helvetica-bold color=black size ='+str(font_size)+'>Kennwert</span>', style=self.styles['Centered']),
                       Paragraph('<span name=Helvetica-bold color=black size ='+str(font_size)+'>Definition</span>', style=self.styles['Centered'])))
        #content.append((Paragraph('Parameter', style=self.styles['Centered']), Paragraph('Definition', style=self.styles['Centered'])))
        for var in variables:
            text_zeile = Paragraph('<span name=Helvetica color=black size ='+str(font_size2)+'>'+glossar_dict[var][1]+'</span>', style=self.styles['SmallTableContent'])
            breite, hoehe = text_zeile.wrapOn(self.c, self.width - self.text_offset_links - self.text_offset_rechts - var_col_width - 1. *cm, self.height)
            varara = Paragraph('<span name=Helvetica color=black size ='+str(font_size2)+'>'+glossar_dict[var][0]+'</span>', style = self.styles['SmallTableContent'])
            breite2, hoehe2 = varara.wrapOn(self.c, var_col_width , self.height)
            content.append((varara, text_zeile))
            #print( hoehe, hoehe2)
            self.hoehe = hoehe
            heights.append(max(hoehe+ 0.25 * cm, hoehe2+ 0.25 * cm)+ 0.2 * cm)
        dum = heights.pop(-1)
        heights.append(dum + 0.25*cm)
        table = Table(content, colWidths=columnwidths, rowHeights=heights)
        table.setStyle([("VALIGN", (0, 0), (1, 0), "MIDDLE"),
                        ("VALIGN", (0, 1), (1, -1), "CENTER"),
                        ("ALIGN", (0, 0), (0, -1), "LEFT"),
                        ("GRID", (0,0), (-1,-1), 0.25, colors.gray),
                        ('BACKGROUND', (0, 0), (-1, -1), (colors.Color(255 / 255., 255 / 255., 255 / 255., 1)))])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, self.text_offset_links + 0.25*cm, einfuegehoehe -0.25 * cm - numpy.sum(heights))

def return_glossar(sprache):
    glossar_dict = {'TG': ['Temperatur', 'Die Temperatur ist hier die bodennahe Lufttemperatur (2 m über Grund). Die Werte für\
                                Jahresmittel und Jahreszeiten werden auf Basis der Tagesmittelwerte der Temperatur berechnet.\
                                Die Werte für die Jahreszeiten werden für das meteorologische Jahr berechnet: Die Temperatur für den Winter\
                                ist der Mittelwert aller Tage in den Monaten Dezember, Januar, Februar; für das Frühjahr in den Monaten März, April, Mai;\
                                für den Sommer in den Monaten Juni, Juli, August; und für den Herbst in den Monaten September, Oktober, November.'],
                    'TX': ['Maximum Temperatur', 'Die Temperatur ist hier die bodennahe Lufttemperatur (2 m über Grund). Die Werte für\
                                Jahresmittel und Jahreszeiten werden auf Basis der Tagesmaxima der Temperatur berechnet.'],
                    'TN': ['Minimum Temperatur', 'Die Temperatur ist hier die bodennahe Lufttemperatur (2 m über Grund). Die Werte für\
                                Jahresmittel und Jahreszeiten werden auf Basis der Tagesminima der Temperatur berechnet.'],
                    'SU': ['Sommertage','Anzahl an Tagen pro Jahr mit einer Tagesmaximumtemperatur von mehr als 25\u202F°C.'],
                    'SU18': ['Warme Tage','Anzahl an Tagen pro Jahr mit einer Tagesmaximumtemperatur von mehr als 18\u202F°C.'],
                    'SU30': ['Heiße Tage', 'Anzahl an Tagen pro Jahr mit einer Tagesmaximumtemperatur von mehr als 30\u202F°C.'],
                    'SU35': ['Sehr heiße Tage', 'Anzahl an Tagen pro Jahr mit einer Tagesmaximumtemperatur von mehr als 35\u202F°C.'],
                    'SU40': ['Extrem heiße Tage', 'Anzahl an Tagen pro Jahr mit einer Tagesmaximumtemperatur von mehr als 40\u202F°C.'],
                    'TR': ['Tropische Nächte','Anzahl an Tagen pro Jahr mit einer Minimumtemperatur von mehr als 20\u202F°C.'],
                    'SQI': ['Schlecht Schlaf Index','Anzahl an Tagen pro Jahr mit einer Minimumtemperatur von mehr als 18\u202F°C.'],
                    'CHD30x': ['Maximale Dauer von Hitzeperioden','jährliches Maximum der Länge von Perioden an denen die Tagesmaximumtemperatur von 30°C überschritten wird '],
                    'GD5':['Tage über 5\u202F°C','Anzahl an Tagen pro Jahr mit einer Tagesmitteltemperatur größer als 5\u202F°C. Diese Tage werden gelegentlich auch als Vegetationstage bezeichnet.\
                         Um zu beantworten, ob die Vegetation an einem bestimmten Tag wächst, sind jedoch noch andere Faktoren entscheidend, z.B. Bodenfeuchte, Strahlung und Nährstoffverfügbarkeit.'],
                    'WI': ['Wintertage', 'Anzahl der Tage pro Jahr mit einer Tagesminimumtemperatur geringer als -10\u202F°C.'],
                    'ID':['Eistage','Anzahl der Tage pro Jahr mit einer Tagesmaximumtemperatur geringer als 0\u202F°C.'],
                    'FD': ['Frosttage','Anzahl der Tage pro Jahr mit einer Tagesminimumtemperatur geringer als 0\u202F°C.'],
                    'LFD': ['Frosttage in April/Mai/Juni','Anzahl der Tage pro Jahr mit einer Tagesminimumtemperatur geringer als 0\u202F°C zwischen dem 1. April und dem 30. Juni.'],
                    'RRm': ['Niederschlag','Die Niederschlagswerte werden auf Basis von täglichen Niederschlagsmengen berechnet und als\
                                 durchschnittliche monatliche Niederschlagssummen bezogen aufs Jahr und die Jahreszeiten in mm pro Monat angegeben.\
                                 Sie beinhalten sowohl flüssigen als auch festen Niederschlag, also Regen und Schnee. Die jahreszeitlichen Niederschlagsmengen\
                                 werden für das meteorologische Jahr berechnet (siehe Erläuterungen zur Temperatur).'],
                    'R5mm': ['Niederschlag &#8805; 5\u202Fmm/Tag','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) von 5\u202Fmm\
                                überschritten wird. '],
                    'R10mm': ['Niederschlag &#8805; 10\u202Fmm/Tag','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) von 10\u202Fmm\
                                überschritten wird. '],
                    'R15mm': ['Niederschlag &#8805; 15\u202Fmm/Tag','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) von 15\u202Fmm\
                                überschritten wird. '],
                    'R20mm': ['Tage mit Niederschlag &#8805; 20\u202Fmm/Tag','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) von 20\u202Fmm\
                                erreicht oder überschritten wird. '],
                    'R25mm': ['Niederschlag &#8805; 25\u202Fmm/Tag','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) von 25\u202Fmm\
                                überschritten wird. '],
                    'DD': ['Trockentage','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) weniger als  1\u202Fmm beträgt.'],
                    #'RR1': ['Trockentage','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) weniger als  1\u202Fmm beträgt.'],
                    'RR1': ['Nasse Tage','Anzahl der Tage pro Jahr, an denen die Niederschlagsmenge (Regen und Schnee) mindestens  1\u202Fmm beträgt'],
                    'FG': ['Windgeschwindigkeit','Mittlere Windgeschwindigkeit im Jahr in m/s.'],
                    'RR95p' : ['95. Perzentil des Niederschlags', 'Tagesniederschlag, dessen Höhe an 5% aller Tage im Jahr mit Niederschlag über 1\u202Fmm überschritten wird.'],
                    'RR99p' : ['99. Perzentil des Niederschlags', 'Tagesniederschlag, dessen Höhe an 1% aller Tage im Jahr mit Niederschlag über 1\u202Fmm überschritten wird.'],
                    'R95p' : ['Niederschlagstage > 95. Perzentil', 'Anzahl der Tage mit Tagesniederschlag, dessen Höhe nur an 5% aller Tage im Jahr mit Niederschlag über 1\u202Fmm im Referenzklima (1971 - 2000) überschritten wird.'],
                    'R99p' : ['Niederschlagstage > 99. Perzentil',  'Anzahl der Tage mit Tagesniederschlag, dessen Höhe nur an 1% aller Tage im Jahr mit Niederschlag über 1\u202Fmm im Referenzklima (1971 - 2000) überschritten wird.'],
                    'R95pTOT' : ['Niederschlagsanteil > 95. Perzentil', 'Anteil des Niederschlags, der an den 5% niederschlagsreichsten Tagen aller nassen Tage im Jahr des Referenzklimazeitraumes (1971 - 2000) überschritten wird.'],
                    'R99pTOT' : ['Niederschlagsanteil > 99. Perzentil', 'Anteil des Niederschlags, der an den 1% niederschlagsreichsten Tagen aller nassen Tage im Jahr des Referenzklimazeitraumes (1971 - 2000) überschritten wird.'],
                    'r95p-gerics' : ['Niederschlagstage > 95. Perzentil', 'Anzahl der Tage pro Jahr bzw. pro Jahreszeit deren Tagesniederschlagshöhe nur an  5% aller nasser Tage im Referenzklima (1971 - 2000) überschritten wird.'],
                    'r99p-gerics' : ['Niederschlagstage > 99. Perzentil',  'Anzahl der Tage pro Jahr bzw. pro Jahreszeit deren Tagesniederschlagshöhe nur an 1% aller nasser Tage im Referenzklima (1971 - 2000) überschritten wird.'],
                    'r95-gerics' : ['95. Perzentil des Niederschlags', 'Tagesniederschlag, dessen Höhe nur an 5% der nassen Tage im Jahr bzw. in der Jahreszeit überschritten wird.'],
                    'r99-gerics' : ['99. Perzentil des Niederschlags',  'Tagesniederschlag, dessen Höhe nur an 1% der nassen Tage im Jahr bzw. in der Jahreszeit überschritten wird.'],
                    'CWB' : ['Klimatische Wasserbilanz', 'Jahresmittel der täglichen Differenz von Niederschlag und Verdunstung in mm/Tag.'],
                    'WD': ['Warm-trockene Tage','Anzahl der Tage pro Jahr an denen die Temperatur über dem 75. Perzentil und der Niederschlag unter dem 25. Perzentil liegt.'],
                    'Sfreq': ['Schneetage','Anzahl der Tage pro Jahr an denen Schnee fällt.'],
                    'GSS': ['Start der Wachstumsperiode','Start der Wachstumsperiode.'],
                    'HSx3': ['Maximale Dauer von Hitzeperioden','jährliches Maximum der Länge von Perioden an denen mindestens an drei aufeinanderfolgenden Tagen die Tagesmaximumtemperatur von 30°C überschritten wird '],
                    'HSf3': ['Mittlere Häufigkeit des Auftretens Hitzeperioden','jährlicher Mittelwert der Anzahl von Perioden an denen mindestens an drei aufeinanderfolgenden Tagen die Tagesmaximumtemperatur von 30°C überschritten wird '],
                    'DSf': ['Mittlere Häufigkeit des Auftretens Trockenperioden','jährlicher Mittelwert der Anzahl von Perioden an denen mindestens an fünf aufeinanderfolgenden Tagen die Niederschlagsmenge unter 1mm liegt '],
                    "DSx5":['Maximale Dauer von Trockenperioden','jährliches Maximum der Länge von Perioden an denen mindestens an fünf aufeinanderfolgenden Tagen die Niederschlagsmenge unter 1mm liegt'],
                    "HD17" : ["Heizgradtage", "Akkumulierte Temperatursumme aller Tage im Jahr, an denen die mittlere Temperatur 17°C nicht überschreitet"],
                    "FFS" : ["Beginn der frostfreien Saison", "Tag im Jahr, ab dem das Minimum der Tagestemperatur für mindestens 5 aufeinanderfolgende Tage größer oder gleich 0°C war"],
                    "ClimWas" : ["Klimatische Wasserbilanz", "Jahresmittel der täglichen Differenz von Niederschlag und Verdunstung in mm/Tag."],
                    "sultriness" : ["Schwüle", "Anzahl der Tage pro Jahr mit einem Wasserdampf-Partialdruck größer als 18,8 hPa. Der Dampfdruck wird aus Tageswerten der bodennahen Lufttemperatur und der relativen Luftfeuchte mittels der Magnusformel berechnet. ACHTUNG: Basis sind Tageswerte von Temperatur und Luftfeuchte"],
                    "freeze-thaw-days" : ["Tage mit Frost-Tau-Wechsel", "Anzahl der Tage pro Jahr mit Frost-Tau-Wechsel, d.h. der Tage an denen die Tagesminimumtemperatur unter 0°C und die Tagesmaximumtemperatur über 0°C liegt. "],
                     }
    return glossar_dict
