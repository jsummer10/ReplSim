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

    def Replace(self, cache):
        """ Pass to selected replacement policy """

        if self.repl == 'LRU':
            return self.LRU(cache)
        elif self.repl == 'Random':
            return self.Random(cache)

    def LRU(self, cache):
        """ perform a least recently used replacement """ 
        
        min_value = cache[0][0]
        
        for line in cache:
            if line[0] < min_value:
                min_value = line[0]

        for index, line in enumerate(cache):
            if line[0] == min_value:
                return index

    def Random(self, cache):
        """ perform a random replacement """ 
        
        return random.randint(0, len(cache)-1)
