'''
Project     : Replacement Policy Simulation
File name   : replsimtests.py
Authors     : Jacob Summerville, Martin Lopez, Henry Lee
Creation    : 04/17/21
Description : The file contains the test cases for the replacement
              policy simulator
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

import unittest, sys, os, HtmlTestRunner

sys.path.insert(0, os.getcwd() + os.path.sep + 'src')

from replacementpolicy  import ReplacementPolicy

class ReplSimTests(unittest.TestCase): 
   
    def test_1_LRU(self): 
        """ Description: Test the LRU Replacement Policy """

        repl_policy    = ReplacementPolicy('LRU')

        cache = [[{'recency_index'  : 7}],
                 [{'recency_index'  : 1}],
                 [{'recency_index'  : 6}],
                 [{'recency_index'  : 11}],
                 [{'recency_index'  : 100}],
                 [{'recency_index'  : 54}],
                 [{'recency_index'  : 28}],
                 [{'recency_index'  : 10}],
                 [{'recency_index'  : 77}],
                 [{'recency_index'  : 92}],
                 [{'recency_index'  : 33}]]

        #---------------
        # Replacement 1
        #---------------

        repl_index = repl_policy.Replace(cache, 0, None)
        cache[repl_index][0] = { 'recency_index':  60 }

        if cache != [[{'recency_index'  : 7}],
                     [{'recency_index'  : 60}],
                     [{'recency_index'  : 6}],
                     [{'recency_index'  : 11}],
                     [{'recency_index'  : 100}],
                     [{'recency_index'  : 54}],
                     [{'recency_index'  : 28}],
                     [{'recency_index'  : 10}],
                     [{'recency_index'  : 77}],
                     [{'recency_index'  : 92}],
                     [{'recency_index'  : 33}]]:

            self.fail('Incorrect replacement')

        #---------------
        # Replacement 2
        #---------------

        repl_index = repl_policy.Replace(cache, 0, None)
        cache[repl_index][0] = { 'recency_index':  157 }

        if cache != [[{'recency_index'  : 7}],
                     [{'recency_index'  : 60}],
                     [{'recency_index'  : 157}],
                     [{'recency_index'  : 11}],
                     [{'recency_index'  : 100}],
                     [{'recency_index'  : 54}],
                     [{'recency_index'  : 28}],
                     [{'recency_index'  : 10}],
                     [{'recency_index'  : 77}],
                     [{'recency_index'  : 92}],
                     [{'recency_index'  : 33}]]:

            self.fail('Incorrect replacement')

        print(cache)

    def test_2_MRU(self): 
        """ Description: Test the MRU Replacement Policy """

        repl_policy    = ReplacementPolicy('MRU')

        cache = [[{'recency_index'  : 7}],
                 [{'recency_index'  : 1}],
                 [{'recency_index'  : 6}],
                 [{'recency_index'  : 11}],
                 [{'recency_index'  : 100}],
                 [{'recency_index'  : 54}],
                 [{'recency_index'  : 28}],
                 [{'recency_index'  : 10}],
                 [{'recency_index'  : 77}],
                 [{'recency_index'  : 92}],
                 [{'recency_index'  : 33}]]

        #---------------
        # Replacement 1
        #---------------

        repl_index = repl_policy.Replace(cache, 0, None)
        cache[repl_index][0] = { 'recency_index':  60 }

        if cache != [[{'recency_index'  : 7}],
                     [{'recency_index'  : 1}],
                     [{'recency_index'  : 6}],
                     [{'recency_index'  : 11}],
                     [{'recency_index'  : 60}],
                     [{'recency_index'  : 54}],
                     [{'recency_index'  : 28}],
                     [{'recency_index'  : 10}],
                     [{'recency_index'  : 77}],
                     [{'recency_index'  : 92}],
                     [{'recency_index'  : 33}]]:

            self.fail('Incorrect replacement')

        #---------------
        # Replacement 2
        #---------------

        repl_index = repl_policy.Replace(cache, 0, None)
        cache[repl_index][0] = { 'recency_index':  40 }

        if cache != [[{'recency_index'  : 7}],
                     [{'recency_index'  : 1}],
                     [{'recency_index'  : 6}],
                     [{'recency_index'  : 11}],
                     [{'recency_index'  : 60}],
                     [{'recency_index'  : 54}],
                     [{'recency_index'  : 28}],
                     [{'recency_index'  : 10}],
                     [{'recency_index'  : 77}],
                     [{'recency_index'  : 40}],
                     [{'recency_index'  : 33}]]:

            self.fail('Incorrect replacement')

        print(cache)

    def test_3_FIFO(self): 
        """ Description: Test the FIFO Replacement Policy """

        repl_policy    = ReplacementPolicy('FIFO')

        cache = [[{'added_index'  : 7}],
                 [{'added_index'  : 1}],
                 [{'added_index'  : 6}],
                 [{'added_index'  : 11}],
                 [{'added_index'  : 100}],
                 [{'added_index'  : 54}],
                 [{'added_index'  : 28}],
                 [{'added_index'  : 10}],
                 [{'added_index'  : 77}],
                 [{'added_index'  : 92}],
                 [{'added_index'  : 33}]]

        #---------------
        # Replacement 1
        #---------------

        repl_index = repl_policy.Replace(cache, 0, None)
        cache[repl_index][0] = { 'added_index':  60 }

        if cache != [[{'added_index'  : 7}],
                     [{'added_index'  : 60}],
                     [{'added_index'  : 6}],
                     [{'added_index'  : 11}],
                     [{'added_index'  : 100}],
                     [{'added_index'  : 54}],
                     [{'added_index'  : 28}],
                     [{'added_index'  : 10}],
                     [{'added_index'  : 77}],
                     [{'added_index'  : 92}],
                     [{'added_index'  : 33}]]:

            self.fail('Incorrect replacement')

        #---------------
        # Replacement 2
        #---------------

        repl_index = repl_policy.Replace(cache, 0, None)
        cache[repl_index][0] = { 'added_index':  157 }

        if cache != [[{'added_index'  : 7}],
                     [{'added_index'  : 60}],
                     [{'added_index'  : 157}],
                     [{'added_index'  : 11}],
                     [{'added_index'  : 100}],
                     [{'added_index'  : 54}],
                     [{'added_index'  : 28}],
                     [{'added_index'  : 10}],
                     [{'added_index'  : 77}],
                     [{'added_index'  : 92}],
                     [{'added_index'  : 33}]]:

            self.fail('Incorrect replacement')

        print(cache)

    def test_4_RR(self): 
        """ Description: Test the RR Replacement Policy """
        return

    def test_5_LFU(self): 
        """ Description: Test the LFU Replacement Policy """

        repl_policy = ReplacementPolicy('LFU')

        cache = [[{'tag' : 'tag1' }],
                 [{'tag' : 'tag2' }],
                 [{'tag' : 'tag3' }],
                 [{'tag' : 'tag4' }],
                 [{'tag' : 'tag5' }],
                 [{'tag' : 'tag6' }],
                 [{'tag' : 'tag7' }],
                 [{'tag' : 'tag8' }],
                 [{'tag' : 'tag9' }],
                 [{'tag' : 'tag10'}],
                 [{'tag' : 'tag11'}]]

        usage_index = [{ 'tag1'  : 4,
                         'tag2'  : 1,
                         'tag3'  : 2,
                         'tag4'  : 1,
                         'tag5'  : 5,
                         'tag6'  : 6,
                         'tag7'  : 7,
                         'tag8'  : 8,
                         'tag9'  : 3,
                         'tag10' : 6,
                         'tag11' : 9 }]

        #---------------
        # Replacement 1
        #---------------

        repl_index = repl_policy.Replace(cache, 0, usage_index)
        cache[repl_index][0] = { 'tag' : 'tag20' }

        usage_index[0]['tag20'] = 9

        if cache != [[{'tag' : 'tag1' }],
                     [{'tag' : 'tag20' }],
                     [{'tag' : 'tag3' }],
                     [{'tag' : 'tag4' }],
                     [{'tag' : 'tag5' }],
                     [{'tag' : 'tag6' }],
                     [{'tag' : 'tag7' }],
                     [{'tag' : 'tag8' }],
                     [{'tag' : 'tag9' }],
                     [{'tag' : 'tag10'}],
                     [{'tag' : 'tag11'}]]:

            self.fail('Incorrect replacement')

        #---------------
        # Replacement 2
        #---------------

        repl_index = repl_policy.Replace(cache, 0, usage_index)
        cache[repl_index][0] = { 'tag' : 'tag50' }

        usage_index[0]['tag50'] = 60

        if cache != [[{'tag' : 'tag1'  }],
                     [{'tag' : 'tag20' }],
                     [{'tag' : 'tag3'  }],
                     [{'tag' : 'tag50' }],
                     [{'tag' : 'tag5'  }],
                     [{'tag' : 'tag6'  }],
                     [{'tag' : 'tag7'  }],
                     [{'tag' : 'tag8'  }],
                     [{'tag' : 'tag9'  }],
                     [{'tag' : 'tag10' }],
                     [{'tag' : 'tag11' }]]:

            self.fail('Incorrect replacement')

        print(cache)
        print(usage_index[0])

    def test_6_LFRU(self): 
        """ Description: Test the LFRU Replacement Policy """
        
        repl_policy = ReplacementPolicy('LFRU')

        cache = [[{ 'tag' : 'tag1' , 'recency_index'  : 7   }],
                 [{ 'tag' : 'tag2' , 'recency_index'  : 1   }],
                 [{ 'tag' : 'tag3' , 'recency_index'  : 6   }],
                 [{ 'tag' : 'tag4' , 'recency_index'  : 11  }],
                 [{ 'tag' : 'tag5' , 'recency_index'  : 100 }],
                 [{ 'tag' : 'tag6' , 'recency_index'  : 54  }],
                 [{ 'tag' : 'tag7' , 'recency_index'  : 28  }],
                 [{ 'tag' : 'tag8' , 'recency_index'  : 10  }],
                 [{ 'tag' : 'tag9' , 'recency_index'  : 77  }],
                 [{ 'tag' : 'tag10', 'recency_index'  : 92  }],
                 [{ 'tag' : 'tag11', 'recency_index'  : 33  }]]

        usage_index = [{ 'tag1'  : 4,
                         'tag2'  : 1,
                         'tag3'  : 2,
                         'tag4'  : 1,
                         'tag5'  : 5,
                         'tag6'  : 6,
                         'tag7'  : 7,
                         'tag8'  : 8,
                         'tag9'  : 3,
                         'tag10' : 6,
                         'tag11' : 9 }]

        #---------------
        # Replacement 1
        #---------------

        repl_index = repl_policy.Replace(cache, 0, usage_index)
        cache[repl_index][0] = { 'tag' : 'tag20', 'recency_index': 60 }

        usage_index[0]['tag20'] = 9

        if cache != [[{'tag' : 'tag1' , 'recency_index'  : 7   }],
                     [{'tag' : 'tag20', 'recency_index'  : 60  }],
                     [{'tag' : 'tag3' , 'recency_index'  : 6   }],
                     [{'tag' : 'tag4' , 'recency_index'  : 11  }],
                     [{'tag' : 'tag5' , 'recency_index'  : 100 }],
                     [{'tag' : 'tag6' , 'recency_index'  : 54  }],
                     [{'tag' : 'tag7' , 'recency_index'  : 28  }],
                     [{'tag' : 'tag8' , 'recency_index'  : 10  }],
                     [{'tag' : 'tag9' , 'recency_index'  : 77  }],
                     [{'tag' : 'tag10', 'recency_index'  : 92  }],
                     [{'tag' : 'tag11', 'recency_index'  : 33  }]]:

            self.fail('Incorrect replacement')

        #---------------
        # Replacement 2
        #---------------

        repl_index = repl_policy.Replace(cache, 0, usage_index)
        cache[repl_index][0] = { 'tag' : 'tag60', 'recency_index': 80 }

        usage_index[0]['tag60'] = 10

        if cache != [[{'tag' : 'tag1' , 'recency_index'  : 7   }],
                     [{'tag' : 'tag20', 'recency_index'  : 60  }],
                     [{'tag' : 'tag3' , 'recency_index'  : 6   }],
                     [{'tag' : 'tag60', 'recency_index'  : 80  }],
                     [{'tag' : 'tag5' , 'recency_index'  : 100 }],
                     [{'tag' : 'tag6' , 'recency_index'  : 54  }],
                     [{'tag' : 'tag7' , 'recency_index'  : 28  }],
                     [{'tag' : 'tag8' , 'recency_index'  : 10  }],
                     [{'tag' : 'tag9' , 'recency_index'  : 77  }],
                     [{'tag' : 'tag10', 'recency_index'  : 92  }],
                     [{'tag' : 'tag11', 'recency_index'  : 33  }]]:

            self.fail('Incorrect replacement')

        print(cache)
        print(usage_index[0])

def RunUnitTests():

    if not os.path.isdir(os.path.join(os.getcwd(), 'test/results')):
        os.mkdir('test/results')

    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test/results'))

if __name__ == '__main__':
    RunUnitTests()
