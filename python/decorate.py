import time

def entryExit(f):
	def new_f(num):
		begin = time.time()
		print "Entering", f.__name__
		f(num)
		print "Exited after %0.9f seconds for num = %d" % (time.time() - begin, num)
	return new_f

@entryExit
def sumUp(num):
	sum = 0
	for i in range(0,num):
		sum += i
	return sum

sumUp(1)

sumUp(10)

sumUp(100)

sumUp(1000)

sumUp(10000)

sumUp(100000)

