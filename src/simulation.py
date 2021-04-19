'''
Project     : Replacement Policy Simulation
File name   : simulation.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the simulation class that will
              run all simulations
'''

import sys, threading, logging
from cache      import Cache
from summary    import Summary
from config     import cache_config
from arguments  import RandomMem

class Simulation():
    """ This class defines the simulation environment """

    def __init__(self):
        self.PrintConfiguration()
        self.SimConfig()
        self.RunSims()

    def PrintConfiguration(self):
        """ Prints build configuration to command line """

        print('\nCache Configuration...\n')
        print('Memory Type  :', cache_config['mem_type'])
        print('Cache Size   :', cache_config['cache_size'], 'bytes')
        print('Line Size    :', cache_config['line_size'], 'bytes')
        print('Address Size :', cache_config['address_size'], 'bits')

        print('\n---------------------------------------\n')

    def SimConfig(self):
        """ Setup and process simulation """

        self.sim_configs = []

        self.sim_configs.append(Cache(config_name='LRU Cache (2-way)',  repl='LRU',     ways=2))
        self.sim_configs.append(Cache(config_name='RR Cache (2-way)',   repl='RR',      ways=2))
        self.sim_configs.append(Cache(config_name='LFRU Cache (2-way)', repl='LFRU',    ways=2))
        self.sim_configs.append(Cache(config_name='LFU Cache (2-way)',  repl='LFU',     ways=2))
        self.sim_configs.append(Cache(config_name='FIFO Cache (2-way)', repl='FIFO',    ways=2))
        self.sim_configs.append(Cache(config_name='MRU Cache (2-way)',  repl='MRU',     ways=2))

    def RunSims(self):
        """ Select how many sim batches will be run """

        if cache_config['mult_sims'] == 1:
            # Run single simulation
            self.RunSingle()
        else:
            # Run multiple simulations
            self.RunMultiple()

    def RunSingle(self):

        global sim_results
        sim_results = []

        StartSimulations(self.sim_configs, cache_config['memory'])

        Summary(sim_results)

    def RunMultiple(self):

        total_results = []

        global sim_results
        sim_results = []

        for i in range(0, cache_config['mult_sims']):

            # Generate new memory 
            cache_config['memory'] = RandomMem(size=cache_config['mem_size'], 
                                               max_address=cache_config['mem_range'],
                                               filename='gen_mem' + str(i+1) + '.txt',
                                               save_mem=True)

            print('Beginning simulation batch', i+1, 'of', cache_config['mult_sims'], 'using gen_mem' + str(i+1) + '.txt')

            StartSimulations(self.sim_configs, cache_config['memory'])

            # Add results together
            if total_results == []:
                total_results = sim_results.copy()
            else:
                for index in range(0, len(total_results)):
                    total_results[index]['history'] += sim_results[index]['history']
                    total_results[index]['hits']    += sim_results[index]['hits']
                    total_results[index]['misses']  += sim_results[index]['misses']

            for sim in total_results:
                name = '{:25s}'.format(sim['cache'].config_name)
                hits = '{:6s}'.format(str(sim['hits']))
                misses = '{:6s}'.format(str(sim['misses']))
                logging.info(name + ' - Hits:' + hits + '- Misses:' + misses)

            logging.info('')

            sim_results = []

        Summary(total_results)

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

    print('Running', len(sim_queue), 'simulations...\n')

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
