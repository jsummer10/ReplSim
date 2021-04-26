'''
Application : ReplSim
File name   : replacementpolicy.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : This file contains the replacement policy algorithms
              that will be used
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

import random, os, sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import ann

class ReplacementPolicy():
    """ This class defines the replacement policy that 
        will be used in the cache
    """

    def __init__(self, repl):
        self.repl = repl

        if repl == 'LRUML':
            self.GetMLPrediction()
            self.ml_counter = 0

    def GetMLPrediction(self):

        os.chdir("mem/")
        self.ml_list = ann.main()
        os.chdir("../")

    def Replace(self, cache, address_index, usage_index, new_addr):
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
        elif self.repl == 'LRUML':
            return self.LRUML(cache, address_index, new_addr)

    def LRU(self, cache, address_index):
        """ perform a least recently used replacement """ 
        
        min_value = None
        min_index = None

        for index, line in enumerate(cache):
            if min_value is None or line[address_index]['recency_index'] < min_value:
                min_value = line[address_index]['recency_index']
                min_index = index

        return min_index

    def LRUML(self, cache, address_index, new_addr):
        """ perform a least recently used replacement with machine learning """ 

        min_value = None
        min_index = None

        # Don't replace an item in the cache if the address doesn't occur again 
        if new_addr in self.ml_list:
        
            # LRU replacement with an ML check 
            for index, line in enumerate(cache):
                if min_value is None or line[address_index]['recency_index'] < min_value:
    
                    if line[address_index]['tag_index'] in self.ml_list:
                        continue
    
                    min_value = line[address_index]['recency_index']
                    min_index = index
    
            # If every address in cache occurs again, run normal LRU replacement
            if min_index is None:
                for index, line in enumerate(cache):
                    if min_value is None or line[address_index]['recency_index'] < min_value:
                        min_value = line[address_index]['recency_index']
                        min_index = index

        self.ml_counter += 1 

        if self.ml_counter == 250:
            self.GetMLPrediction()
            self.ml_counter = 0

        return min_index

    def RR(self, cache):
        """ perform a random replacement """ 
        
        return random.randint(0, len(cache)-1)

    def LFU(self, cache, address_index, usage_index):
        """ perform a least frequently used replacement """ 
        
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
