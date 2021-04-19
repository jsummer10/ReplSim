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
        #self.Setup()
        self.Run()

    def Setup(self):
        self.mem_accesses = RandomMem(cache_config['mem_size'], cache_config['mem_max'])

    def Run(self):
        """ Setup and process simulation """

        sim_configs = []

        #--------------------------------
        # Start of Simulations to be run
        #--------------------------------

        sim_configs.append(Cache(config_name='LRU Cache (2-way)',   repl='LRU',     ways=2))
        sim_configs.append(Cache(config_name='RR Cache (2-way)',    repl='RR',      ways=2))
        sim_configs.append(Cache(config_name='LFRU Cache (2-way)',  repl='LFRU',    ways=2))
        sim_configs.append(Cache(config_name='LFU Cache (2-way)',   repl='LFU',     ways=2))

        sim_configs.append(Cache(config_name='LRU Cache (4-way)',   repl='LRU',     ways=4))
        sim_configs.append(Cache(config_name='RR Cache (4-way)',    repl='RR',      ways=4))
        sim_configs.append(Cache(config_name='LFRU Cache (4-way)',  repl='LFRU',    ways=4))
        sim_configs.append(Cache(config_name='LFU Cache (4-way)',   repl='LFU',     ways=4))

        #--------------------------------
        #  End of Simulations to be run
        #--------------------------------

        global sim_results
        sim_results = []

        StartSimulations(sim_configs, cache_config['memory'])

        sim_summary = Summary(sim_results)

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
