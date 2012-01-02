import random
import math

class GeneralRandomInteger():
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
        
        x = map(int, x)
        xSorted = list(x); xSorted.sort()
        assert xSorted == x
        assert len(x) == len(set(x))
        
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
        sump = sum(p)
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
            
if __name__ == '__main__':
    rng = GeneralRandomInteger(range(3), [1, 2, 3])
    smpl = rng.random(5000)
    from collections import defaultdict
    count = defaultdict(int)
    for s in smpl:
        count[s] += 1
    for i in range(3):
        print '%d %d'%(i, count[i])
    
