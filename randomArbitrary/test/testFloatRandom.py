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
        
        import scipy.stats as stats
        
        ALPHA = 0.01
        SAMPLES = 100
        REPEATS = 1000
        lMsg =[]
        
        kstest = stats.kstest
        class CDFFunction:
            '''Class that creates simple CDF function'''
            def __init__(self, x, p):
                self.x = x
                self.cdf = np.cumsum(np.array(p) / np.sum(p))
                
            def __call__(self, v):
                return np.interp(v, self.x, self.cdf, 0, 1.0)
            
        createPValuesInteger = ('Integer p values',
                                lambda nSamples: np.random.randint(0, 100, nSamples))
        createPValuesFloat = ('Float p values', 
                              lambda  nSamples: np.random.rand(nSamples))
        createPValiuesLargeDifferences = ('Large differences in p values',
                                          lambda nSamples: np.exp(np.random.randn(nSamples)))
        pValueGenerators = (createPValuesInteger, createPValuesFloat,
                            createPValiuesLargeDifferences)  
        
        for name, pGenerator in pValueGenerators:
            falsePositives = 0
            for i in range(REPEATS): #@UnusedVariable
                theRange = np.random.randn(2) * 100
                theRange.sort()
                x = np.linspace(theRange[0], theRange[1], SAMPLES)         
                theSum = 0
                while theSum <= 0:
                    pValuesRequested = pGenerator(SAMPLES)
                    theSum = sum(pValuesRequested)
                rng = randomArbitrary.RandomArbitrary(x=x, p=pValuesRequested)
                theSample = rng.random(SAMPLES)
                cdf = CDFFunction(x,  pValuesRequested.astype(float) / np.sum(pValuesRequested))
                p = kstest(theSample, cdf)[1]
                
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
            msg = '. '.join(lMsg)
            self.fail(msg)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()