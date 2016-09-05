import itertools

def inumber(x):
	for i in xrange(x):
		yield i



for i in itertools.chain(inumber(3), inumber(2)):
	print i

for i in itertools.repeat('me', 3):
	print i