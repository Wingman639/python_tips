import traceback


def func_1():
	traceback.print_exc()
	return 1

def main():
	a = func_1()
	print a

if __name__ == '__main__':
	main()