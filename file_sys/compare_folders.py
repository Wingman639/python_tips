import os
import shutil
import sys
import time

FULL_INFO_MODE = False
ONLY_DIFF_MODE = True
ONLY_SIZE_DIFF_MODE = True

def get_file_modify_time(file_path):
	t = time.localtime(os.stat(file_path).st_mtime)
	return time.strftime('%Y-%m-%d %H:%M:%S', t)

def readable_line(a, b, c):
	a_MAX = 100
	a_space = ' ' * (a_MAX - len(a))
	b_MAX = 20
	b_space = ' ' * (b_MAX - len(b))
	return ' '.join([a, a_space, b, b_space, c])


def get_children_of_folder(dir_path):
	if not os.path.isdir(dir_path): return
	items = os.listdir(dir_path)
	if not items: return
	children = {'root'		: dir_path,
				'files' 	: [], 
	            'folders' 	: [],
	           }
	for item in items:
		path = os.path.join(dir_path, item)
		if os.path.isdir(path):
			children['folders'].append(item)
		else:
			children['files'].append(item)
	return children


def compare_files(source_folder_path, distination_folder_path, files):
	for file_name in files:
		source_path = os.path.join(source_folder_path, file_name)
		distination_path = os.path.join(distination_folder_path, file_name)
		compare_a_file(source_path, distination_path)


def compare_a_file(source_path, distination_path):
	s_size = os.path.getsize(source_path)
	s_time = get_file_modify_time(source_path)
	if os.path.exists(distination_path): 
		d_size = os.path.getsize(distination_path)
		d_time = get_file_modify_time(distination_path)
		if ONLY_DIFF_MODE and (s_size == d_size) and (s_time == d_time): return
		if ONLY_SIZE_DIFF_MODE and (s_size == d_size): return
		if s_size == d_size:
			op_size = '='
		elif s_size > d_size:
			op_size = '>'
		else:
			op_size = '<'
		if s_time == d_time:
			op_time = '='
		elif s_time > d_time:
			op_time = '>'
		else:
			op_time = '<'
		size_output = '{} {} {}'.format(s_size, op_size, d_size)
		time_output = '{} {} {}'.format(s_time, op_time, d_time)
		print readable_line(source_path, size_output, time_output)
	else:
		print readable_line(source_path, str(s_size), s_time)
	


def compare_folders(source_folder_path, distination_folder_path, folders):
	for folder_name in folders:
		if '.svn' in folder_name: continue
		compare_folder(source_folder_path, distination_folder_path, folder_name)


def compare_folder(source_folder_path, distination_folder_path, folder_name):
	source_path = os.path.join(source_folder_path, folder_name)
	distination_path = os.path.join(distination_folder_path, folder_name)
	compare(source_path, distination_path)
	


def compare(source_folder_path, distination_folder_path):
	if source_folder_path == distination_folder_path:
		print 'source and distination are same target'
		return
	children = get_children_of_folder(source_folder_path)
	if FULL_INFO_MODE: print children
	if not children: return
	if children['files']:
		compare_files(source_folder_path, distination_folder_path, children['files'])
	if children['folders']:
		compare_folders(source_folder_path, distination_folder_path, children['folders'])


def main():
	if len(sys.argv) < 3:
		print 'Please input source folder, distination folder.'
		exit(0)
	source_folder_path = sys.argv[1]
	distination_folder_path = sys.argv[2]
	compare(source_folder_path, distination_folder_path)


if __name__ == '__main__':
	main()
	# print get_file_modify_time(sys.argv[1])