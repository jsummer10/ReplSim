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

def GenRandomAccesses(size, max_address, save_mem):

    mem_accesses = []

    for i in range(0, size):
        mem_accesses.append(4 * random.randint(0, max_address))

    if save_mem:
        SaveToFile(mem_accesses)

    return mem_accesses

def SaveToFile(data):
    f = open("mem/random_mem.txt", "w")

    for item in data:
        f.write(str(item) + '\n')

    f.close()
