import numpy as np


class RandomArbitrary:
    """This class enables us to generate random numbers with an arbitrary 
    distribution.
    
    Based on a code by  Kaushik Ghose, copied on Dec 6 2011 
    http://code.activestate.com/recipes/576556/ Used under the MIT license
    """
    
    def __init__(self, x=np.arange(0.0, 1.0, .01), p=None, Nrl=1000,
                 trimOutput=True):
        """Initialize the lookup table (with default values if necessary)
        @param x: random number values
        @param p: probability density profile at that point
        @param Nrl: number of reverse look up values between 0 and 1
        @param trimOutput: should the output values beyong `x` be trimmed?
            default: True
        
        """    
        if p == None:
            p = np.ones(len(x))
        self.set_pdf(x, p, Nrl)
        self.trimOutput = bool(trimOutput)
        
    def set_pdf(self, x, p, Nrl=1000):
        """Generate the lookup tables. 
        x is the value of the random variate
        pdf is its probability density
        cdf is the cumulative pdf
        inversecdf is the inverse look up table
        
        """
        
        self.x = x
        p = np.array(p)
        if not np.all(p >= 0):
            raise ValueError('Negative PDF values are not allowed')
        elif np.all(p == 0):
            raise ValueError('At least one PDF non-zero value is required')
        self.pdf = p 
        self.pdf /= p.sum() #normalize it, it is provided that the sum >0
        self.cdf = self.pdf.cumsum()
        self.inversecdfbins = Nrl
        self.Nrl = Nrl
        y = np.arange(Nrl) / float(Nrl)
        self.inversecdf = np.zeros(Nrl)        
        self.inversecdf[0] = self.x[0]
        cdf_idx = 0
        for n in xrange(1, self.inversecdfbins):
            while self.cdf[cdf_idx] < y[n] and cdf_idx < Nrl:
                cdf_idx += 1
            self.inversecdf[n] = self.x[cdf_idx - 1] + (self.x[cdf_idx] - self.x[cdf_idx - 1]) * (y[n] - self.cdf[cdf_idx - 1]) / (self.cdf[cdf_idx] - self.cdf[cdf_idx - 1]) 
            if cdf_idx >= Nrl:
                break
        self.delta_inversecdf = np.concatenate((np.diff(self.inversecdf), [0]))
                            
    def random(self, n=None):
        """Give us N random numbers with the requested distribution
        
        @param n: amount of random values to return or None
        @return: if n is None: return a scalar, if n>=1 return a list with n
            elements, else raise an exception
        """

        idx_f = np.random.uniform(size=n, high=self.Nrl - 1)
        idx = np.array([idx_f], 'i').reshape(-1)
        y = self.inversecdf[idx] + (idx_f - idx) * self.delta_inversecdf[idx]
        
        if self.trimOutput:
            # We could have done something like:
            #    y[y<min(x)] = min(x); y[y>max(x)] = max(x)
            # but this will result in incorrectly high probability for
            # the minimum and the maximum values, thus we use this, much
            # slower method
            mn = min(self.x)
            mx = max(self.x)
            for i, v in  enumerate(y):
                if not mn <= v < mx:
                    while not mn <= v < mx: 
                        v = self.random(None)
                    y[i] = v
                    
        if n is None:
            y = y[0]
        return y
        
        