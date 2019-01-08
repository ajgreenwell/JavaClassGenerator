"""
This is a script for generating type-correct Java classes (implementations) from their 
corresponding interfaces. By passing a java interface to this generator at the command line,
an implementation file will be automatically constructed with all the proper method definitions. 
Each method will return a predefined value in order to make the file compilable, as specified in 
the returntypes.py module.

Written by: Andrew Greenwell

TO DO:
  + fill out the README
  + add more comments
  + delete print statements
  + fix 'interface_generic' regex and
  	get rid of the patch up in parse()
"""

import syntax
import sys
import re
import returntypes as rt
import os


_interface = ""
_className = ""
_classFile = None
_comments = '/*\nThis class file has been automatically generated from ' + \
		    'its corresponding {} interface.\nIf that interface extends any ' + \
		    'others, you may need to define additional methods within this class.\n\nWritten by: {}\n*/\n\n'
_num_spaces = 0


def init_method(scope, return_type, name, args):
	template = ' ' * _num_spaces + '{} ' + '{} {}({}) {{ return {}; }}\n'
	try:
		return_value = rt.values[return_type.lower()]
	except:
		return_value = 'null'
	_classFile.write(template.format(scope, return_type, name, args, return_value))


def init_class(generic=None, generic_extends=None):
	template = '\npublic class {}{} implements {}{} {{\n\n'
	className = _className.rstrip('.java')
	interface = _interface.rstrip('.java')
	if generic and not generic_extends:
		_classFile.write(template.format(className, generic, interface, generic))
	elif generic and generic_extends:
		_classFile.write(template.format(className, generic, interface, generic_extends))
	else:
		_classFile.write(template.format(className, '', interface, ''))


def parse(line):
	for category, exp in syntax.valid.items():
		match = re.compile(exp).fullmatch(line)
		if match and category == 'import':
			_classFile.write(match.group(1) + '\n')
		elif match and category == 'interface':
			init_class()
		elif match and category == 'interface_generic':
			match2 = re.compile(syntax.valid['interface_generic_extends']).fullmatch(line)
			# if line matches interface_generic regex, first check if it matches interface_generic_extends,
			# since the latter regex string is a more specific version of the former
			if match2:
				init_class(generic=match2.group(2), generic_extends='<' + match2.group(3) + '>')
			else:
				init_class(generic=match.group(1))
			break
		elif match and category == 'interface_generic_extends':
			init_class(generic=match.group(2), generic_extends='<' + match.group(3) + '>')
		elif match and category == 'method':
			init_method('public', match.group(1), match.group(2), match.group(3))
		elif match and category == 'public_method':
			init_method(match.group(1), match.group(2), match.group(3), match.group(4))


def set_globals():
	global _className
	global _classFile
	global _interface
	global _num_spaces

	_className = input('Please enter the name of your class file: ')
	_classFile = open(_className, 'a')

	try:
		_interface = sys.argv[1]
		# init new class file with boilerplate comments, so it can be appended to later
		with open(_className, 'w') as f:
			f.write(_comments.format(_interface, 'Andrew Greenwell')) # os.getenv('USER', 'Your Name')
	except:
		print('***InvalidFilenameError*** : File Does Not Exist')
		return False

	# If the user passed in the number of desired indentation spaces, record it for future use.
	# Otherwise, default to its global value of 2.
	try:
		_num_spaces = int(sys.argv[2])
	except:
		_num_spaces = 2

	return True


def main():
	if not set_globals():
		exit()
	file = open(_interface, 'r')
	for line in file:
		line = line.rstrip('\n')
		print(line)
		parse(line)

	_classFile.write(' ' * _num_spaces + 'public static void main(String[] args) {}\n\n')
	_classFile.write('}\n')
	_classFile.close()
	file.close()


if __name__ == '__main__':
	main()
