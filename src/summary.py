'''
Application : ReplSim
File name   : summary.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : The file contains the functionality to output
              simulation data cleanly to excel
'''

# Copyright (c) April 26, 2021 Jacob Summerville, Martin Lopez, Henry Lee
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

import xlsxwriter
from xlsxwriter     import Workbook

import plotly.graph_objects as go

class Summary():
    """ This class creates an excel summary of the simulation """ 

    def __init__(self, sim_list, title):

        print('Processing Results')

        self.sim_list = sim_list
        self.title = title

        self.CreateWorkbook()
        self.CreateFormats()
        self.SortSims()
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

        self.heading    = self.sim_workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 
                                                        'bg_color': '#DADADA', 'border':1})

        self.data       = self.sim_workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border':1}) 
        
        self.percent    = self.sim_workbook.add_format({'num_format': '0.00%', 'align':'center', 'valign': 'vcenter', 
                                                        'border':1})

    def SortSims(self):
        """ Sort sims in alphabetical order """

        self.sim_list.sort(key=lambda x: x['cache'].config_name)

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
                    if line[way] is None or line[way]['tag'] is None:
                        cache_sheet.write(y, x_cur, 'empty', self.data)
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

        fig.update_layout(title_text  = self.title,
                          xaxis_title = 'Simulations',
                          yaxis_title = 'Hit Rate (%)')

        fig.write_html('output/HitRateComparison.html') 

    def CloseWorkbook(self):
        self.sim_workbook.close()