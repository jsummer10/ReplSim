'''
Project     : Replacement Policy Simulation
File name   : replacementpolicy.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the replacement policy algorithms
              that will be used
'''

import random

class ReplacementPolicy():
    """ This class defines the replacement policy that 
        will be used in the cache
    """

    def __init__(self, repl):
        self.repl = repl

    def Replace(self, cache, address_index, usage_index):
        """ Pass to selected replacement policy """

        if self.repl == 'LRU':
            return self.LRU(cache, address_index)
        elif self.repl == 'RR':
            return self.RR(cache)
        elif self.repl == 'LFRU':
            return self.LFRU(cache, address_index, usage_index)
        elif self.repl == 'LFU':
            return self.LFU(cache, address_index, usage_index)
        elif self.repl == 'FIFO':
            return self.FIFO(cache, address_index)
        elif self.repl == 'MRU':
            return self.MRU(cache, address_index)

    def LRU(self, cache, address_index):
        """ perform a least recently used replacement """ 
        
        min_value = None
        min_index = None

        for index, line in enumerate(cache):
            if min_value is None or line[address_index]['recency_index'] < min_value:
                min_value = line[address_index]['recency_index']
                min_index = index

        return min_index

    def RR(self, cache):
        """ perform a random replacement """ 
        
        return random.randint(0, len(cache)-1)

    def LFU(self, cache, address_index, usage_index):
        """ perform a least frequently used replacement """ 
        
        # Perform least frequently used analysis
        min_used = None
        least_used_tags = []

        for key, value in usage_index[address_index].items():
            if min_used is None or value < min_used:
                min_used = value
                least_used_tags = [key]
            elif value == min_used:
                least_used_tags.append(key)

        for index, line in enumerate(cache):
            if line[address_index]['tag'] in least_used_tags:
                return index

    def LFRU(self, cache, address_index, usage_index):
        """ perform a least frequently recently used replacement """ 
        
        # Perform least frequently used analysis
        min_used = None
        least_used_tags = []

        for key, value in usage_index[address_index].items():
            if min_used is None or value < min_used:
                min_used = value
                least_used_tags = [key]
            elif value == min_used:
                least_used_tags.append(key)

        # Perform least recently used analysis
        min_value = None
        min_index = None
        for index, line in enumerate(cache):
            if line[address_index]['tag'] in least_used_tags:
                if min_value is None or line[address_index]['recency_index'] < min_value:
                    min_value = line[address_index]['recency_index']
                    min_index = index

        return min_index

    def FIFO(self, cache, address_index):
        """ perform a first in, first out replacement """ 
        
        min_value = None
        min_index = None

        for index, line in enumerate(cache):
            if min_value is None or line[address_index]['added_index'] < min_value:
                min_value = line[address_index]['added_index']
                min_index = index

        return min_index

    def MRU(self, cache, address_index):
        """ perform a most recently used replacement """ 
        
        max_value = None
        max_index = None

        for index, line in enumerate(cache):
            if max_value is None or line[address_index]['recency_index'] > max_value:
                max_value = line[address_index]['recency_index']
                max_index = index

        return max_index
