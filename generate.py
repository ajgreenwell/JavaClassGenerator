"""
This is a script for generating type-correct Java classes (implementations) from their 
corresponding interfaces. By passing a java interface to this generator at the command line,
an implementation file will be automatically constructed with all the proper method definitions. 
Each method will return a predefined value in order to make the file compilable, as specified in 
the returntypes.py module.

Written by: Andrew Greenwell

TO DO:
  + fix 'interface_generic' regex and
  	get rid of the patch up in parse()
"""

import syntax
import sys
import re
import returntypes

_interface = ""
_className = ""
_classFile = None
_comments = '/*\nThis class file has been automatically generated from ' + \
		    'its corresponding {} interface.\nIf that interface extends any ' + \
		    'others, you may need to define additional methods within this class.\n\nWritten by: {}\n*/\n\n'

# customizable settings
_name = 'Andrew Greenwell'
_num_spaces = 2


# writes out the proper method definition
def init_method(scope, return_type, name, args):
	template = ' ' * _num_spaces + '{} ' + '{} {}({}) {{ return {}; }}\n'
	try:
		return_value = returntypes.values[return_type.lower()]
	except:
		return_value = 'null'
	_classFile.write(template.format(scope, return_type, name, args, return_value))


# writes out the proper class definition
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


# checks each regex string in syntax.py to look for matches on the provided line
# depending on which regex gets matched, calls appropriate function to write out Java code
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
			break  # prevents double matching with interface_generic_extends
		elif match and category == 'interface_generic_extends':
			init_class(generic=match.group(2), generic_extends='<' + match.group(3) + '>')
		elif match and category == 'method':
			init_method('public', match.group(1), match.group(2), match.group(3))
		elif match and category == 'public_method':
			init_method(match.group(1), match.group(2), match.group(3), match.group(4))	


def main():
	global _className
	global _classFile
	global _interface
	global _num_spaces

	# get command line args and set global variables accordingly
	try:
		_interface = sys.argv[1]
	except:
		print('***InvalidArgumentError*** : First Arg Must be a Valid Interface')
		exit(1)

	try:
		_num_spaces = int(sys.argv[2])
	except:
		pass

	# open interface and class files for reading and writing
	try:
		file = open(_interface, 'r')
	except:
		print('***InvalidFilenameError*** : File Does Not Exist')
		_classFile.close()
		exit(1)

	_className = input('Please enter the name of your class file: ')
	_classFile = open(_className, 'a')
	_classFile.write(_comments.format(_interface, _name))


	# main loop that parses each line of the interface
	for line in file:
		line = line.rstrip('\n')
		parse(line)
	
	# write out boilerplate closing lines and free up resources
	_classFile.write(' ' * _num_spaces + 'public static void main(String[] args) {}\n\n')
	_classFile.write('}\n')

	_classFile.close()
	file.close()


if __name__ == '__main__':
	main()
