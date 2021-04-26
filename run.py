'''
Project     : Replacement Policy Simulation
File name   : run.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : The file contains the main functions to run
              the simulations 
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

__softwarename__  = 'Replacement Policy Simulation'
__author__        = 'Jacob Summerville, Henry Lee, Martin Lopez'
__copyright__     = 'Copyright (C) 2021 Jacob Summerville, Henry Lee, Martin Lopez'
__credits__       = ['Jacob Summerville, Henry Lee, Martin Lopez']
__version__       = '1.0.0'
__status__        = 'Development'
__doc__           = 'The Replacement Policy Simulator helps simulate a fully associative or set \
                     associative cache to estimate the hit rate for various replacement policies'

import os, sys, time

sys.path.insert(0, os.getcwd() + os.path.sep + 'src')

from src.simulation import Simulation
from src.logger import InitializeLogger
from src.arguments import ReadArguments


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
