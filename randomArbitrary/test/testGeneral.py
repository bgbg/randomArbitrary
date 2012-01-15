import unittest

import sys
sys.path.append(r'../asop')
import randomArbitrary
import numpy as np

class TestRNG(unittest.TestCase):
    '''Module-wide tests'''
    
    classes = [randomArbitrary.RandomArbitrary,
               randomArbitrary.RandomArbitraryInteger]
               
    def _dummyrandomArbitraryObject(self):
        r = randomArbitrary.RandomArbitrary()
        return r
        
    def _dummyrandomArbitraryIntegerObject(self):
        x = np.arange(10) + 1
        r = randomArbitrary.RandomArbitraryInteger(x)
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
            
    
    def testRaiseExceptionOnAllZeroPValues(self):
        '''If sum of the requested p values is 0, should raise exception'''
        
        n = 3
        x = range(n)
        p = [0, ] * n
        for cls in (randomArbitrary.RandomArbitrary,
                    randomArbitrary.RandomArbitraryInteger):
            self.assertRaises(ValueError, cls,
                              *(x, p)) 
    
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
    

            
            
        
        
        
        
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAbstractClasses']
    unittest.main() 
             
    
        