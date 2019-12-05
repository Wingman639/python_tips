

def main_error_text_of_log_line(line):
    pos = line.find('|TEXT:')
    return line[pos:]

main_info_set = set([])

with open('new.txt', 'w+') as wf:
    with open('syslog.txt', 'r') as rf:
        for line in rf.readlines():
            main_err = main_error_text_of_log_line(line)
            if main_err not in main_info_set:
                main_info_set.add(main_err)
                wf.write(line)
                print main_err

print main_info_set