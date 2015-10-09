import os
import shutil
import sys



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


def operate(source, distination):
	shutil.move(source, distination)
	print 'move: %s --> %s' % (source, distination)


def merge_files(source_folder_path, distination_folder_path, files):
	for file_name in files:
		source_path = os.path.join(source_folder_path, file_name)
		distination_path = os.path.join(distination_folder_path, file_name)
		merge_a_file(source_path, distination_path)


def merge_a_file(source_path, distination_path):
	if os.path.exists(distination_path): 
		print 'skip: %s' % distination_path
		return
	operate(source_path, distination_path)


def merge_folders(source_folder_path, distination_folder_path, folders):
	for folder_name in folders:
		merge_folder(source_folder_path, distination_folder_path, folder_name)


def merge_folder(source_folder_path, distination_folder_path, folder_name):
	source_path = os.path.join(source_folder_path, folder_name)
	distination_path = os.path.join(distination_folder_path, folder_name)
	if os.path.exists(distination_path):
		merge(source_path, distination_path)
	else:
		operate(source_path, distination_path)
	


def merge(source_folder_path, distination_folder_path):
	if source_folder_path == distination_folder_path:
		print 'source and distination are same target'
		return
	children = get_children_of_folder(source_folder_path)
	print children
	if not children: return
	if children['files']:
		merge_files(source_folder_path, distination_folder_path, children['files'])
	if children['folders']:
		merge_folders(source_folder_path, distination_folder_path, children['folders'])


def main():
	if len(sys.argv) < 3:
		print 'Please input source folder, distination folder.'
		exit(0)
	source_folder_path = sys.argv[1]
	distination_folder_path = sys.argv[2]
	merge(source_folder_path, distination_folder_path)


if __name__ == '__main__':
	main()