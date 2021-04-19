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

class Simulation():
    """ This class defines the simulation environment """

    def __init__(self):
        self.PrintConfiguration()
        self.SimConfig()
        self.Run()

    def PrintConfiguration(self):
        """ Prints build configuration to command line """

        print('Cache Configuration...')
        print('Memory Type:', cache_config['mem_type'])
        print('Cache Size:', cache_config['cache_size'], 'bytes')
        print('Line Size:', cache_config['line_size'], 'bytes')
        print('Address Size:', cache_config['address_size'], 'bits')

    def SimConfig(self):
        """ Setup and process simulation """

        self.sim_configs = []

        self.sim_configs.append(Cache(config_name='LRU Cache (2-way)',   repl='LRU',     ways=2))
        self.sim_configs.append(Cache(config_name='RR Cache (2-way)',    repl='RR',      ways=2))
        self.sim_configs.append(Cache(config_name='LFRU Cache (2-way)',  repl='LFRU',    ways=2))
        self.sim_configs.append(Cache(config_name='LFU Cache (2-way)',   repl='LFU',     ways=2))

        self.sim_configs.append(Cache(config_name='LRU Cache (4-way)',   repl='LRU',     ways=4))
        self.sim_configs.append(Cache(config_name='RR Cache (4-way)',    repl='RR',      ways=4))
        self.sim_configs.append(Cache(config_name='LFRU Cache (4-way)',  repl='LFRU',    ways=4))
        self.sim_configs.append(Cache(config_name='LFU Cache (4-way)',   repl='LFU',     ways=4))

    def Run(self):

        global sim_results
        sim_results = []

        StartSimulations(self.sim_configs, cache_config['memory'])

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
