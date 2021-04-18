'''
Project     : Replacement Policy Simulation
File name   : simulation.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the simulation class that will
              run all simulations
'''

import sys, threading
from cache      import Cache
from summary    import Summary
from genmem     import GenRandomAccesses
from fileparser import Parse
from config     import cache_config

def MemFromFile(filename):
    return Parse('mem/sample_mem.txt')

def RandomMem(size, max_address, save_mem=False):
    return GenRandomAccesses(size, max_address, save_mem)

class Simulation():
    """ This class defines the simulation environment """

    def __init__(self):
        self.Setup()
        self.Run()

    def Setup(self):
        self.mem_accesses = RandomMem(cache_config['mem_size'], cache_config['mem_max'])

    def Run(self):
        """ Setup and process simulation """

        sim_configs = []

        sim_configs.append(self.LRUSim())
        sim_configs.append(self.RRSim())
        sim_configs.append(self.LFRUSim())
        sim_configs.append(self.LFUSim())

        global sim_results
        sim_results = []

        StartSimulations(sim_configs, self.mem_accesses)

        sim_summary = Summary(sim_results)

    def LRUSim(self):
        """ Sim with LRU, 2-way set associative """
        return Cache(config_name='LRU Cache', repl='LRU', ways=4)

    def RRSim(self):
        """ Sim with RR, 2-way set associative """
        return Cache(config_name='RR Cache', repl='RR', ways=4)

    def LFRUSim(self):
        """ Sim with LFRU, 2-way set associative """
        return Cache(config_name='LFRU Cache', repl='LFRU', ways=4)

    def LFUSim(self):
        """ Sim with LFU, 2-way set associative """
        return Cache(config_name='LFU Cache', repl='LFU', ways=4)


class myThread (threading.Thread):
    """ This class enables multithreading capabilities """

    def __init__(self, threadID, name, counter, sim, mem_accesses):
        threading.Thread.__init__(self)
        self.threadID     = threadID
        self.name         = name
        self.counter      = counter
        self.sim          = sim
        self.mem_accesses = mem_accesses

    def run(self):
        Simulate(self.sim, self.mem_accesses)

def StartSimulations(sim_queue, mem_accesses):
    """ Guide multithreaded simulations """

    threads = []

    print('\nBeginning', len(sim_queue), 'simulations...\n')

    count = 1
    for sim in sim_queue:
        thread = myThread(count, 'Thread-' + str(count), count, sim, mem_accesses)
        thread.start()
        threads.append(thread)
        count += 1

    for thread in threads:
        thread.join()

def Simulate(cache, mem_accesses):
    """ Run simulation """

    misses = 0
    hits   = 0

    history = []

    for access in mem_accesses:
        if cache.L1CacheAccess(access):
            hits += 1
            history.append([hex(access), 'Hit'])
        else:
            misses += 1
            history.append([hex(access), 'Miss'])

    sim_data = { 'history'  : history, 
                 'cache'    : cache,
                 'hits'     : hits,
                 'misses'   : misses }

    sim_results.append(sim_data)
