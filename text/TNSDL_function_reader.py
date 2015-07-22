
import re


def procedures_with_names(text, procedure_names):
	procedure_list = []
	for name in procedure_names:
		procedure = procedure_text_with_name(text, name)
		if procedure:
			procedure_list.append(procedure)
	return procedure_list

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
	return line.replace('PROCEDURE', '').strip('\n\r\t\f\v ;')

def get_procedure_name_lines(text):
	pattern_str = r'\sPROCEDURE\s.*?;'
	return findall_with_pattern_str(pattern_str, text)



### INPUT signal part

def input_signals_with_names(text, signal_names):
	input_signal_list = []
	for name in signal_names:
		input_signal_text = input_signal_text_with_name(text, name)
		if input_signal_text:
			input_signal_list.append(input_signal_text)
	return input_signal_list

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
	pattern_str = r'\sINPUT\s.*?[(;]'
	return findall_with_pattern_str(pattern_str, text)
	




## find all in text

def findall_with_pattern_str(pattern_str, text):
	pattern = re.compile(pattern_str, re.M|re.S)
	match = pattern.search(text)
	if match:
		return pattern.findall(text)
	else:
		return []


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
  DECISION ( sub_id );
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

  NEXTSTATE -;

ENDSTATE working;
		'''

	def test_procedure_list():
		lines = get_procedure_name_lines(text)
		procedure_name_list = procedure_names_from_lines(lines)
		print procedure_name_list
		procedure_list = procedures_with_names(text, procedure_name_list)
		print_list(procedure_list)

	def test_input_list():
		lines = get_input_signal_name_lists(text)
		name_list = input_signal_names_from_lines(lines)
		print name_list
		#print input_signal_text_with_name(text, 'INPUT rnw_param_wait_timer')
		input_signal_list = input_signals_with_names(text, name_list)
		print_list(input_signal_list)

	def print_list(a_list):
		print '[' + '\n,\n'.join(a_list) + ']'

	def test():
		test_procedure_list()
		test_input_list()
	


	test()