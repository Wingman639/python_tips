
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



def access_chains_with_procedure(chain, functions):
	if not chain: return
	chain_list = []
	procedure_name = chain[-1]
	for proc_name, procedure in functions['procedures'].items():
		if procedure_name == proc_name: continue
		if tnsdl.is_procedure_called_in_code(procedure_name, procedure):
			new_list = chain + [proc_name]
			chain_list.append( new_list )
	if not chain_list:
		return [chain]
	return chain_list


def access_chains_with_level(procedure_name, level, functions):
	level = int(level)
	chains = access_chains_with_procedure([procedure_name], functions)
	for i in xrange(level - 1):
		chains = expend_chains_one_more_level(chains, functions)
	return chains


def expend_chains_one_more_level(chains, functions):
	new_chains = []	
	for chain in chains:
		new_chains += access_chains_with_procedure(chain, functions)
	return new_chains


def read_tnsdl_file(file_name):
	with open(file_name, 'r') as f:
		text = f.read()
	return text

if __name__ == '__main__':
	import unittest

	class FunctionTestCase(unittest.TestCase):
		def test_access_chains_with_procedure_not_find(self):
			expected = [['a', 'b']]
			result = access_chains_with_procedure(['a', 'b'], {'procedures':{}})
			self.assertEqual(expected, result)

		def test_access_chains_with_procedure(self):
			expected = [['a', 'b', 'c']]
			result = access_chains_with_procedure(['a', 'b'], {'procedures':{'c':'\nCALL b()'}})
			self.assertEqual(expected, result)


	import save_data

	def test():		
		functions = try_to_get_functions('rezha1qx.sdl')
		if not functions: return
		#print functions['procedures'].keys()
		#print functions['inputs'].keys()
		print len(functions['procedures']), len(functions['inputs'])
		#print access_chains_with_procedure(['send_cell_barred__r'], functions)
		chains = access_chains_with_level('send_cell_barred__r', 3, functions)
		print_list(chains)
		#chains = [['send_cell_barred__r', 'request_inact_sib_fail__r', 'hdl_hs_cch_fail__r'], ['send_cell_barred__r', 'request_inact_sib_fail__r', 'hdl_hs_cch_ready__r'], ['send_cell_barred__r', 'perform_cell_shutdown__r', 'handle_rez_cell_shd__r'], ['send_cell_barred__r', 'perform_cell_shutdown__r', 'check_scen_after_hspa_rem__r']]
		#print expend_chains_one_more_level(chains, functions)

	def access_chains(proc_name, level, file_name):
		functions = try_to_get_functions(file_name)
		chains = access_chains_with_level(proc_name, level, functions)
		return chains


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

	def print_list(a_list):
		print '[' 
		for item in a_list:
			print item
		print ']'


	def main():
		file_name = 'rezha1qx.sdl'
		proc_name = 'send_cell_barred__r'
		level = 3
		chains = access_chains(proc_name, level, file_name)
		print_list(chains)




	#test()
	main()
	#unittest.main()