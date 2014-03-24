import numpy as np
from pymc import stochastic, DiscreteUniform, DiscreteMetropolis, Model, MAP
import statsmodels.api as sm
import itertools
import math
import pandas as pd
import random

size = 100

rank = 10

numPredictors = [3,4,5]

x = np.random.randn(size, rank)*np.random.randint(0,10,rank) + \
             np.random.randint(5,10,rank)
e = np.random.randn(size)*3

coefficients = np.zeros(rank)
coefficients[np.random.randint(0, rank, 4)] = np.array([2]*4)
coefficients = coefficients.reshape((-1,1))

intercept = 4

y = intercept + x.dot(coefficients) + e.reshape((-1,1))
combos = [itertools.combinations(xrange(0,rank),k) for k in numPredictors]
models = list(itertools.chain.from_iterable(combos))
models = [list(i) for i in models]

K = len(models)

@stochastic(dtype=int)
def regression_model(value=0):
    
    def logp(value):
	    prior = 1./K
	    
	    predictors = models[value]
	    
	    X = sm.add_constant(x[:,predictors], prepend=True)

	    ols = sm.OLS(y,X).fit()
	    
	    bic = ols.bic

	    return -np.log(math.exp(-0.5*bic)*prior)

    def random():
		import random
		return random.choice(range(K))

class ModelMetropolis(DiscreteMetropolis):
    def __init__(self, stochastic, *args, **kwargs):
        DiscreteMetropolis.__init__(self, stochastic, *args, **kwargs)
    
    def propose(self):
		        
        last = self.stochastic.value

        last_indicator = np.zeros(rank)
        
        last_indicator[models[last]] = 1
        
        last_indicator = last_indicator.reshape((-1,1))
        
        neighbors = abs(np.diag(np.ones(rank)) - last_indicator)
        
        neighbors = neighbors[:,np.any([neighbors.sum(axis=0) == i \
                            for i in numPredictors], axis=0)]
        neighbors = pd.DataFrame(neighbors)
        
        draw = random.choice(xrange(neighbors.shape[1]))

        return models.index(list(neighbors[draw][neighbors[draw]==1].index))