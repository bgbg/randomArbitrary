import unittest

import sys
sys.path.append(r'../../')
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

    def testSetPDFFunction(self):
        objGeneral = self._dummyrandomArbitraryObject()
        objInteger = self._dummyrandomArbitraryIntegerObject()
        TIMES = 100
        N = 20
        for obj in [objGeneral, objInteger]:
            for t in range(TIMES): #@UnusedVariable
                x = np.unique(np.random.randint(-1000, 1000, N)) #already sorted
                p = np.random.rand(len(x))
                obj.set_pdf(x, p)


    def testSetPDFBadX(self):
        '''The set_pdf function should fail on unsorted or non-unique x'''
        objGeneral = self._dummyrandomArbitraryObject()
        objInteger = self._dummyrandomArbitraryIntegerObject()
        TIMES = 100
        N = 20
        for obj in [objGeneral, objInteger]:
            for t in range(TIMES): #@UnusedVariable
                x = np.unique(np.random.randint(-1000, 1000, N))
                p = np.random.random(len(x))
                #unique makes sure x is sorted
                x[0], x[1] = x[1], x[0] #verify that x is not sorted
                p = np.random.rand(N)
                try:
                    obj.set_pdf(x, p)
                except (ValueError, AssertionError):
                    pass
                else:
                    self.fail()

                x = np.unique(np.random.randint(-1000, 1000, N))
                p = np.random.random(len(x))
                #unique makes sure x is sorted
                x[0] = x[1] #verify that x is not unique
                p = np.random.rand(N)
                try:
                    obj.set_pdf(x, p)
                except (ValueError, AssertionError):
                    pass
                else:
                    self.fail()





    def testSetPDFFunctionBadArguments(self):
        '''set_pdf function should fail when its arguments have unequal length'''
        objGeneral = self._dummyrandomArbitraryObject()
        objInteger = self._dummyrandomArbitraryIntegerObject()
        x = np.arange(3)
        p = np.arange(4)
        for obj in [objGeneral, objInteger]:
            try:
                obj.set_pdf(x, p)
            except (ValueError, AssertionError):
                pass
            else:
                self.fail()

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


