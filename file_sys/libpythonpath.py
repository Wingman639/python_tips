import os
import shutil

def get_resource_library_folder(dir_path):
	dir_list = os.listdir(dir_path)
	for dir_name in dir_list:
		if dir_name.lower() == 'resources':
			lib_part = os.path.join(dir_name, r'library')
			return os.path.join(dir_path, lib_part) 


def get_library_list(root_path):
	library_list = []
	dir_list = os.listdir(root_path)
	for path in dir_list:
		if os.path.isdir(path):
			dir_name = os.path.join(root_path, path)
			new_path = get_resource_library_folder(dir_name)
			if new_path:
				if os.path.exists(new_path):
					library_list.append(new_path)
	return library_list


def copy_children_to_lib_folder(lib_folder_path, path_list):
	for path in path_list:
		if os.path.isdir(path):
			children = os.listdir(path)
			copy_to_lib_folder(lib_folder_path, path, children)


def copy_to_lib_folder(lib_folder_path, src_folder, item_list):
	for item in item_list:
		src_path = os.path.join(src_folder, item)
		dist_path = os.path.join(lib_folder_path, os.path.basename(src_path))
		if os.path.exists(src_path) and not os.path.exists(dist_path):
			if os.path.isdir(src_path):
				shutil.copytree(src_path, dist_path)


def create_lib_folder(root_path):
	folder_name = 'libs'
	lib_folder_path = os.path.join(root_path, folder_name)
	children = os.listdir(root_path)
	if folder_name not in children:
		os.mkdir(lib_folder_path)
	return lib_folder_path



def new_init_file(root_path):
	with open(os.path.join(root_path, '__init__.py'), 'w') as f:
		f.write('')


def main():
	current_path = os.path.dirname(__file__)
	lib_list = get_library_list(current_path)
	lib_folder_path = create_lib_folder(current_path)
	copy_children_to_lib_folder(lib_folder_path, lib_list)
	new_init_file(lib_folder_path)


if __name__ == '__main__':
	main()
