"""
This is a script for generating type-correct Java classes (implementations) from their 
corresponding interfaces. By passing a java interface to this generator at the command line,
an implementation file will be automatically constructed with all the proper method definitions. 
Each method will return a predefined value in order to make the file compilable, as specified in 
the returntypes.py module. See handlers.py for details about regex matching and class file generation.

Written by: Andrew Greenwell
"""

import settings
import sys
from handlers import handler_objects


# checks each handler object to look for regex matches on provided line
def parse_interface_code(line):
	for category, handler in handler_objects.items():
		match = handler.match(line)
		if match:
			return (match, handler)
	return (False, False)


# If the user provided a relative path to the 
# interface, return it. Else, return the null string.
def get_file_path(interface_name):
	path = ''
	interface_has_path = '/' in interface_name
	if interface_has_path:
		directory_list = interface_name.split('/')
		path = '/'.join(directory_list[:-1]) + '/'
	return path


# attempts to return provided command line arg
# upon failure, prints appropriate error message and exits 
def get_interface_name():
	interface_name = ''
	try:
		interface_name = sys.argv[1]
	except:
		print('***InvalidArgumentError*** : First Arg Must be a Valid Interface', \
			  file=sys.stderr)
		exit(1)
	return interface_name


# returns file object of user provided filename, opened in the mode provided
# checks validity of filename -- if not valid, displays error message and exits
def open_interface_file(filename, mode):
	interface_file = ''
	try:
		interface_file = open(filename, mode)
	except:
		print('***InvalidFilenameError*** : File or Relative Path Does Not Exist', 
			  file=sys.stderr)
		exit(1)
	return interface_file


# returns user provided class name, after ensuring it contains the ".java" extension
def prompt_for_class_name():
	class_name = input('Please enter the name of your class file: ')
	class_name_length = len(class_name)
	isJavaFile = class_name_length > 5 and \
	             class_name[class_name_length - 5 :] == '.java'
	if not isJavaFile:
		print('***UserInputError*** : Your class name must end in ".java"',
			  file=sys.stderr)
		exit(1)
	return class_name


def main():
	# get user input
	interface_name = get_interface_name()
	class_name = prompt_for_class_name()

	# open interface and class files for reading and writing
	interface_file = open_interface_file(interface_name, 'r')
	path_to_interface = get_file_path(interface_name)
	class_file = open(path_to_interface + class_name, 'a')

	# file extension is no longer needed
	class_name = class_name.rstrip('.java')

	# write out boilerplate comments from settings.py
	class_file.write(settings.comments.format(interface_name))

	# main loop that parses each line of the interface
	for line in interface_file:
		match, handler = parse_interface_code(line.rstrip('\n'))
		if match and handler:
			code = handler.generate_code(match, class_name)
			class_file.write(code)
	
	# write out boilerplate closing lines and free up resources
	class_file.write(' ' * settings.num_spaces + \
	                 'public static void main(String[] args) {}\n\n}\n')
	class_file.close()
	interface_file.close()


if __name__ == '__main__':
	main()
