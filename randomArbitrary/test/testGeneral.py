import unittest
from matplotlib import pylab as plt

import sys
sys.path.append(r'../asop')
import randomArbitrary
import numpy as np

class TestRNG(unittest.TestCase):
    classes = [randomArbitrary.GeneralRandom,
               randomArbitrary.GeneralRandomInteger]
               
    def _dummyrandomArbitraryObject(self):
        r = randomArbitrary.GeneralRandom()
        return r
        
    def _dummyrandomArbitraryIntegerObject(self):
        x = np.arange(10) + 1
        r = randomArbitrary.GeneralRandomInteger(x)
        return r
    
    def testRandDefaultIsScalar(self):
        '''random() should return a scalar'''
        lBad = []
        obj = self._dummyrandomArbitraryObject()
        r = obj.random()
        if not np.isscalar(r):
            lBad.append(obj.__class__)
        
        obj = self._dummyrandomArbitraryIntegerObject()
        r = obj.random()
        if not np.isscalar(r):
            lBad.append(obj.__class__)
        if lBad:
            msg = ['%s: random(1) returned a non-scalar value'%str(b)
                for b in lBad]
            self.fail(msg)
            
            
    def testRandNIsIterable(self):
        '''random(N) should return a iterable with length N for each N>1'''
        lBad = set()
        lN = [1, 2, 3, 1000]
        objGeneral = self._dummyrandomArbitraryObject()
        objInteger = self._dummyrandomArbitraryIntegerObject()
        for obj in [objGeneral, objInteger]:
            for n in lN:
                r = obj.random(n)
                try:
                    iter(r)
                except TypeError:
                    lBad.add(obj.__class__)
                else:
                    if len(r) != n:
                        lBad.add(obj.__class__)
        if lBad:
            msg = ['%s: random(N) returned an object with a wrong length'%\
                str(b) for b in lBad]
            self.fail(msg)
            

    
    
      

    @staticmethod    
    def _cdfFromSample(xValues, theSample):
        theSample = np.array(theSample)
        pObsCumAbs = []
        for x in xValues:
            pObsCumAbs.append(np.sum(theSample <= x))
        pObsCum = np.array(pObsCumAbs, dtype=float) / len(theSample)
        return pObsCum
        
    @staticmethod
    def _cdfFromPvalues(pRef):
        pRef = np.array(pRef, dtype=float) / np.sum(pRef)
        pRefCum = np.cumsum(pRef)
        return pRefCum
        
    @staticmethod
    def _meanSquaredErrorBetweenCDFs(cdf1, cdf2, npoints):
        return np.sum(cdf1 - cdf2) ** 2 / npoints
        
        
            
    def _compareDistributions(self, xValues, pRef, theSample):
        TIMES = 10
        SAMPLES = 100    
        ALPHA = 0.2
        
        PLOT = False #Debugging plot
        
        cdfExpected = self._cdfFromPvalues(pRef)        
        cdfSample = self._cdfFromSample(xValues, theSample)
        if PLOT:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        npoints = len(theSample)
        mseObserved = self._meanSquaredErrorBetweenCDFs(cdfExpected, cdfSample,
                                                        npoints)
        timesFailed = 0
        quantiles = []
        for t in range(TIMES): #@UnusedVariable
            mseValues = []
            for i in range(SAMPLES): #@UnusedVariable
                pRand = np.abs(3.0 * np.random.randn(len(pRef)))
                cdfRand = self._cdfFromPvalues(pRand)
                mseRand = self._meanSquaredErrorBetweenCDFs(cdfExpected, 
                                                            cdfRand,
                                                            npoints)
                if PLOT: ax.plot(xValues, cdfRand, '-k', label='rand')
                mseValues.append(mseRand)
            thresholdValue = np.percentile(mseValues, ALPHA * 100)
            mseValues = np.array(mseValues)            
            Q = 100.0 * np.sum(mseValues > mseObserved) / float(len(mseValues))
            quantiles.append(Q)
            if mseObserved > thresholdValue:
                timesFailed += 1
                failed = True
            else:
                failed = False
            print 'observed: %.4f, threshold: %.4f, Q: %.0f%% %s'%(
                mseObserved, thresholdValue, Q, ['','FFF'][failed])
        
        if PLOT:
            ax.plot(xValues, cdfExpected, '-og', label='Expected')
            ax.plot(xValues, cdfSample, '-sr', label='Observed')
            ax.set_title('Failed: %d; Q%.0f%%. %.2f'%(
                timesFailed,
                np.mean(quantiles), 
                self._meanSquaredErrorBetweenCDFs(cdfExpected, cdfSample, npoints)))
            plt.show()
        return quantiles
        
                                                
        
    
    def testSampledValuesFollowDistribution(self):
        TIMES = 10
        SAMPLES = 1000
        xValues = np.linspace(-10, 10, 50)
        pValues = np.sin(xValues) ** 2
        rng = randomArbitrary.GeneralRandom(x=xValues,
                                            p=pValues)
        failures = []
        for i in range(TIMES): #@UnusedVariable
            rValues = rng.random(SAMPLES)
            failures.append(self._compareDistributions(xValues, 
                                                         pValues, rValues))
        self.fail(str(failures))
            
            
        
        
        
        
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAbstractClasses']
    unittest.main() 
             
    
        