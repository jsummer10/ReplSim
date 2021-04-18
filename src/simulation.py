'''
Project     : Replacement Policy Simulation
File name   : simulation.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the simulation class that will
              run all simulations
'''

from cache      import Cache
from summary    import CreateSummarySheet, WriteSummaryData, CreateCacheSheet

class Simulation():
    """ This class defines the simulation environment """

    def __init__(self, mem_accesses):
        self.mem_accesses = mem_accesses

        self.Run()

    def Run(self):
        """ Run simulation """

        CreateSummarySheet()
        CreateCacheSheet()

        self.LRUSim()
        self.RandomSim()

    def LRUSim(self):
        """ Run LRU Simulation """

        cache = Cache('LRU')

        self.misses = 0
        self.hits   = 0

        history = []

        for access in self.mem_accesses:
            if cache.L1CacheAccess(access):
                self.hits += 1
                history.append([hex(access), 'Hit'])
            else:
                self.misses += 1
                history.append([hex(access), 'Miss'])

        cache.WriteCache(1, 'LRU Cache')
        self.WriteStats(1, history, 'LRU Stats')

    def RandomSim(self):
        """ Run Random Simulation """

        cache = Cache('Random')

        self.misses = 0
        self.hits   = 0

        history = []

        for access in self.mem_accesses:
            if cache.L1CacheAccess(access):
                self.hits += 1
                history.append([hex(access), 'Hit'])
            else:
                self.misses += 1
                history.append([hex(access), 'Miss'])

        cache.WriteCache(4, 'Random Cache')
        self.WriteStats(4, history, 'Random Stats')

    def WriteStats(self, x, history, title):
        """ Prints simulation statistics """ 

        hit_rate = self.hits / (self.misses + self.hits)

        WriteSummaryData(1, x, [title])

        WriteSummaryData(2, x, ['Hits:', self.hits])
        WriteSummaryData(3, x, ['Misses:', self.misses])
        WriteSummaryData(4, x, ['Hit Rate:', '{:0.2f}%'.format(hit_rate * 100)])

        y = 6

        for access in history:
            WriteSummaryData(y, x, access)
            y += 1
