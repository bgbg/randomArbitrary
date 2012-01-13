import numpy as np
import scipy.stats as stats
from collections import defaultdict
import randomArbitrary

def chi2testSampleAgainsProbability(observed, expectedProbabilities):
    expectedProbabilities = np.array(expectedProbabilities)
    countO = defaultdict(int)
    nPoints = len(observed)
    for o in observed: countO[o] += 1
    
    
    keys = range(len(expectedProbabilities))
    countObserved = np.array([countO[k] for k in keys], dtype=float) 
    countObserved = countObserved / countObserved.sum()
    try:
        chi2 = np.sum((countObserved - expectedProbabilities) ** 2 / expectedProbabilities)
    except:
        print 'huj'
    df = len(keys) - 1
    pVal = 1.0 - stats.distributions.chi2.cdf(chi2, df)
    return (chi2, pVal)
    


def chi2testTwoSamples(observed, expected):
    countO = defaultdict(int)
    countE = defaultdict(int)
    for o in observed: countO[o] += 1
    for e in expected: countE[e] += 1

    keysO = set(countO.keys())
    keysE = set(countE.keys())
    keys = list(keysO.union(keysE))
    keys.sort()
    countExpected = np.array([countE[k] for k in keys], dtype=float) 
    countObserved = np.array([countO[k] for k in keys], dtype=float) 
    sel = (countExpected != 0)
    countExpected = countExpected[sel]
    countObserved = countObserved[sel]
    k2 = np.sqrt(np.sum(countExpected, dtype=float) / np.sum(countObserved, dtype=float))
    k1 = np.sqrt(np.sum(countObserved, dtype=float) / np.sum(countExpected, dtype=float))
    chi2 = np.sum((k1 * countExpected - k2 * countObserved) ** 2 / (countExpected + countObserved))
        
    c = int(len(observed) == len(expected))
    df = len(keys) - c
    pVal = 1.0 - stats.distributions.chi2.cdf(chi2, df)
    return (chi2, pVal)
    
TIMES = 100
REPEATS = 3
np.random.seed(3)

ALPHA = 0.01
SAMPLES = 100
REPEATS = 1000
timesBelowAlpha = 0
lMsg =[]
createPValuesInteger = ('Integer p values',
                        lambda nSamples: np.random.randint(0, n, nSamples))
createPValuesFloat = ('Float p values', 
                      lambda  nSamples: np.random.rand(nSamples))
createPValiuesLargeDifferences = ('Large differences in p values',
                                  lambda nSamples: np.exp(np.random.randn(nSamples)))
pValueGenerators = (createPValuesInteger, createPValuesFloat,
                    createPValiuesLargeDifferences)  

for name, pGenerator in (createPValuesInteger, ):
#                       createPValuesFloat,
#                       createPValiuesLargeDifferences):
    for i in range(REPEATS):
        n = np.random.randint(3, 20)
        x = range(n)
        theSum = 0
        while theSum <= 0:
            pValuesRequested = pGenerator(n)
            theSum = sum(pValuesRequested)
        z = np.exp(pValuesRequested)
        rng = randomArbitrary.RandomArbitraryInteger(x=x, p=z)
        theSample = rng.random(SAMPLES)
        pValuesNormalized = np.divide(pValuesRequested, 
                                      float(sum(pValuesRequested)))
        p = chi2testSampleAgainsProbability(theSample, pValuesNormalized)[1]
        if p < ALPHA:
            timesBelowAlpha += 1

    #Binomial test.
    #At this point we expect that timesBelowAlpha will not be significantly
    # higher than ALPHA * REPEATS 
    #failureFractionValues are above ALPHA. Let's use binomial test to 
    #test it  
    nExpected = int(REPEATS*ALPHA)
    if timesBelowAlpha > nExpected:
        pBinomialTest = stats.binom_test(timesBelowAlpha, 
                                         REPEATS, ALPHA) * 2 #one-sided test, thus *2
        if pBinomialTest < ALPHA:
            #shit, there might be a problem
            msg = '(%s) Failed sampling distribution test'\
                'This might happen once in a while even if everything is OK. '\
                'Expected %d failures, observed %d ones (p=%.4f). '\
                'Repeat the test and hope for the best'%(name, nExpected,
                                                         timesBelowAlpha, 
                                                         pBinomialTest)
            lMsg.append(msg)

if lMsg:
    raise AssertionError('\n'.join(lMsg))

