import inspect

def print_func(func):
	def print_function_and_args(*args, **kwargs):
		print '{func_name} {args} {kwargs}'.format(func_name=func.__name__, args=args, kwargs=kwargs)
		func(*args, **kwargs)
	return print_function_and_args

@print_func
def test_case_1(a1, a2, a3):
	print 'test case runs'

test_case_1(1, 2, 3)


#===========================

def method_func(method):
	def print_method_and_args(obj, *args, **kwargs):
		print '{method_name} {args} {kwargs}'.format(method_name=method.__name__, args=args, kwargs=kwargs)
		method(obj, *args, **kwargs)
	return print_method_and_args

def decallmethods(decorator, prefix='test_'):
  def dectheclass(cls):
    for name, m in inspect.getmembers(cls, inspect.ismethod):
      if name.startswith(prefix):
        setattr(cls, name, decorator(m))
    return cls
  return dectheclass

@decallmethods(method_func)
class TestSuite(object):
	def test_case_a(self, a1, a2):
		print 'I am test case A'

	def test_case_b(self, b1, b2='22'):
		print 'I am test case B'



suite = TestSuite()
suite.test_case_a(4, 5)
suite.test_case_b('Tom', 'Jarry')