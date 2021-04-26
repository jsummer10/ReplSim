'''
Application : ReplSim
File name   : simulation.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : This file contains the simulation class that will
              run all simulations
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

        if cache_config['mem_pattern'] == 'normal':
            self.mem_pattern = 'Normal'
        elif cache_config['mem_pattern'] == 'loops':
            self.mem_pattern = 'Heavy Loops'
        elif cache_config['mem_pattern'] == 'rep':
            self.mem_pattern = 'Heavy Repetition'
        elif cache_config['mem_pattern'] == 'random':
            self.mem_pattern = 'Random'

        print('\nCache Configuration...\n')
        print('Memory Source  :', cache_config['mem_src'])
        print('Memory Pattern :', self.mem_pattern)
        print('Cache Size     :', cache_config['cache_size'], 'bytes')
        print('Line Size      :', cache_config['line_size'], 'bytes')
        print('Address Size   :', cache_config['address_size'], 'bits')

        print('\n---------------------------------------\n')

    def SimConfig(self):
        """ Setup and process simulation """

        self.sim_configs = []

        self.title = '2-Way Set Associative Replacement Policy Comparison (' + self.mem_pattern + ')'

        self.sim_configs.append(Cache(config_name='LRU Cache (2-way)',   repl='LRU',     ways=2))
        self.sim_configs.append(Cache(config_name='RR Cache (2-way)',    repl='RR',      ways=2))
        self.sim_configs.append(Cache(config_name='LFRU Cache (2-way)',  repl='LFRU',    ways=2))
        self.sim_configs.append(Cache(config_name='LFU Cache (2-way)',   repl='LFU',     ways=2))
        self.sim_configs.append(Cache(config_name='FIFO Cache (2-way)',  repl='FIFO',    ways=2))
        self.sim_configs.append(Cache(config_name='MRU Cache (2-way)',   repl='MRU',     ways=2))
        self.sim_configs.append(Cache(config_name='LRUML Cache (2-way)', repl='LRUML',   ways=2))

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

        Summary(sim_results, self.title)

    def RunMultiple(self):

        total_results = []

        global sim_results
        sim_results = []

        for i in range(0, cache_config['mult_sims']):

            # Generate new memory 
            cache_config['memory'] = RandomMem(size=cache_config['mem_size'], 
                                               max_address=cache_config['mem_range'],
                                               filename='gen_mem' + str(i+1) + '.csv',
                                               pattern_type=cache_config['mem_pattern'],
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

        Summary(total_results, self.title)

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
