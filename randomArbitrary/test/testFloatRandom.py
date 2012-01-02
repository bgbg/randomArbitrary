import unittest
import numpy as np

import testGeneral
import randomArbitrary


class TestGeneralRandomFloat(testGeneral.TestRNG):
    def testDefaultRNGFloat(self):
        '''general RNG can be initialized and used without parameters'''
        obj = randomArbitrary.RandomArbitrary()
        obj.random()
        
    def testDefaultRNGFloatValues(self):
        '''default object of general RNG returns values in range [0, 1)'''
        N = 10000
        obj = randomArbitrary.RandomArbitrary()
        values = obj.random(N)
        self.assertTrue(np.min(values)>=0)
        self.assertTrue(np.max(values)<1)
        
    def testRNGFloatValuesRange(self):
        '''By default, float RNG will return values within the specified range'''
        N = 10000
        TIMES = 100
        for i in range(TIMES): #@UnusedVariable
            tmp = np.random.randint(-1000., 1000, size=2)
            mn = min(tmp); mx = max(tmp)
            x = np.linspace(mn, mx, TIMES, endpoint=True)
            rng = randomArbitrary.RandomArbitrary(x)
            values = rng.random(N)
            mnValues = min(values)
            mxValues = max(values)
            self.assertTrue(mnValues >= mn)
            self.assertTrue(mxValues < mx)
            
            
    def testRNGFloatNumbersFollowDistribution(self):
        '''Generated numbers must agree with specified distribution'''
        raise NotImplementedError()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()