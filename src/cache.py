'''
Project     : Replacement Policy Simulation
File name   : cache.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the cache class which will 
              store the current state of the cache
'''

import sys
from replacementpolicy  import ReplacementPolicy
from summary            import CreateCacheSheet

class Cache():
    """ This class defines the cache that will be simulated """

    def __init__(self):
        self.Configure()

    def Configure(self):
        """ Configure cache """

        # Values in bytes
        self.cache_size   = 32  # Has to be power of 2
        self.line_size    = 4   # Has to be power of 2 and less than cache size
        self.cache_index  = 1

        self.repl_policy  = ReplacementPolicy('LRU')

    def FullyAssociativeCache(self):
        """ Creates empty fully associative cache """

        amount_lines  = int(self.cache_size / self.line_size)
        words_in_line = int(self.line_size / 4)
        
        self.cache = [[None] * words_in_line] * amount_lines

    def L1CacheAccess(self, address):
        """ Access the cache """

        # Check if address is in cache
        for index, line in enumerate(self.cache):
            if address in line:
                self.cache[index][0] = self.cache_index
                self.cache_index += 1
                return True

        # Address is not in cache

        # Check if any line is empty 
        for index, line in enumerate(self.cache):
            if None in line: 
                self.cache[index] = [self.cache_index, address]    # Get value from memory

                for i in range(1, int(self.line_size / 4)):
                    self.cache[index].append(address + (i * 4))

                self.cache_index += 1
                return False

        repl_index = self.repl_policy.Replace(self.cache, address)

        if repl_index is None:
            return False

        # Replace the specified index
        self.cache[repl_index] = [self.cache_index, address]    # Get value from memory

        for i in range(1, int(self.line_size / 4)):
            self.cache[repl_index].append(address + (i * 4))

        self.cache_index += 1
        return False

    def PrintCache(self):
        """ Prints the values in the cache """

        for line in self.cache:
            for i in range(1,len(line)):
                print(hex(line[i]), end=' ')

            print()

    def WriteCache(self):
        CreateCacheSheet(self.cache)



