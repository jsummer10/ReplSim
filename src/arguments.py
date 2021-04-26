'''
Application : ReplSim
File name   : arguments.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : This file contains the functionality to parse CLI arguments
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

import argparse, os, sys, subprocess

from genmem     import MemoryGenerator
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
    parser.add_argument('--mempattern', help='Generated memory pattern focus (normal, loops, rep, random)')
    parser.add_argument('--cachesize',  help='Cache size to be used')
    parser.add_argument('--linesize',   help='Cache line size to be used')
    parser.add_argument('--mult',       help='Run an entered number of simulations back-to-back')
    parser.add_argument('-t', '--test', help='Run tests to verify the simulator is functioning properly', action="store_true")

    return parser.parse_args()

def MemFromFile(filename):
    cache_config['mem_src'] = 'File'
    return Parse(filename)

def RandomMem(size, max_address, filename, pattern_type='normal', save_mem=False):
    cache_config['mem_src'] = 'Generated'
    gen_mem = MemoryGenerator()
    return gen_mem.GenerateMemory(size, max_address, filename, pattern_type, save_mem)

def IsTest(args):
    if args.test:

        # Remove all arguments
        while len(sys.argv) > 1:
            sys.argv.pop()

        subprocess.run(['python3', 'test/replsimtests.py', '-v'])
        print('')
        sys.exit()

def ProcessCacheSize(args):
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

def ProcessLineSize(args):
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

def ProcessMulti(args):
    if args.mult:

        try:
            multiple = int(args.mult)
        except:
            print('Unable to convert mult (', args.mult, ') to an integer')
            sys.exit()

        if multiple < 1:
            print('Mult has to be greater than or equal to zero')
            sys.exit()

        cache_config['mult_sims'] = multiple      

def ProcessMemPattern(args):
    if args.mempattern:
    
        try:
            mempattern = args.mempattern.lower().strip()
        except:
            print('Unable to read', args.mempattern)
            sys.exit()

        if mempattern == 'normal':
            cache_config['mem_pattern'] = mempattern
        elif mempattern == 'loops':
            cache_config['mem_pattern'] = mempattern
        elif mempattern == 'rep':
            cache_config['mem_pattern'] = mempattern
        elif mempattern == 'random':
            cache_config['mem_pattern'] = mempattern
        else:
            print(args.mempattern, 'is not an option. Enter normal, loops, rep, or random')
            sys.exit()

def ProcessMemFile(args):
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

            cache_config['mem_size']  = memsize
            cache_config['mem_range'] = memrange

        elif args.memsize and not args.memrange:
            try:
                memsize = int(args.memsize)
            except:
                print('Unable to convert', args.memsize, 'to an integer')
                sys.exit()

            cache_config['mem_size']  = memsize
            cache_config['mem_range'] = DEFAULT_MEMRANGE

        elif not args.memsize and args.memrange:
            try:
                memrange = int(args.memrange)
            except:
                print('Unable to convert', args.memrange, 'to an integer')
                sys.exit()

            cache_config['mem_size']  = DEFAULT_MEMSIZE
            cache_config['mem_range'] = memrange

        else:
            cache_config['mem_size']  = DEFAULT_MEMSIZE
            cache_config['mem_range'] = DEFAULT_MEMRANGE

        cache_config['memory']  = RandomMem(size=cache_config['mem_size'], 
                                            max_address=cache_config['mem_range'], 
                                            pattern_type=cache_config['mem_pattern'],
                                            filename='gen_mem.csv',
                                            save_mem=True)

def ReadArguments():
    """ Read in command line arguments """

    args = ParseArguments()

    IsTest(args)
    ProcessCacheSize(args)
    ProcessLineSize(args)
    ProcessMulti(args)
    ProcessMemPattern(args)
    ProcessMemFile(args)
    

