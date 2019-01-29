"""
This is a script for generating type-correct Java classes (implementations) from their 
corresponding interfaces. By passing a java interface to this generator at the command line,
an implementation file will be automatically constructed with all the proper method definitions. 
Each method will return a predefined value in order to make the file compilable, as specified in 
the returntypes.py module. See syntax.py for details about regex matching and class file generation.

Written by: Andrew Greenwell
"""

import settings
import syntax
import sys
import re

# Checks each regex string in syntax.py to look for matches on provided line.
# Returns a tuple containing the match object and the relevant expression data
# from syntax.py if a match is found. Else returns a tuple containing False.
def parse(line):
	for category, expr_data in syntax.expressions.items():
		match = re.compile(expr_data["regex"]).fullmatch(line)
		if match:
			return (match, expr_data)
	return (False, False)


# Generates list of args to pass handler function based off regex metadata (see syntax.py).
# Then calls the appropriate handler function to write out the proper Java code
def write_to_class_file(class_file, match, expr_data):
	args = [class_file] # every function in syntax.py requires the class_file as 1st arg
	regex_specific_args = [match.group(group_num) for group_num \
						   in range(1, expr_data["num_groups"] + 1)]
	args.extend(regex_specific_args)
	if len(args) != expr_data["num_args"]:
		args.extend(['' for arg in range(0, expr_data["num_args"] - len(args))])
	# unpack args list and pass to appropriate handler function
	expr_data["function"](*args)


def main():
	# get command line args and set variables accordingly
	try:
		interface_name = sys.argv[1]
	except:
		print('***InvalidArgumentError*** : First Arg Must be a Valid Interface')
		exit(1)
	try:
		settings._num_spaces = int(sys.argv[2])
	except:
		pass

	# if the user provided a relative path to the interface, save it
	# to store the new class file in that same directory
	path = ''
	if '/' in interface_name:
		relative_path_list = interface_name.split('/')
		path = '/'.join(relative_path_list[:-1]) + '/'

	# open interface and class files for reading and writing
	try:
		interface_file = open(interface_name, 'r')
	except:
		print('***InvalidFilenameError*** : File or Relative Path Does Not Exist')
		exit(1)
	syntax._class_name = input('Please enter the name of your class file: ')
	class_file = open(path + syntax._class_name, 'a')
	class_file.write(settings._comments.format(interface_name))

	# main loop that parses each line of the interface and writes out corresponding Java code
	for line in interface_file:
		match, expr_data = parse(line.rstrip('\n'))
		if match:
			write_to_class_file(class_file, match, expr_data)
	
	# write out boilerplate closing lines and free up resources
	class_file.write(' ' * settings._num_spaces + \
					 'public static void main(String[] args) {}\n\n}\n')
	class_file.close()
	interface_file.close()


if __name__ == '__main__':
	main()
