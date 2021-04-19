'''
Project     : Replacement Policy Simulation
File name   : cache.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the cache class which will 
              store the current state of the cache
'''

import sys, math, logging
from replacementpolicy  import ReplacementPolicy
from config             import cache_config

class Cache():
    """ This class defines the cache that will be simulated """

    def __init__(self, config_name, repl, ways):
        self.config_name = config_name
        self.Configure(repl, ways)

    def Configure(self, repl, ways):
        """ Configure cache """

        self.address_size   = cache_config['address_size']
        self.cache_size     = cache_config['cache_size']
        self.line_size      = cache_config['line_size']

        self.ways           = int(ways)
        self.offset_bits    = int(math.log(self.line_size, 2))   # Log base 2 of line size
        self.index_bits     = int(math.log(self.ways, 2))        # Log base 2 of ways
        self.tag_bits       = int(self.address_size - self.offset_bits - self.index_bits)

        self.repl           = repl
        self.repl_policy    = ReplacementPolicy(repl)

        amount_tags = int((self.cache_size / self.line_size) / self.ways) 

        # Set up empty cache
        self.cache = []
        for tags in range(0, amount_tags):
            way_list = []
            for i in range(0, self.ways):
                way_list.append(None)
            self.cache.append(way_list)

        self.LogConfig()

        self.usage_index = []
        for i in range(0, self.ways):
            self.usage_index.append(dict())

        self.recency_index = 1
        self.added_index = 1

    def L1CacheAccess(self, address):
        """ Access the cache """

        address_bits = '{0:032b}'.format(address)

        address_tag    = int(address_bits[0 : self.tag_bits], 2)
        address_offset = int(address_bits[self.tag_bits + self.index_bits : ], 2)

        if self.ways == 1:
            address_index = 0
        else:
            address_index  = int(address_bits[self.tag_bits : self.tag_bits + self.index_bits], 2)

        self.LogCache(address_tag)

        # Check if tag is in cache
        for index, line in enumerate(self.cache):

            if line[address_index] is None:
                continue

            if address_tag == line[address_index]['tag']:
                self.cache[index][address_index]['tag'] = self.recency_index
                self.recency_index += 1

                if address_tag in self.usage_index[address_index].keys():
                    self.usage_index[address_index][address_tag] += 1
                else:
                    self.usage_index[address_index][address_tag] = 1

                return True

        #-------------------------
        # Address is not in cache
        #-------------------------

        # Check if any line is empty 
        for index, line in enumerate(self.cache):
            if line[address_index] is None:
                # Get value from memory

                cache_line = { 'recency_index'  : self.recency_index, 
                               'added_index'    : self.added_index,
                               'tag'            : address_tag }

                self.cache[index][address_index] = cache_line  

                if address_tag in self.usage_index[address_index].keys():
                    self.usage_index[address_index][address_tag] += 1
                else:
                    self.usage_index[address_index][address_tag] = 1
            
                self.added_index += 1
                self.recency_index += 1
                return False

        repl_index = self.repl_policy.Replace(self.cache, address_index, self.usage_index)

        if repl_index is None:
            return False

        # Replace the specified index
        cache_line = { 'recency_index':  self.recency_index, 
                       'added_index'    : self.added_index,
                       'tag': address_tag }

        self.cache[repl_index][address_index] = cache_line

        if address_tag in self.usage_index[address_index].keys():
            self.usage_index[address_index][address_tag] += 1
        else:
            self.usage_index[address_index][address_tag] = 1

        self.added_index += 1
        self.recency_index += 1
        return False

    def PrintCache(self):
        """ Prints the values in the cache """

        print('\nCache: \n')

        for way in range(0,len(self.cache[0])):
            print('{:10s} | '.format('set ' + str(way)), end='')

        print()

        for way in range(0,len(self.cache[0])):
            print('{:10s} | '.format('----------'), end='')

        print()

        for line in self.cache:
            for way in range(0,len(line)):
                if line[way]['tag'] is None:
                    print('{:10s} | '.format('empty'), end='')
                else:
                    print('{:10s} | '.format(hex(line[way]['tag'])), end='')

            print()

        print()

    def LogCache(self, tag):
        """ Log every cache access """

        logging.info('New Address: ' + hex(tag))

        logging.info('')
        logging.info('Cache:')
        logging.info('')

        log_string = '' 

        for way in range(0,len(self.cache[0])):
            log_string += '{:10s} | '.format('set ' + str(way))

        logging.info(log_string[:-2]) 
        log_string = '' 

        for way in range(0,len(self.cache[0])):
            log_string += '{:10s} | '.format('----------')

        logging.info(log_string[:-2]) 
        log_string = '' 

        for line in self.cache:
            for way in range(0,len(line)):
                if line[way] is None:
                    log_string += '{:10s} | '.format('empty')
                else:
                    log_string += '{:10s} | '.format(hex(line[way]['tag']))

            logging.info(log_string[:-2]) 
            log_string = '' 

        log_string = '' 

        logging.info('')
        for way in range(0,len(self.cache[0])):
            log_string += '------------------'

        logging.info(log_string) 
        logging.info('')

    def LogConfig(self):
        """ Log cache configuration """

        logging.info('')
        logging.info('Cache Config...')
        logging.info('')

        logging.info('Cache Size         : ' + str(self.cache_size) + ' bytes')
        logging.info('Line Size          : ' + str(self.line_size) + ' bytes')

        if self.ways == 1:
            logging.info('Associativity      : Fully Associative')
        else:
            logging.info('Associativity      : ' + str(self.ways) + '-Way Set Associative')

        logging.info('Replacement Policy : ' + str(self.repl))

        logging.info('')

        logging.info('Address Size       : ' + str(self.address_size) + ' bits')
        logging.info('Tag Size           : ' + str(self.tag_bits) + ' bits')
        logging.info('Index Size         : ' + str(self.index_bits) + ' bits')
        logging.info('Offset Size        : ' + str(self.offset_bits) + ' bits')

        logging.info('')
        logging.info('------------------------------------')
        logging.info('')



