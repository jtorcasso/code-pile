from multiprocessing import Pool
import numpy as np
import time
import statsmodels.api as sm

np.random.seed(1234)

x = np.random.randn(100)*10
z = x + 3*np.random.randn(100)
y = 2*x + np.random.randn(100)*2

def OLS(**kwargs):
	a = kwargs['a']
	b = kwargs['b']
	return sm.OLS(y,a).fit().params

pool = Pool()

fit = pool.map(OLS,[{'a':x,'b':1},{'a':z,'b':1}])

print(fit[0], fit[1])

# def bootstrap(x):
# 	"""
# 	x is an array

# 	Returns bootstrapped standard error of mean of x
# 	"""

# 	R = 10000
# 	u = [x.mean()]
# 	for i in xrange(R):
# 		boot = np.random.choice(x, x.shape[0])
# 		u.append(boot.mean())
	
# 	return np.array(u).std()


# if __name__ == '__main__':

# 	a = 10 + 10*np.random.randn(1000)
# 	b = 20 + 20*np.random.randn(1000)
# 	c = np.random.randn(1000)
# 	d = 32 + 16*np.random.randn(1000)

# 	# Standard Errors of Mean Assuming (correctly) normality
# 	start = time.time()
# 	stds = [np.std(x)/np.sqrt(x.shape[0]) for x in [a,b,c,d]]
# 	print "Baseline - Parametric: ", time.time() - start, 'seconds'
# 	print stds

# 	print ""
# 	print ""
# 	# Standard Errors of Mean, Non-parametric Bootstrap
# 	start = time.time()
# 	stds = [bootstrap(x) for x in [a,b,c,d]]
# 	print "Single:                ", time.time() - start, 'seconds'
# 	print stds

# 	print ""
# 	print ""
# 	# Standard Errors of Mean, Non-parametric Bootstrap, Parellel - I
# 	start = time.time()
# 	pool = Pool()
# 	results = [pool.apply_async(bootstrap, (x,)) for x in [a,b,c,d]]
# 	stds = [r.get() for r in results]
# 	print "Parallel:              ", time.time() - start, "seconds"
# 	print stds

# 	print ""
# 	print ""
# 	# Standard Errors of Mean, Non-parametric Bootstrap, Parellel - II
# 	start = time.time()
# 	pool = Pool()
# 	stds = pool.map(bootstrap, (a,b,c,d))
# 	print "Parallel:              ", time.time() - start, "seconds"
# 	print stds