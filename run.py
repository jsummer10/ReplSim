'''
Project     : Replacement Policy Simulation
File name   : run.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains the main functions to run
              the simulations 
'''

__softwarename__    = 'Replacement Policy Simulation'
__author__          = 'Jake Summerville, Henry Lee, Martin Lopez, Fausto Sanchez'
__copyright__       = 'Copyright (C) 2021 Jake Summerville, Henry Lee, Martin Lopez, Fausto Sanchez'
__credits__         = ['Jake Summerville, Henry Lee, Martin Lopez, Fausto Sanchez']
__version__         = '1.0.0'
__status__          = 'Development'
__doc__             = 'The Replacement Policy Simulator helps simulate a fully associative or set \
                       associative cache to estimate the hit rate for various replacement policies'

import os,sys, time
sys.path.insert(0, os.getcwd() + os.path.sep + 'src')

from src.simulation import Simulation
from src.logger     import InitializeLogger
from src.arguments  import ReadArguments

def main():

    # Save initial start time 
    start_time = time.time()

    InitializeLogger()
  
    ReadArguments()

    Simulation()

    time_dif = (time.time() - start_time) / 60

    print('\nTesting Complete ({:.2f} minutes)\n'.format(time_dif))

if __name__ == '__main__':
    main()