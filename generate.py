"""
This is a script for generating type-correct Java classes (implementations) from their 
corresponding interfaces. By passing a java interface to this generator at the command line,
a corresponding implementation file will be constructed with all the proper method definitions. 
Each method will return a predefined value in order to make the file compilable, as specified in 
the returntypes.py module.

Written by: Andrew Greenwell
Last edited: Jan 4, 2019
"""

import syntax
import sys
import re
import returntypes as rt


_className = ""
_classFile = None
_comments = '/*\nThis class file has been automatically generated from its corresponding {} interface.\n\nWritten by: Andrew Greenwell\n*/\n\n'
_num_spaces = 2


def init_method(scope, return_type, name, args):
	template = ' ' * _num_spaces + '{} ' + '{} {}({}) {{ return {}; }}\n'
	try:
		return_value = rt.values[return_type.lower()]
	except:
		return_value = 'null'
	_classFile.write(template.format(scope, return_type, name, args, return_value))


def init_class():
	global _classFile
	template = 'public class {} implements {} {{\n\n'
	_classFile = open(_className, 'a')
	_classFile.write(template.format(_className.rstrip('.java'),
									 _className.rstrip('C.java')))

def parse(line):
	for category, exp in syntax.valid.items():
		match = re.compile(exp).match(line)
		if match and category == 'interface':
			init_class()
			return True
		elif match and category == 'method':
			init_method('public', match.group(1), match.group(2), match.group(3))
		elif match:
			init_method(match.group(1), match.group(2), match.group(3), match.group(4))
	

def main():
	global _className
	global _num_spaces

	# if the user passed in the number of desired indentation spaces, record it for future use
	# otherwise, default to its global value of 2
	try:
		_num_spaces = int(sys.argv[2])
	except:
		pass
	try:
		filename = sys.argv[1]
		_className = filename.rstrip('.java') + 'C.java'
		# init new class file with boilerplate comments, so it can be appended to later
		with open(_className, 'w') as f:
			f.write(_comments.format(filename))
		interface = open(filename, 'r')
	except:
		print('***InvalidFilenameError*** : File Does Not Exist')
		return

	# parse each line of the interface
	line_num = 1
	for line in interface:
		line = line.rstrip('\n')
		if parse(line) == False:
			print('***ParsingError*** : {} on Line {}'.format(filename, line_num))
			interface.close()
			return
		line_num += 1

	_classFile.write(' ' * _num_spaces + 'public static void main(String[] args) {}\n\n')
	_classFile.write('}\n')
	_classFile.close()
	interface.close()


if __name__ == '__main__':
	main()
