'''
Project     : Replacement Policy Simulation
File name   : simulation.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the simulation class that will
              run all simulations
'''

import sys
from cache      import Cache
from summary    import Summary

class Simulation():
    """ This class defines the simulation environment """

    def __init__(self, mem_accesses):
        self.mem_accesses = mem_accesses

        self.Run()

    def Run(self):
        """ Run simulation """

        sim_list = []

        sim_list.append(self.LRUSim())
        sim_list.append(self.RandomSim())

        sim_summary = Summary(sim_list)

    def LRUSim(self):
        """ Run LRU Simulation """

        cache = Cache(config_name='LRU Cache', repl='LRU', ways=2)

        misses = 0
        hits   = 0

        history = []

        for access in self.mem_accesses:
            if cache.L1CacheAccess(access):
                hits += 1
                history.append([hex(access), 'Hit'])
            else:
                misses += 1
                history.append([hex(access), 'Miss'])

        sim_data = { 'sim_name' : 'LRU Cache', 
                     'history'  : history, 
                     'cache'    : cache,
                     'hits'     : hits,
                     'misses'   : misses }

        return sim_data

    def RandomSim(self):
        """ Run RR Simulation """

        cache = Cache(config_name='RR Cache', repl='Random', ways=2)

        misses = 0
        hits   = 0

        history = []

        for access in self.mem_accesses:
            if cache.L1CacheAccess(access):
                hits += 1
                history.append([hex(access), 'Hit'])
            else:
                misses += 1
                history.append([hex(access), 'Miss'])

        sim_data = { 'sim_name' : 'RR Cache', 
                     'history'  : history, 
                     'cache'    : cache,
                     'hits'     : hits,
                     'misses'   : misses }

        return sim_data

