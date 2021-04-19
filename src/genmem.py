'''
Project     : Replacement Policy Simulation
File name   : genmem.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains functionality to generate 
              random memory access values of any size
'''

import random

class MemoryGenerator():
    """ This class will generate a memory file to be used """

    def __init__(self):
        self.memory = []

    def GenerateMemory(self, size, max_address, save_mem):
        """ Generates a list of random memory addresses to use """

        self.size = size
        self.max_address = max_address

        self.memory = []

        self.InitialMemory()

        self.InjectRandomLoop(num_loops=int(self.size / 40), loop_size=6)

        self.InjectIncrementLoop(num_loops=int(self.size / 40), loop_size=8, increment=4)
        self.InjectIncrementLoop(num_loops=int(self.size / 40), loop_size=8, increment=12)

        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))
        self.InjectRepetition(int(self.size / 40))

        if save_mem:
            self.SaveToFile()

        return self.memory

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

    def SaveToFile(self):
        """ Save memory list as a txt file for later use """

        f = open("mem/random_mem.txt", "w")

        for item in self.memory:
            f.write(str(item) + '\n')

        f.close()

    if __name__ == '__main__':

        size = 100
        max_address = 100
        save_mem = True

        GenRandomAccesses(size, max_address, save_mem)
