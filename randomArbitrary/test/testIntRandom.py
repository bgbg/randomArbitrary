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
    def _chi2testSampleAgainsProbability(observed, expectedProbabilities):
        '''chi2 test to test whether a sample is consistent with expected prob.
        
        This function works only with integer samples in the range [0, n), where
        n is a natural number
        
        @param observed: the observed sample
        @param expectedProbabilities: list of expected probabilities. Value at
            index `i` corresponds to the probability of integer `i`.
        @return: (chi2, pval)
        '''
        expectedProbabilities = np.array(expectedProbabilities)
        countO = defaultdict(int)
        for o in observed: countO[o] += 1
        keys = range(len(expectedProbabilities))
        countObserved = np.array([countO[k] for k in keys], dtype=float) 
        countObserved = countObserved / countObserved.sum()
        chi2 = np.sum((countObserved - expectedProbabilities) ** 2 / expectedProbabilities)
        df = len(keys) - 1
        pVal = 1.0 - stats.distributions.chi2.cdf(chi2, df)
        return (chi2, pVal)
    
   
    
    def testRNGIntegerFollowsDistribution(self):
        ALPHA = 0.01
        SAMPLES = 100
        REPEATS = 1000
        lMsg =[]
        createPValuesInteger = ('Integer p values',
                                lambda nSamples: np.random.randint(0, n, nSamples))
        createPValuesFloat = ('Float p values', 
                              lambda  nSamples: np.random.rand(nSamples))
        createPValiuesLargeDifferences = ('Large differences in p values',
                                          lambda nSamples: np.exp(np.random.randn(nSamples)))
        pValueGenerators = (createPValuesInteger, createPValuesFloat,
                            createPValiuesLargeDifferences)  
        
        for name, pGenerator in pValueGenerators:
            falsePositives = 0
            for i in range(REPEATS): #@UnusedVariable
                n = np.random.randint(3, 20)
                x = range(n)
                theSum = 0
                while theSum <= 0:
                    pValuesRequested = pGenerator(n)
                    theSum = sum(pValuesRequested)
                rng = randomArbitrary.RandomArbitraryInteger(x=x, p=pValuesRequested)
                theSample = rng.random(SAMPLES)
                pValuesNormalized = np.divide(pValuesRequested, 
                                              float(sum(pValuesRequested)))
                p = self._chi2testSampleAgainsProbability(theSample, 
                                                          pValuesNormalized)[1]
                if p < ALPHA:
                    falsePositives += 1
                
        
            #Binomial test.
            #At this point we expect that falsePositives will not be significantly
            # higher than ALPHA * REPEATS 
            #failureFractionValues are above ALPHA. Let's use binomial test to 
            #test it  
            nExpectedFalsePositives = int(REPEATS*ALPHA)
            if falsePositives > nExpectedFalsePositives:
                pBinomialTest = stats.binom_test(falsePositives, 
                                                 REPEATS, 
                                                 ALPHA) * 2 #one-sided test, thus *2
                if pBinomialTest < ALPHA:
                    #shit, there might be a problem
                    msg = '(%s) Failed sampling distribution test '\
                        'Expected %d failures or less, observed %d ones (p=%.3f). '\
                        "Don't panic. "\
                        'This might happen once in a while even if everything is OK. '\
                        'Repeat the test and hope for the best'%(name, nExpectedFalsePositives,
                                                                 falsePositives, 
                                                                 pBinomialTest)
                    lMsg.append(msg)
        if lMsg:
            self.fail('. '.join(lMsg))
            
            

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()