
_integer = int

_byte_length = 2


def dict_from_hex_record( hex_record, definition_dict ):
    hex_value_dict = _hex_value_dict_from_hex_str( hex_record, definition_dict )
    return _dict_from_hex_value_dict( hex_value_dict, definition_dict )


def _hex_value_dict_from_hex_str( hex_str, definition_dict ):
    hex_value_dict = {}
    begin_idx = 0
    end_idx = 0

    for key in definition_dict['order']:
        hex_length = definition_dict[key]['size'] * _byte_length
        end_idx = begin_idx + hex_length
        hex_value_dict[key] = hex_str[begin_idx : end_idx]
        begin_idx = end_idx
    return hex_value_dict


def _dict_from_hex_value_dict( hex_value_dict, definition_dict ):
    data = {}
    for key in hex_value_dict:
        field_definition = definition_dict[key]
        value = hex_value_dict[key]
        if field_definition['type'] == 'int':
            data[key] = _integer(value, 16)
        elif field_definition['type'] == 'str':
            data[key] = _hexToASCII(value)
        else:
            data[key] = value
    return data


def _hexToASCII( hex_str ):
    ending = _hexStrEnding( hex_str )
    hex_str = hex_str[: ending]
    return hex_str.decode('hex')


def _hexStrEnding( hex_str ):
    if '00' not in hex_str: return len(hex_str)
    i = hex_str.find('00')
    if (i % 2) > 0:
        i += 1      #in case '1000', expect '10' not '1'
    return i



#=======================================#

if __name__ == '__main__':


    prebts_t_definition = { 'prebts_id' :       {'size' : 2,    'type' : 'int'},
                            'wbts_id' :         {'size' : 2,    'type' : 'int'},
                            'version' :         {'size' : 10,   'type' : 'str'},
                            'tech_info' :       {'size' : 1,    'type' : 'int'},
                            'autoconn_siteid' : {'size' : 50,   'type' : 'str'},
                            'autoconn_hwid' :   {'size' : 11,   'type' : 'str'},
                            'spare' :           {'size' : 11,   'type' : None},
                            'order' : [ 'prebts_id',
                                        'wbts_id',
                                        'version',
                                        'tech_info',
                                        'autoconn_siteid',
                                        'autoconn_hwid',
                                        'spare']}


    #============================
    # Unit Testing
    #----------------------------
    import unittest

    class RNWDBHexTestCase(unittest.TestCase):

        def test_prebts_hex_from_hex_str(self):
            expected = {'prebts_id': '0001', 'tech_info': '03', 'autoconn_hwid': '4556303132333435363738', 'wbts_id': 'fffe',
                        'version': '57313600000000000000', 'spare': '0000000000000000',
                        'autoconn_siteid': '3031323334353637383930313233343536373839303132333435363738393031323334353637383900000000000000000000'}
            hexStr = '0001fffe5731360000000000000003303132333435363738393031323334353637383930313233343536373839303132\
333435363738390000000000000000000045563031323334353637380000000000000000'
            prebts_hex = _hex_value_dict_from_hex_str( hexStr, prebts_t_definition )
            #self.assertEqual( expected, prebts_hex )
            for k, v in prebts_hex.items():
                self.assertEqual( expected[k], v)




        def test_prebts(self):
            expected = {'prebts_id': 1, 'tech_info': 3, 'autoconn_hwid': 'EV012345678', 'wbts_id': 65534, 'version': 'W16', 'spare': '0000000000000000', 'autoconn_siteid': '0123456789012345678901234567890123456789'}
            prebts_hex = {'prebts_id': '0001', 'tech_info': '03', 'autoconn_hwid': '4556303132333435363738', 'wbts_id': 'fffe',
                        'version': '57313600000000000000', 'spare': '0000000000000000',
                        'autoconn_siteid': '3031323334353637383930313233343536373839303132333435363738393031323334353637383900000000000000000000'}
            prebts = _dict_from_hex_value_dict( prebts_hex, prebts_t_definition )
            self.assertEqual( expected, prebts )



        def test_hexStrEnding_all_zero(self):
            expected = 0
            hex_str = '0000'
            result = _hexStrEnding(hex_str)
            self.assertEqual( expected, result )


        def test_hexToASCII_all_zero(self):
            expected = ''
            hex_str = '0000'
            result = _hexToASCII(hex_str)
            self.assertEqual( expected, result )


    unittest.main()
