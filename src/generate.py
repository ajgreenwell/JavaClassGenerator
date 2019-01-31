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

# Checks each handler object to look for regex matches on provided line.
# Returns a tuple containing the match and handler objects if a match 
# is found. Else returns a tuple containing False.
def parse(line):
	for category, handler in handler_objects.items():
		match = handler.match(line)
		if match:
			return (match, handler)
	return (False, False)


# If the user provided a relative path to the 
# interface, return it. Else, return the null string.
def getPath(interface_name):
	path = ''
	if '/' in interface_name:
		relative_path_list = interface_name.split('/')
		path = '/'.join(relative_path_list[:-1]) + '/'
	return path


def main():
	# get command line args and set variables accordingly
	try:
		interface_name = sys.argv[1]
	except:
		print('***InvalidArgumentError*** : First Arg Must be a Valid Interface', 
			  file=sys.stderr)
		exit(1)
	try:
		settings.num_spaces = int(sys.argv[2])
	except:
		pass

	path_to_interface = getPath(interface_name)

	# open interface and class files for reading and writing
	try:
		interface_file = open(interface_name, 'r')
	except:
		print('***InvalidFilenameError*** : File or Relative Path Does Not Exist', 
			  file=sys.stderr)
		exit(1)
	class_name = input('Please enter the name of your class file: ')
	class_file = open(path_to_interface + class_name, 'a')
	class_file.write(settings.comments.format(interface_name))
	class_name = class_name.rstrip('.java')

	# main loop that parses each line of the interface and writes out corresponding Java code
	for line in interface_file:
		match, handler = parse(line.rstrip('\n'))
		if match:
			code = handler.generate_code(match, class_name)
			class_file.write(code)
	
	# write out boilerplate closing lines and free up resources
	class_file.write(' ' * settings.num_spaces + \
					 'public static void main(String[] args) {}\n\n}\n')
	class_file.close()
	interface_file.close()


if __name__ == '__main__':
	main()
