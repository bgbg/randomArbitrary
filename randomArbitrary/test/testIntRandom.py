import unittest
import numpy as np
import scipy.stats as stats

from collections import defaultdict


import testGeneral
import randomArbitrary

class TestGeneralRandomInteger(testGeneral.TestRNG):

    
    def testRandIntegerCoversAllTheValues(self):
        'Sampling integer values should eventually cover all possible values'
        nPoints = 10        
        SAMPLES = 100 * nPoints
        TIMES = 10
        for t in xrange(TIMES): #@UnusedVariable
            xValues = []
            while len(xValues) < 2:
                xValues = np.random.randint(-100, 100, nPoints).tolist()
                xValues.sort()
                xValues = np.unique(xValues)
            pValues = np.arange(len(xValues)) + 1
            rng = randomArbitrary.RandomArbitraryInteger(xValues, pValues)
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
            rng = randomArbitrary.RandomArbitraryInteger(x=xValues,
                                                       p=pValues)
            r = rng.random(TIMES)
            f = filter(lambda v: v==i, r)
            self.assertTrue(len(f)==0)
                
    @staticmethod
    def _compareDiscreteDistributions(x, p, theSample):
        '''chi2 test that the difference between distributions is random
        
        Compare the discrete distribution that is defined by `x` and `p` to
        the `sample` using chi2 test. Return p-value that the difference
        between the expected and the observed CDF's is random. If PDF is
        defined using two values (i.e len(x)==2), exact Fisher's test is used
        '''
        nCells = len(x)    
        assert len(x) == len(p)

        nPoints = len(theSample)        
        expected = np.array(p, dtype=float) / np.sum(p)
        sel = [expected > 0]
        expected = expected[sel]
        expected *= nPoints
        
        observed = [0] * nCells
        for i in range(len(x)):
            n = np.sum(theSample == x[i])
            observed[i] = n
        observed = np.array(observed)[sel]
        nCells = len(observed)
        if nCells == 1:
            pdf = 0.0
        elif nCells >= 2:
            chi2 = np.sum(((observed - expected) ** 2) / expected)
            k = len(x) - 1
            pdf = stats.chi2.pdf(chi2, k)
        else:
            table = np.vstack((observed, expected))
            pdf = stats.fisher_exact(table)[1]
        return pdf
    
    def testRNGIntegerFollowsDistribution(self):
        TIMES = 100
        SAMPLES = 1000
        ALPHA = 0.01
        countPvaluesBelowAlpha = 0
        out = open(r'G:\eclipsetemp\randomArbitrary\src\randomArbitrary\test\zzz.txt', 'w')
        for nx in range(2, 40, 2):
            for t in range(TIMES): #@UnusedVariable
#                nx = np.random.randint(2, 40)
                n = 0
                while n < 2:
                    x = np.random.randint(-100, 100, nx)
                    x.sort()
                    x = np.unique(x)
                    
    #                r = np.random.random()
    #                if r < 0.33:
    #                    p = np.random.randint(0, 100, len(x))
    #                elif r < 0.66:
    #                    p = np.random.random(len(x))
    #                else:
    #                    #huge differences between p values
    #                    p = np.exp(np.random.randn(len(x)) * 10)
                    p = np.random.random(len(x)) 
                    sel = (np.random.random(len(x)) > 0.9)
                    p[sel] = 0.0
                    n = np.sum(p != 0)
                rng = randomArbitrary.RandomArbitraryInteger(x, p)
                smpl = rng.random(SAMPLES)
                pdf = self._compareDiscreteDistributions(x, p, smpl)
                if pdf < ALPHA:
                    countPvaluesBelowAlpha += 1
                out.write('(%d, %s, %s, %.3f),\n'%(nx, repr(x), repr(p), pdf))
#            print 'count:', countPvaluesBelowAlpha
        if countPvaluesBelowAlpha > TIMES * ALPHA:
            self.fail()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()