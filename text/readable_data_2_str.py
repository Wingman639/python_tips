
WIDTH_LIMIT = 80
INDENTATION_WIDTH = 2

def readable_str(data, level=0):
	if type(data) in [type(''), type(u'')]:
		return string_str(data)
	if type(data) == type({}):
		return dict_str(data, level)
	if type(data) == type([]):
		return list_str(data, level)
	return str(data)

def string_str(data):
	return "'" + str(data) + "'"

def dict_str(data, level=0):
	if len(str(data)) < WIDTH_LIMIT:
		return str(data)
	level += 1
	iden = identation(level)
	lines = []
	for key in data:
		line = readable_str(key, level) + ': ' + readable_str(data[key], level)
		lines.append(line)
	return '{\n' + iden + (',\n' + iden).join(lines) + '\n' + identation(level - 1) + '}'

def list_str(data, level=0):
	if len(str(data)) < WIDTH_LIMIT:
		return str(data)
	level += 1
	iden = identation(level)
	lines = [readable_str(item, level) for item in data]
	return '[\n' + iden + (',\n' + iden).join(lines) + '\n' + identation(level - 1) + ']'

def identation(level):
	return ' ' * INDENTATION_WIDTH * level

if __name__ == '__main__':

	def test():
		d_1 = {'a': 1, 'b': 2}
		# print readable_str(d_1)
		d_2 = {'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
			            'cccccccccccccccccccccccccccccc': 'dddddddddddddddddddddddddddddddddddddddd'}
		# print readable_str(d_2)
		list_1 = [1, 2]
		# print readable_str(list_1)
		list_2 = ['xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
			            'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy']
		# print readable_str(list_2)
		d_3 = {'a': list_1, 'b': list_2}
		# print readable_str(d_3)

		list_3 = [d_1, d_2, list_1, list_2]
		# print readable_str(list_3)

		d_4 = {'a': d_1, 'b': d_2, 'c': list_1, 'd': list_2, 'e': d_3, 'f': list_3}
		print readable_str(d_4)

		print identation(2)
	test()