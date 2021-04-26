'''
Application : ReplSim
File name   : genmem.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : The file contains functionality to generate 
              random memory access values of any size
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

import random, os, math
from config import cache_config

class MemoryGenerator():
    """ This class will generate a memory file to be used """

    def __init__(self):
        self.memory = []

    def GenerateMemory(self, size, max_address, filename, pattern_type, save_mem):
        """ Generates a list of random memory addresses to use """

        self.size = size
        self.max_address = max_address

        self.memory = []

        self.InitialMemory()

        if pattern_type == 'normal':
            self.NormalPatterns()
        elif pattern_type == 'loops':
            self.LoopPattern()
        elif pattern_type == 'rep':
            self.RepPattern()
        elif pattern_type == 'random':
            pass # Add nothing

        if save_mem:
            self.SaveToFile(filename)

        return self.memory

    def NormalPatterns(self):
        self.InjectRandomLoop(num_loops=int(self.size / 40), loop_size=6)
        self.InjectRandomLoop(num_loops=int(self.size / 40), loop_size=3)

        self.InjectIncrementLoop(num_loops=int(self.size / 40), loop_size=15, increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 40), loop_size=8,  increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 40), loop_size=6,  increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 40), loop_size=11, increment=12)

        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))

    def LoopPattern(self):
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))

        self.InjectRandomLoop(num_loops=int(self.size / 20), loop_size=6)
        self.InjectRandomLoop(num_loops=int(self.size / 20), loop_size=4)
        self.InjectRandomLoop(num_loops=int(self.size / 20), loop_size=7)

        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=8,  increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=12, increment=12)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=9,  increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=20, increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=4,  increment=8)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=5,  increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=7,  increment=24)

    def RepPattern(self):
        self.InjectRandomLoop(num_loops=int(self.size / 20), loop_size=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=8, increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 20), loop_size=6, increment=4)

        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))
        self.InjectRepetition(int(self.size / 20))

    def InitialMemory(self):
        """ Generates a list of random numbers from 0 to max_address """
        for i in range(0, self.size):
            self.memory.append(4 * random.randint(0, self.max_address))

    def InjectRandomLoop(self, num_loops, loop_size):
        """ Inject a loop of random values into memory """

        loop = []

        for i in range(0, loop_size):
            loop.append(4 * random.randint(0, self.max_address))

        for i in range(0, num_loops):
            random_index = random.randint(0, self.size - loop_size - 1)

            for x in range(0, loop_size):
                self.memory[random_index + x] = loop[x]

    def InjectIncrementLoop(self, num_loops, loop_size, increment):
        """ Inject a loop of incremented values into memory """

        loop = []

        first_loop_value = 4 * random.randint(0, self.max_address)

        for i in range(0, loop_size):
            loop.append(first_loop_value + (i * increment))

        for i in range(0, num_loops):
            random_index = random.randint(0, self.size - loop_size - 1)

            for x in range(0, loop_size):
                self.memory[random_index + x] = loop[x]

    def InjectRepetition(self, num_occur):

        index = random.randint(0, self.size - 1)
        value = 4 * random.randint(0, self.max_address)

        for i in range(0, num_occur):
            self.memory[index] = value

    def SaveToFile(self, filename):
        """ Save memory list as a txt file for later use """

        if not os.path.isdir('mem/'):
            os.mkdir('mem/')

        f = open('mem/' + filename, "w")

        for item in self.memory:
            # Get tag + index bits
            address_bits   = '{0:032b}'.format(item)
            offset_bits    = int(math.log(cache_config['line_size'], 2))
            address_tag    = int(address_bits[0 : -offset_bits], 2)

            # write to file
            f.write(str(item) + ', ' + str(address_tag) + '\n')

        f.close()

    if __name__ == '__main__':

        size = 100
        max_address = 100
        save_mem = True

        GenRandomAccesses(size, max_address, save_mem)
