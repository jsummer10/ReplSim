'''
Project     : Replacement Policy Simulation
File name   : config.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the cache configuration
'''

import sys, argparse

b  = 1
B  = 1
KB = 1024
MB = 1048576
GB = 1073741824

class CacheConfig(dict):
    """ This class sets the cache configuration """
    def __init__(self):
        self.cache_config = { 'memory'        : None,
                              'mem_type'      : '',
                              'mem_size'      : None,
                              'mem_range'     : None,
                              'address_size'  : 32 * b,
                              'cache_size'    : 64 * KB,
                              'line_size'     : 32 * B,
                              'mult_sims'     : 1,
                            }

    def __getitem__(self, key):
        return self.cache_config[key]

    def __setitem__(self, key, value):
        if key not in self.cache_config.keys():
            print("\nKeyError: '{}' does not exist in settings".format(key))
            print('The following keys exist:')
            print('\tmemory')
            print('\tmem_type')
            print('\tmem_range')
            print('\tmem_size')
            print('\tmem_range')
            print('\taddress_size')
            print('\tcache_size')
            print('\tline_size')
            print('\tmult_sims')
            
            sys.exit()

        self.cache_config[key] = value

cache_config = CacheConfig()
