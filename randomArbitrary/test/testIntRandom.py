import unittest
import numpy as np
from collections import defaultdict


import testGeneral
import randomArbitrary

class TestGeneralRandomInteger(testGeneral.TestRNG):


    def testRNGFIntegerNumbersFollowDistribution(self):
        '''Generated numbers must agree with specified distribution'''
        raise NotImplementedError()
    
    def testRandIntegerCoversAllTheValues(self):
        'Sampling integer values should eventually cover all possible values'
        nPoints = 10        
        SAMPLES = 100 * nPoints
        TIMES = 10
        for t in xrange(TIMES): #@UnusedVariable
            pValues = np.arange(nPoints) + 1
            xValues = np.random.randint(-100, 100, nPoints).tolist()
            xValues.sort()
            rng = randomArbitrary.GeneralRandomInteger(xValues, pValues)
            rValues = rng.random(SAMPLES)
            count = defaultdict(int)
            for v in rValues:
                count[v] += 1
            for i in range(nPoints):
                if i in xValues:
                    self.assertTrue(count[i] > 0)
                else:
                    self.assertEqual(count[i], 0)
    def testRandIntegerExcludedValues(self):
        nPoints = 10
        TIMES = 100 * nPoints
        xValues = range(nPoints)
        for i in range(nPoints):
            pValues = np.arange(nPoints) + 1
            pValues[i] = 0.0
            rng = randomArbitrary.GeneralRandomInteger(x=xValues,
                                                       p=pValues)
            r = rng.random(TIMES)
            f = filter(lambda v: v==i, r)
            self.assertTrue(len(f)==0)
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()