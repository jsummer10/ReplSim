'''
Project     : Replacement Policy Simulation
File name   : logger.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the functionality for logging
'''

import datetime, logging, os

def InitializeLogger():
    """ Initialize Logger """

    today = datetime.datetime.now()

    if not os.path.isdir('logs/'):
        os.mkdir('logs/')

    log_file = 'logs/' + today.strftime("%Y%m%d_%H%M%S") + '.log'

    logging.basicConfig(filename=log_file, 
                        format='%(asctime)s - %(levelname)s: %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    logging.info('--- Beginning Simulations ---')
    logging.info('')