import random
import math

issortedAndUnique = lambda l: np.all([l[i] < l[i+1] for i in xrange(len(l)-1)])


class RandomArbitraryInteger():
    '''Random integer numbers from an arbitrary distribution.

    This algorithm is based on
    Vose, A Linear Algorithm For Generating Random
    Numbers With a Given Distribution
    IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 17, NO. 9, SEPTEMBER 1991
    http://web.eecs.utk.edu/~vose/Publications/random.pdf
    '''
    def __init__(self, x, p=None):
        '''Initialize the object

        @param x: integer that will be used by the generator
        @param p: probability density proile for the distribution.
            If None (default) every value in `x` will have the same probability
        '''

        if p is None:
            p = [1.0, ] * len(x)
        assert len(x) == len(p)
        self.set_pdf(x, p)

    def set_pdf(self, x, p):
        '''Set the internal probability distribution function
        '''

        assert len(x) == len(p)
        x = map(int, x)
        assert issortedAndUnique(x)


        xMin = x[0]
        xMax = x[-1]
        xActual = range(xMin, xMax + 1, 1)
        pActual = [0.0,] * len(xActual)
        ix = 0
        for i, xValue in enumerate(xActual):
            if xValue in x[ix:]:
                pActual[i] = p[ix]
                ix += 1
        xActual = [xVal - xMin for xVal in xActual]
        self._xmin = xMin
        p = pActual
        for v in p:
            assert v >= 0
        p = map(float, p)
        for v in p:
            if v < 0:
                raise ValueError('Negative PDF values are not allowed')
        sump = sum(p)
        if sump == 0:
            raise ValueError('At least one non-zero PDF value is required')
        p = [v/sump for v in p]
        n = len(p)
        self._n = n

        #first stage -- divide indices to small and large
        large = []
        small = []
        n_1 = 1.0 / n
        for j, pValue in enumerate(p):
            if pValue > n_1:
                large.append(j)
            else:
                small.append(j)

        #second stage
        prob = [None,] * n
        alias = [None,] * n
        while bool(small) and bool(large):
            j = small.pop()
            k = large.pop()
            prob[j] = n * p[j]
            alias[j] = k
            p[k] = p[k] + p[j] - n_1
            if p[k] > n_1:
                large.append(k)
            else:
                small.append(k)
        for s in small:
            prob[s] = 1.0
        for l in large:
            prob[l] = 1.0


        self._prob = prob
        self._alias = alias


    def random(self, n=None):
        '''Return random number or numbers

        @param n: amount of random values to return or None
        @return: if n is None: return a scalar, if n>=1 return a list with n
            elements, else raise an exception
        '''

        if n is None:
            return self._randOne()
        else:
            assert n > 0
            return [self._randOne() for i in range(n)] #@UnusedVariable

    def _uniformN(self):
        return random.random() * self._n

    def _randOne(self):
        '''Return a single random number'''
        u = self._uniformN()
        j = int(math.floor(u))
        if (u - j) < self._prob[j]:
            ret = j
        else:
            ret = self._alias[j]
        return ret + self._xmin


import numpy as np
import scipy.stats as stats

def compareDiscreteDistributions(x, p, theSample):
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

    #zero expected values cause division-by-zero. Removing
    sel = [expected > 0]
    expected = expected[sel]
    expected *= nPoints

    observed = [0] * nCells
    for i in range(len(x)):
        n = np.sum(theSample == x[i])
        observed[i] = n

    #remove observed values that correspond to cells with zero expectation
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

def testRNGIntegerFollowsDistribution():
    np.random.seed(11223344)
    TIMES = 500
    REPEATS = 3
    SAMPLES = 1000
    ALPHA = 0.01
    for nx in range(8, 40, 2): #number of cells
        for r in range(REPEATS): #@UnusedVariable
            countPvaluesBelowAlpha = 0
            for t in range(TIMES): #@UnusedVariable
                n = 0
                while n < 2:
                    x = np.random.randint(-100, 100, nx)
                    x.sort()
                    x = np.unique(x)
                    p = np.random.random(len(x))
                    sel = (np.random.random(len(x)) > 0.9)
                    p[sel] = 0.0
                    n = np.sum(p != 0) #at least non-zero beans
                rng = RandomArbitraryInteger(x, p)
                smpl = rng.random(SAMPLES)
                pdf = compareDiscreteDistributions(x, p, smpl)
                if pdf < ALPHA:
                    countPvaluesBelowAlpha += 1
            prcnt = 100.0 * float(countPvaluesBelowAlpha) / TIMES
            print '%4d cells. p-values below %.2f: %3d (~%.0f%%)'%(
                              nx, ALPHA, countPvaluesBelowAlpha, prcnt)


if __name__ == '__main__':

    testRNGIntegerFollowsDistribution()


