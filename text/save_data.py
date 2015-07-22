
import cPickle as pickle

def save_to_file(obj, file_name):
	text = pickle.dumps(obj)
	with open(file_name, 'w') as f:
		f.write(text)

def load_from_file(file_name):
	try:
		with open(file_name, 'r') as f:
			text = f.read()
			return pickle.loads(text)
	except Exception as e:
		print e


if __name__ == '__main__':
	def test_save_load_obj():
		file_name = '1.data'
		obj = ('this is a string', 42, [1, 2, 3], None)
		save_to_file(obj, file_name)
		obj_2 = load_from_file(file_name)
		print bool(obj == obj_2), obj, obj_2



	def test():
		test_save_load_obj()

	test()