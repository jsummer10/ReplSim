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

def CreateWorkbook():
    """ Open and set workbook configurations """
    
    if not os.path.isdir('output'):
        os.mkdir('output')

    global sim_workbook

    sim_workbook = Workbook('output/sim_data.xlsx')

    sim_workbook.set_size(3000, 1600)

def CreateSummarySheet():
    """ Create excel sheet for the summary """

    global sum_sheet

    sum_sheet = sim_workbook.add_worksheet('Simulation Summary')

def WriteSummaryData(y, x, data):
    """ Write a list to the summary sheet """
    sum_sheet.write_row(y, x, data)

def CreateCacheSheet():
    """ Create excel sheet for the summary """

    global cache_sheet

    cache_sheet = sim_workbook.add_worksheet('Cache')

def WriteCacheData(x, cache, title):
    """ Create excel sheet for the cache """

    cache_sheet.write(1, x, title)

    cache_sheet.write(2, x, 'Use Index')

    for i in range(1, len(cache[0])):
        cache_sheet.write(2, i+x, 'Block ' + str(i))

    y = 3
    for line in cache:
        cache_sheet.write(y, x, line[0])
        for i in range(1,len(line)):
            cache_sheet.write(y, i+x, hex(line[i]))
        y += 1

def CloseWorkbook():
    sim_workbook.close()