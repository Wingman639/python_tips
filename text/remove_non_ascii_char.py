import sys


def replace_non_ascii_char_with_dot(text):
	return ''.join([c if ord(c) < 128 else '.' for c in text])


def remove_non_ascii_from_file_path(file_path):
	with open(file_path, 'r') as source_file:
		with open('new.txt', 'w') as new_file:
			line = source_file.readline()
			while line:
				new_line = replace_non_ascii_char_with_dot(line)
				new_file.write(new_line)
				line = source_file.readline()



def main():
	if len(sys.argv) < 2:
		print 'File path required.'
		return
	file_path = sys.argv[1]
	remove_non_ascii_from_file_path(file_path)

if __name__ == '__main__':
	main()

