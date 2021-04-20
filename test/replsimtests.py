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
        return

    def test_2_MRU(self): 
        """ Description: Test the MRU Replacement Policy """
        return

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
