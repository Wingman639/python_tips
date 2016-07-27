import inspect


def func_1(a, b):
	print inspect.stack()
	return a + b

def main():
	b = 1
	c = 3
	a = func_1(b, c)

if __name__ == '__main__':
	main()