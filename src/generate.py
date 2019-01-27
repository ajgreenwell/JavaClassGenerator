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

# checks each regex string in syntax.py to look for matches on the provided line
# depending on which regex gets matched, calls appropriate function to write out Java code
def parse(class_file, line):
	for category, expr_data in syntax.expressions.items():
		match = re.compile(expr_data["regex"]).fullmatch(line)
		if match:
			args = [class_file]
			args.extend([match.group(x) for x in range(1, expr_data["num_groups"] + 1)])
			if len(args) != expr_data["num_args"]:
				args.extend(['' for y in range(0, expr_data["num_args"] - len(args))])
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

	# open interface and class files for reading and writing
	try:
		interface_file = open(interface_name, 'r')
	except:
		print('***InvalidFilenameError*** : File Does Not Exist')
		exit(1)
	syntax._class_name = input('Please enter the name of your class file: ')
	class_file = open(syntax._class_name, 'a')
	class_file.write(settings._comments.format(interface_name))

	# main loop that parses each line of the interface and generates the corresponding class file
	for line in interface_file:
		parse(class_file, line.rstrip('\n'))
	
	# write out boilerplate closing lines and free up resources
	class_file.write(' ' * settings._num_spaces + 'public static void main(String[] args) {}\n\n}\n')
	class_file.close()
	interface_file.close()


if __name__ == '__main__':
	main()