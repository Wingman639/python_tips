
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


def get_access_chain_with_signal(signal_name, signal, functions):
	chain = {}
	accessed_functions = functions_in_signal(signal)
	return chain

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
	def test():
		pass


	def main():
		text = read_tnsdl_file('rezha1qx.sdl')
		functions = get_functions(text)
		#print functions['procedures'].keys()
		#print functions['inputs'].keys()
		print len(functions['procedures']), len(functions['inputs'])
		print access_chain_with_procedure('send_cell_barred__r', functions)



	#test()
	main()