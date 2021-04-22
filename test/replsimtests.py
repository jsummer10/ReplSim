'''
Project     : Replacement Policy Simulation
File name   : replsimtests.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains the test cases for the replacement
              policy simulator
'''

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
        return

    def test_4_RR(self): 
        """ Description: Test the RR Replacement Policy """
        return

    def test_5_LFU(self): 
        """ Description: Test the LFU Replacement Policy """
        return

    def test_6_LFRU(self): 
        """ Description: Test the LFRU Replacement Policy """
        return

def RunUnitTests():

    if not os.path.isdir(os.path.join(os.getcwd(), 'test/results')):
        os.mkdir('test/results')

    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test/results'))

if __name__ == '__main__':
    RunUnitTests()
