
import TNSDL_function_reader as tnsdl



def get_functions(text):
	functions = {}
	functions['procedures'] = tnsdl.get_procedure_list(text)
	functions['inputs'] = tnsdl.get_input_list(text)
	return functions

def fill_access_chain(functions):
	chains = {}
	for s_name, signal in functions['inputs'].items():
		chain = get_access_chain_with_signal(s_name, signal, functions)
		print chain



def access_chain_with_procedure(procedure_name, functions):
	chains = []
	for proc_name, procedure in functions['procedures'].items():
		if tnsdl.is_procedure_called_in_code(procedure_name, procedure):
			chains.append([procedure_name, proc_name])
	return chains



def read_tnsdl_file(file_name):
	with open(file_name, 'r') as f:
		text = f.read()
	return text

if __name__ == '__main__':
	import save_data

	def test():
		pass

	def try_to_get_functions(file_name):
		data_file_name = file_name + '.data'
		functions = save_data.load_from_file(data_file_name)
		if functions: return functions
		return functions_from_source_file(file_name)


	def functions_from_source_file(file_name):
		text = read_tnsdl_file('rezha1qx.sdl')
		functions = get_functions(text)
		data_file_name = file_name + '.data'
		save_data.save_to_file(functions, data_file_name)
		return functions


	def main():
		functions = try_to_get_functions('rezha1qx.sdl')
		if not functions: return
		#print functions['procedures'].keys()
		#print functions['inputs'].keys()
		print len(functions['procedures']), len(functions['inputs'])
		print access_chain_with_procedure('send_cell_barred__r', functions)



	#test()
	main()