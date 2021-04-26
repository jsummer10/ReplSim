'''
Project     : Replacement Policy Simulation
File name   : config.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : This file contains the cache configuration
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
                              'mem_src'       : '',
                              'mem_size'      : None,
                              'mem_range'     : None,
                              'mem_pattern'   : 'normal',
                              'address_size'  : 32 * b,
                              'cache_size'    : 8 * KB,
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
