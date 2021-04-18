'''
Project     : Replacement Policy Simulation
File name   : summary.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains the functionality to output
              simulation data cleanly to excel
'''

import os

import xlsxwriter
from xlsxwriter     import Workbook

import plotly.graph_objects as go

class Summary():
    """ This class creates an excel summary of the simulation """ 

    def __init__(self, sim_list):

        self.sim_list = sim_list

        self.CreateWorkbook()
        self.CreateFormats()
        self.WriteSummaryData()
        self.WriteCacheData()
        self.CloseWorkbook()

        self.GraphHits()

    def CreateWorkbook(self):
        """ Open and set workbook configurations """
        
        if not os.path.isdir('output'):
            os.mkdir('output')

        self.sim_workbook = Workbook('output/sim_data.xlsx')

        self.sim_workbook.set_size(2000, 1600)   

    def CreateFormats(self):
        """ Create formats to be used in excel spreadsheet """

        self.heading    = self.sim_workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#DADADA', 'border':1})
        self.data       = self.sim_workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border':1}) 
        self.percent    = self.sim_workbook.add_format({'num_format': '0.00%', 'align':'center', 'valign': 'vcenter', 'border':1})

    def WriteSummaryData(self):
        """ Write a list to the summary sheet """

        sum_sheet = self.sim_workbook.add_worksheet('Summary')
        sum_sheet.set_zoom(130)
        sum_sheet.set_default_row(20)

        x = 1
        for sim in self.sim_list:

            hit_rate = sim['hits'] / (sim['misses'] + sim['hits'])

            sum_sheet.merge_range(1, x, 1, x+1, sim['cache'].config_name, self.heading)
            sum_sheet.write_row(2, x, ['Hits:', sim['hits']], self.data)
            sum_sheet.write_row(3, x, ['Misses:', sim['misses']], self.data)
            sum_sheet.write_row(4, x, ['Hit Rate:', '{:0.2f}%'.format(hit_rate * 100)], self.percent)

            y = 6

            for access in sim['history']:
                sum_sheet.write_row(y, x, access, self.data)
                y += 1

            x += 3

    def WriteCacheData(self):
        """ Create excel sheet for the cache """

        cache_sheet = self.sim_workbook.add_worksheet('Cache')
        cache_sheet.set_zoom(130)
        cache_sheet.set_default_row(20)

        x = 1
        for sim in self.sim_list:

            cache_obj = sim['cache']

            # Heading
            cache_sheet.merge_range(1, x, 1, x+cache_obj.ways-1, sim['cache'].config_name, self.heading)

            # Set lables
            x_cur = x
            for way in range(0,cache_obj.ways):
                cache_sheet.write(2, x_cur, 'Set ' + str(way), self.heading)
                x_cur += 1

            x_end = x_cur

            # Values
            y = 3
            for line in cache_obj.cache:
                x_cur = x
                for way in range(0,len(line)):
                    if line[way]['tag'] is None:
                        cache_sheet.write(y, x_cur, 'set ' + str(way), self.data)
                    else:
                        cache_sheet.write(y, x_cur, hex(line[way]['tag']), self.data)

                    x_cur += 1

                y += 1

            x = x_end + 1

    def GraphHits(self):
        """ Graph a comparison of the hits of each sim """

        x_sim  = []
        y_rate = []

        for sim in self.sim_list:
            x_sim.append(sim['cache'].config_name)
            y_rate.append((sim['hits'] / (sim['misses'] + sim['hits']))*100)

        # Graph bar graph to show the number of commits by author
        fig = go.Figure([go.Bar(x=x_sim, y=y_rate)])

        fig.update_layout(title_text  = 'Hit Rate Comparison',
                          xaxis_title = 'Simulations',
                          yaxis_title = 'Hit Rate (%)')

        fig.write_html('output/HitRateComparison.html') 

    def CloseWorkbook(self):
        self.sim_workbook.close()