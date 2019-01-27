"""
This module contains all the methods for writing out to the class file. The 'expressions' dictionary 
acts as a repository of metadata that improves the extensibility and orthogonality of this application. 
Thus, If you wanted the JavaClassGenerator to successfully parse and match more regular expressions, 
you could define the proper write_ methods and add the relevant metadata to the 'expressions' dictionary, 
all without having to modify the parser in the generate.py module.


Written by: Andrew Greenwell
"""

import settings
import returntypes

_class_name = ""

#writes out the proper import statement
def write_import(class_file, module):
	class_file.write('import ' + module + '\n')


# writes out the proper method definition
def write_method(class_file, return_type, name, args):
	template = ' ' * settings._num_spaces + 'public ' + '{} {}({}) {{ return{}; }}\n'
	try:
		return_value = returntypes.values[return_type.lower()]
	except:
		return_value = ' null'
	class_file.write(template.format(return_type, name, args, return_value))


# writes out the proper class definition
def write_class(class_file, interface, generic, generic_extends):
	template = '\npublic class {}{} implements {}{} {{\n\n'
	class_name = _class_name.rstrip('.java')
	if generic_extends:
		class_file.write(template.format(class_name, generic, interface, '<' + generic_extends + '>'))
	else:
		class_file.write(template.format(class_name, generic, interface, generic))


# contains relevant metadata about each regex string and its corresponding function 
# that are used in generate.parse() to provide a more orthogonal and extensible design
expressions = {

	'interface': {

				"regex": '^ *public interface ([^ <>]+) {.*|^ *public interface ([^ <>]+) extends .*{.*',
				"num_groups": 1,
				"function": write_class,
				"num_args": 4

				},
	'interface_generic': {

				"regex": '^ *public interface ([^ <>]+)(<(?!.*extends).+>) {.*',
				"num_groups": 2,
				"function": write_class,
				"num_args": 4

				},
	'interface_generic_extends': {

				"regex": '^ *public interface ([^ <>]+)(<(.+) extends .+>) {.*',
				"num_groups": 3,
				"function": write_class,
				"num_args": 4

				},
	'import': {

				"regex": '^ *import (.+;).*',
				"num_groups": 1,
				"function": write_import,
				"num_args": 2

				},
	'method': {

				"regex": '^ *([\S]+) ([\S]+)\((.*)\);.*|^ *public ([\S]+) ([\S]+)\((.*)\);.*',
				"num_groups": 3,
				"function": write_method,
				"num_args": 4

				}
}
