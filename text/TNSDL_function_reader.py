
import re

def get_procedure_list(text):
	lines = get_procedure_name_lines(text)
	name_list = procedure_names_from_lines(lines)
	procedure_dict = procedures_with_names(text, name_list)
	return procedure_dict

def get_input_list(text):
	lines = get_input_signal_name_lists(text)
	name_list = input_signal_names_from_lines(lines)
	input_signal_dict = input_signals_with_names(text, name_list)
	return input_signal_dict


### PROCEDURE part

def procedures_with_names(text, procedure_names):
	procedure_dict = {}
	for name in procedure_names:
		procedure = procedure_text_with_name(text, name)		
		procedure_dict[name] = procedure
	return procedure_dict

def procedure_text_with_name(text, procedure_name):
	pattern_str = r'\sPROCEDURE\s+{procedure_name}\s*;.*?ENDPROCEDURE\s+{procedure_name}\s*;'
	pattern_str = pattern_str.format(procedure_name=procedure_name)	
	text_list = findall_with_pattern_str(pattern_str, text)
	if text_list:
		return text_list[0]


def procedure_names_from_lines(lines):
	names = []
	for line in lines:
		procedure_name = procedure_name_from_line(line)
		if procedure_name:
			names.append(procedure_name)
	return names

def procedure_name_from_line(line):
	return line.replace('PROCEDURE', '').strip('\n\r\t\f\v ;').split()[0]

def get_procedure_name_lines(text):
	pattern_str = r'\sPROCEDURE[\s\w]*?;'
	return findall_with_pattern_str(pattern_str, text)



### INPUT signal part

def input_signals_with_names(text, signal_names):
	input_signal_dict = {}
	for name in signal_names:
		input_signal_text = input_signal_text_with_name(text, name)
		input_signal_dict[name] = input_signal_text
	return input_signal_dict

def input_signal_text_with_name(text, signal_name):
	pattern_str = r'{signal_name}.*?(?=INPUT|ENDSTATE)'
	pattern_str = pattern_str.format(signal_name=signal_name)	
	text_list = findall_with_pattern_str(pattern_str, text)
	if text_list:
		return text_list[0]



def input_signal_names_from_lines(lines):
	names = []
	for line in lines:
		signal_name = input_signal_name_from_line(line)
		if signal_name:
			names.append(signal_name)
	return names

def input_signal_name_from_line(line):
	return line.strip('\n\r\t\f\v ();')

def get_input_signal_name_lists(text):
	pattern_str = r'\sINPUT[\s\w]*?[(;]'
	return findall_with_pattern_str(pattern_str, text)
	

def get_called_functions(text):
	pattern_str = r'\s(?:TASK|CALL|DECISION|:=|OUTPUT)[\s(]+(\w*)\s*[\(]'
	return findall_with_pattern_str(pattern_str, text)



## is called
def is_procedure_called_in_code(procedure_name, text):
	pattern_str = r'\s(TASK|CALL|DECISION)[\s(]+.*?{name}(?!\w)'.format(name=procedure_name)
	return is_match_with_pattern_str(pattern_str, text)


## find all in text

def findall_with_pattern_str(pattern_str, text):
	pattern = re.compile(pattern_str, re.M|re.S)
	match = pattern.search(text)
	if match:
		return pattern.findall(text)
	else:
		return []

def is_match_with_pattern_str(pattern_str, text):
	pattern = re.compile(pattern_str, re.M|re.S)
	match = pattern.search(text)
	return bool(match)


if __name__ == '__main__':

	text = '''

#if (CRNC)
PROCEDURE query_cosit_stat_from_rak__r;
DCL
  raktor_pid   pid := NULL;
START;
  TASK raktor_pid := get_service_provider__r(raktor_p);
ENDPROCEDURE query_cosit_stat_from_rak__r;
#endif

/*******************************************************************************
*
* This procedure performs c_test_msg actions for hand_table_c test_id .
*
*******************************************************************************/

PROCEDURE c_test_hand_table__r;
FPAR
   IN VIEWED sub_id   byte;
START;
  DECISION get_sub_id();
  (mt_switch__t_dump_c):
	CALL send_dump_req__r();
  ENDDECISION;
  RETURN;

ENDPROCEDURE c_test_hand_table__r;


STATE working;
/***************************************************************************/
/*
* NBAP AUX Ack Handling
*
*****************************************************************************/
INPUT nbap_aux_cell_config_ack_s ( wbts_id
                                  );
DCL
  wbts_id         wbts_id_t,
  l_cell_list     cid_index_tbl__t;

  OUTPUT nbap_aux_cell_config_nack_s TO SELF;

  NEXTSTATE -;

/***************************************************************************/
/*
* NBAP AUX NACK handling
*
*****************************************************************************/
INPUT nbap_aux_cell_config_nack_s (   /* 0xB0BA */
                                    msg
                                  );
DCL
  msg                msg_b0ba_t,
  l_index            dword :=0,
  c_index            dword :=0,
  l_cell_succ_list   cid_index_tbl__t,
  l_cell_fail_list   cid_index_tbl__t;


  /* Start 7775 alarms for Failed cells */
  DECISION(l_cell_fail_list.count > 0);
  (T):
    CALL query_cosit_stat_from_rak__r(l_cell_fail_list,alarm_state_t_start_c);
  ENDDECISION;

  NEXTSTATE-;

/***************************************************************************/
/*
* NBAP AUX TImer Expiry handling
*
*****************************************************************************/
INPUT rnw_param_wait_timer;
DCL
  l_cell_list        cid_index_tbl__t,
  l_index            dword :=0;

  CALL c_test_hand_table__r(l_cell_list, alarm_state_t_start_c);

  OUTPUT send_cell_barred_info_s(msg_b93b_data) TO w_wcel_map(l_index).cell_info.cell_local.rra_cma_pid;
  NEXTSTATE -;

ENDSTATE working;
		'''

	def test_procedure_list():
		lines = get_procedure_name_lines(text)
		procedure_name_list = procedure_names_from_lines(lines)
		print procedure_name_list
		procedures = procedures_with_names(text, procedure_name_list)
		print procedures

	def test_input_list():
		lines = get_input_signal_name_lists(text)
		name_list = input_signal_names_from_lines(lines)
		print name_list
		#print input_signal_text_with_name(text, 'INPUT rnw_param_wait_timer')
		input_signals = input_signals_with_names(text, name_list)
		print input_signals

	def test_get_procedure_list():
		procedures = get_procedure_list(text)
		print_dict(procedures)

	def test_get_input_list():
		inputs = get_input_list(text)
		print_dict(inputs)

	def test_is_procedure_called_in_code():
		print is_procedure_called_in_code('get_service_provider__r', text)
		print is_procedure_called_in_code('get_sub_id', text)
		print is_procedure_called_in_code('send_dump_req__r', text)

	def test_get_called_functions():
		expected = ['get_service_provider__r', 'get_sub_id', 'send_dump_req__r', 'query_cosit_stat_from_rak__r', 'c_test_hand_table__r']
		print get_called_functions(text)
		


	def print_list(a_list):
		print '[' + '\n,\n'.join(a_list) + ']'

	def print_dict(a_dict):
		for k, v in a_dict.items():
			print k, v

	def test():
		#test_procedure_list()
		#test_input_list()
		#test_get_procedure_list()
		#test_get_input_list()
		#test_is_procedure_called_in_code()
		test_get_called_functions()
	


	test()