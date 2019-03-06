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


class CommandLineArgErrs():

	__INTERFACE_ERROR_MSG = '***InvalidArgumentError*** : First Arg Must be a Valid Interface'
	__INDENTATION_ERROR_MSG = None

	__ERR_MESSAGES = {

	'1': __INTERFACE_ERROR_MSG,
	'2': __INDENTATION_ERROR_MSG

	}

	@classmethod
	def get_err_msg(cls, arg_num):
		return cls.__ERR_MESSAGES[str(arg_num)]


# Checks each handler object to look for regex matches on provided line.
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


def get_command_line_arg(arg_num):
	arg = ''
	try:
		arg = sys.argv[arg_num]
		return arg
	except:
		err_msg = CommandLineArgErrs.get_err_msg(arg_num)
		if err_msg:
			print(err_msg, file=stderr)
			exit(1)


def open_interface_file(filename, mode):
	interface_file = ''
	try:
		interface_file = open(filename, mode)
	except:
		print('***InvalidFilenameError*** : File or Relative Path Does Not Exist', 
			  file=sys.stderr)
		exit(1)
	return interface_file


def prompt_for_class_name():
	class_name = input('Please enter the name of your class file: ')
	isJavaFile = class_name[len(class_name) - 5 :] == '.java'
	if not isJavaFile:
		print('***UserInputError*** : Your class name must end in ".java"')
		exit(1)
	return class_name


def main():
	# get command line args and user input
	interface_name = get_command_line_arg(1)
	class_name = prompt_for_class_name()

	num_spaces = get_command_line_arg(2)
	if num_spaces:
		settings._num_spaces = int(num_spaces)

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
