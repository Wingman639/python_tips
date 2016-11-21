



def readable_dict_string(dict_data):
	text = u''
	for key, value in dict_data.items():
		text += u'%s : %s\n' % (readable_string(key), readable_string(value))
	return text

def readable_list_string(list_data):
	text = ''
	for item in list_data:
		text += readable_string(item)
	return text

def readable_string(data):
	text = u''
	if type(data) is type({}):
		text += readable_dict_string(data)
	elif type(data) is type([]):
		text += readable_list_string(data)
	else:
		# print [data]
		try:
			data_text = str(data)
		except:
			data_text = str([data])

		text += data_text
	return text

if __name__ == '__main__':
	import os

	file_path = 'nova_list_output.txt'
	output_file = 'readable.txt'
	output = ''
	with open(file_path, 'r') as f:
		data = eval(f.read())
		output = readable_string(data)
	print output
	with open(output_file, 'w') as f:
		f.write(output)
