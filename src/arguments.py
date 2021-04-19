'''
Project     : Replacement Policy Simulation
File name   : arguments.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : This file contains the functionality to parse CLI arguments
'''

import argparse, os, sys

from genmem     import GenRandomAccesses
from fileparser import Parse
from config     import cache_config

__doc__ = 'The Replacement Policy Simulator helps simulate a fully associative or set \
           associative cache to estimate the hit rate for various replacement policies'

DEFAULT_MEMSIZE  = 2000
DEFAULT_MEMRANGE = 2000

b  = 1
B  = 1
KB = 1024
MB = 1048576
GB = 1073741824

def ParseArguments():
    """ Parses the command line arguments and returns the parser. """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-f', '--file', help='Text file to be used (e.g. mem/sample_mem.txt)')
    parser.add_argument('--memsize',    help='Memory size of generated memory')
    parser.add_argument('--memrange',   help='Max range of memory in generated memory')
    parser.add_argument('--cachesize',  help='Cache size to be used')
    parser.add_argument('--linesize',   help='Cache line size to be used')

    return parser.parse_args()

def MemFromFile(filename):
    cache_config['mem_type'] = 'File'
    return Parse('mem/sample_mem.txt')

def RandomMem(size, max_address, save_mem=False):
    cache_config['mem_type'] = 'Generated'
    return GenRandomAccesses(size, max_address, save_mem)

def ReadArguments():
    """ Read in command line arguments """

    args = ParseArguments()

    # Read in text file for memory using CLI argument
    if args.file:
        if(os.path.isfile(args.file)):
            cache_config['memory'] = MemFromFile(args.file)
        else:
            print('Unable to open', args.file)
            sys.exit()

    # Generate random memory using CLI arguments
    if not args.file:
        if args.memsize and args.memrange:

            try:
                memsize = int(args.memsize)
            except:
                print('Unable to convert', args.memsize, 'to an integer')
                sys.exit()

            try:
                memrange = int(args.memrange)
            except:
                print('Unable to convert', args.memrange, 'to an integer')
                sys.exit()

            cache_config['memory'] = RandomMem(size=memsize, max_address=memrange)

        if args.memsize and not args.memrange:
            try:
                memsize = int(args.memsize)
            except:
                print('Unable to convert', args.memsize, 'to an integer')
                sys.exit()

            cache_config['memory'] = RandomMem(size=memsize, max_address=DEFAULT_MEMRANGE)

        if not args.memsize and args.memrange:
            try:
                memrange = int(args.memrange)
            except:
                print('Unable to convert', args.memrange, 'to an integer')
                sys.exit()

            cache_config['memory'] = RandomMem(size=DEFAULT_MEMSIZE, max_address=memrange)

    # Generate random memory using defaults
    if not args.file and not args.memsize and not args.memrange:
        cache_config['memory'] = RandomMem(size=DEFAULT_MEMSIZE, max_address=DEFAULT_MEMRANGE)

    # Set cache size using CLI argument
    if args.cachesize:

        if isinstance(args.cachesize, int):
            cache_config['cache_size'] = args.cachesize

        else:
            cache_size = args.cachesize.lower().strip()

            if 'b' in cache_size:
                cache_size = cache_size.replace('b', '')

            if 'k' in cache_size:

                cache_size = cache_size.replace('k', '')

                try:
                    cache_size = int(cache_size)
                except:
                    print('Unable to understand the cache size of', args.cachesize)
                    sys.exit()

                cache_config['cache_size'] = cache_size * KB

            elif 'm' in cache_size:

                cache_size = cache_size.replace('m', '')

                try:
                    cache_size = int(cache_size)
                except:
                    print('Unable to understand the cache size of', args.cachesize)
                    sys.exit()

                cache_config['cache_size'] = cache_size * MB

            elif 'g' in cache_size:

                cache_size = cache_size.replace('g', '')

                try:
                    cache_size = int(cache_size)
                except:
                    print('Unable to understand the cache size of', args.cachesize)
                    sys.exit()

                cache_config['cache_size'] = cache_size * GB

            else:
                print('Unable to understand the cache size of', args.cachesize)
                sys.exit()

    # Set line size using CLI argument
    if args.linesize:

        if isinstance(args.linesize, int):
            cache_config['line_size'] = args.linesize

        else:
            line_size = args.linesize.lower().strip()

            if 'b' in line_size:
                line_size = line_size.replace('b', '')

            if 'k' in line_size:

                line_size = line_size.replace('k', '')

                try:
                    line_size = int(line_size)
                except:
                    print('Unable to understand the line size of', args.linesize)
                    sys.exit()

                cache_config['line_size'] = line_size * KB

            elif 'm' in line_size:

                line_size = line_size.replace('m', '')

                try:
                    line_size = int(line_size)
                except:
                    print('Unable to understand the line size of', args.linesize)
                    sys.exit()

                cache_config['line_size'] = line_size * MB

            elif 'g' in line_size:

                line_size = line_size.replace('g', '')

                try:
                    line_size = int(line_size)
                except:
                    print('Unable to understand the line size of', args.linesize)
                    sys.exit()

                cache_config['line_size'] = line_size * GB

            else:
                print('Unable to understand the line size of', args.linesize)
                sys.exit()





