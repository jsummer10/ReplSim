'''
Project     : Replacement Policy Simulation
File name   : run.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains the main functions to run
              the simulations 
'''

import os,sys
sys.path.insert(0, os.getcwd() + os.path.sep + 'src')

from simulation import Simulation
from fileparser import Parse
from genmem     import GenRandomAccesses
from summary    import CreateWorkbook, CloseWorkbook
from logger     import InitializeLogger

def MemFromFile(filename):
    return Parse('mem/sample_mem.txt')

def RandomMem(size, max_address, save_mem=False):
    return GenRandomAccesses(100, max_address, save_mem)

def main():

    InitializeLogger()

    mem_accesses = RandomMem(100, 100, True)

    CreateWorkbook()

    Simulation(mem_accesses)

    CloseWorkbook()

if __name__ == '__main__':
    main()