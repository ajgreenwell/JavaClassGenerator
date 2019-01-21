"""
This module contains a dictionary that maps categories of regular expressions to 
their corresponding regex strings. These regex strings are then accessed and compiled 
in generate.py to find matches while parsing the provided interface.

Written by: Andrew Greenwell
"""

# writes out the proper method definition
def init_method(file, scope, return_type, name, args):
	template = ' ' * _num_spaces + '{} ' + '{} {}({}) {{ return{}; }}\n'
	try:
		return_value = returntypes.values[return_type.lower()]
	except:
		return_value = ' null'
	file.write(template.format(scope, return_type, name, args, return_value))


# writes out the proper class definition
def init_class(file, interface, class_name, generic, generic_extends):
	template = '\npublic class {}{} implements {}{} {{\n\n'
	if generic and not generic_extends:
		file.write(template.format(className, generic, interface, generic))
	elif generic and generic_extends:
		file.write(template.format(className, generic, interface, generic_extends))
	else:
		file.write(template.format(className, '', interface, ''))


valid = {
	'interface': {
					'regex': '^ *public interface ([^ <>]+) {.*|^ *public interface ([^ <>]+) extends .*{.*',
					'func': init_class,
					'num_args',
				},
	'interface_generic': {
					'regex': '^ *public interface [^ <>]+(<.+>) {.*',
					'func': init_class
	'interface_generic_extends': '^ *public interface ([^ <>]+)(<(.+) extends .+>) {.*',
	'import': '^ *(import .+;).*',
	'method': '^ *([\S]+) ([\S]+)\((.*)\);.*',
	'public_method': '^ *(public) ([\S]+) ([\S]+)\((.*)\);.*'
}
