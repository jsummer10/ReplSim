'''
Project     : Replacement Policy Simulation
File name   : simulation.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the simulation class that will
              run all simulations
'''

from summary import CreateSummarySheet, WriteSummary

class Simulation():
    """ This class defines the simulation environment """

    def __init__(self, cache, mem_accesses):
        self.Run(cache, mem_accesses)

    def Run(self, cache, mem_accesses):
        """ Run simulation """

        CreateSummarySheet()

        self.misses = 0
        self.hits   = 0

        history = []

        for access in mem_accesses:
            if cache.L1CacheAccess(access):
                self.hits += 1
                history.append([hex(access), 'Hit'])
            else:
                self.misses += 1
                history.append([hex(access), 'Miss'])

        cache.WriteCache()

        self.WriteStats(history)

    def WriteStats(self, history):
        """ Prints simulation statistics """ 

        hit_rate = self.hits / (self.misses + self.hits)

        WriteSummary(1, 1, ['Hits:', self.hits])
        WriteSummary(2, 1, ['Misses:', self.misses])
        WriteSummary(3, 1, ['Hit Rate:', '{:0.2f}%'.format(hit_rate * 100)])

        y = 5

        for access in history:
            WriteSummary(y, 1, access)
            y += 1
