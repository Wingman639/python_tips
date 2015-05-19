import struct
import re

def _convert_file_to_wireshark_format(file_name):
    with open(file_name) as org_f:
        hex_str = org_f.read()

    with open(file_name.replace('log','cap'),"wb") as convert_f:
        _convert_to_cap_format(hex_str, convert_f)
     
def _convert_to_cap_format(hex_str, convert_f):
    pcap_head = ['D4','C3','B2','A1','02','00','04','00','00','00','00','00','00','00','00','00','FF','FF','00','00','01','00','00','00']
    for item in pcap_head:
        bytes = struct.pack('B', int(item,16))
        convert_f.write(bytes)
    
    
    pattern = re.compile(r'\w{2}')
    packages = hex_str.split('\n\n')
    for package in packages:
        if package == '':
            continue
        info = package.split(':\n')   
        time_stemp = re.findall(r'\[.+\]', info[0])[0][1:-1]
        second = time_stemp.split('.')[0].strip()
        mic_second = time_stemp.split('.')[1].strip()
        convert_f.write(struct.pack('i', int(second))) 
        convert_f.write(struct.pack('i', int(mic_second)*1000))    
        str_data = info[1]
        data = []
        for line in str_data.splitlines():
            line_list = pattern.findall(line)
            if line_list:    
                data.extend(line_list)
        package_len = len(data)
        convert_f.write(struct.pack('I', package_len))
        convert_f.write(struct.pack('I', package_len))
        for i in data:
            bytes = struct.pack('B', int(i,16))
            convert_f.write(bytes)
    

def main():
    _convert_file_to_wireshark_format('eth.log')

if __name__ == '__main__':
    main()