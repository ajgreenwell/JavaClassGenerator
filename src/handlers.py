"""
This module contains class definitions for all the handlers used in generate.py. Each handler 
acts as a translator between Java interface code and its corresponding Java class code. In order
to generalize calls to generate_code() by clients, the handlers take care of extracting all 
necessary data from each match object and passing that data to the approriate methods. 

Note that any classes, methods, or variables prepended by a single underscore are not "mangled,"
but are "protected." They are not intended to be accessed directly by client code, yet they are 
still inheritable by subclasses.

Written by: Andrew Greenwell
"""

import settings
import returntypes
import re

# protected parent class of all handler classes – not intended to be instantiated
class _RegexHandler(): 

	# args list that will be packed and passed to child's _generate_code()
	_args = []
	# number of args required to call child's _generate_code(); overridden in child classes
	_num_args = 0

	def __init__(self, regex):
		self._regex = re.compile(regex)

	# uses match object to extract all necessary arguments for child's 
	# _generate_code(), then packs them into the _args class variable
	def _pack_args_list(self, match):
		self._args.extend(match.groups()) # handler specific args
		# if more args are required, pack in null strings for them
		if len(self._args) < self._num_args:
			self._args.extend(['' for arg in range(self._num_args - len(self._args))])

	# returns a match object (see re.py module) 
	# if there is a full match, else returns None
	def match(self, line):
		return self._regex.fullmatch(line)
	
	# will be overridden in InterfaceHandler, where 'class_name' arg is used
	def generate_code(self, match, class_name):
		self._pack_args_list(match)
		# unpack args list and pass to child's protected method
		code = self._generate_code(*self._args)
		# necessary for reuse of the _args list
		self._args.clear()
		return code


# public class for handling interface declarations
class InterfaceHandler(_RegexHandler):

	_code_template = '\npublic class {}{} implements {}{} {{\n\n'
	_num_args = 3 # numbers of args necessary to call _generate_code()
	_class_name = ""

	def _set_class_name(self, class_name):
		self._class_name = class_name

	def _generate_code(self, interface, generic, generic_extends):
		extension = generic if not generic_extends else '<' + generic_extends + '>'
		return self._code_template.format(self._class_name, generic, interface, extension)

	# overrides parent method
	def generate_code(self, match, class_name):
		self._set_class_name(class_name)
		return super().generate_code(match, class_name)


# public class for handling method definitions
class MethodHandler(_RegexHandler):

	_code_template = ' ' * settings.num_spaces + 'public ' + '{} {}({}) {{ return{}; }}\n'
	_num_args = 3

	def _generate_code(self, return_type, name, args):
		try:
			return_value = returntypes.values[return_type.lower()]
		except:
			return_value = ' null'
		return self._code_template.format(return_type, name, args, return_value)


# public class for handling import statements
class ImportHandler(_RegexHandler):

	_code_template = 'import {}\n'
	_num_args = 1 

	def _generate_code(self, module):
		return self._code_template.format(module)


# map of instatiated handler objects – each of which is 
# used to handle Java interface file code in generate.py
handler_objects = {

	'interface': 

		InterfaceHandler('^ *public interface ([^ <>]+) {.*'),

	'interface_extends': 

		InterfaceHandler('^ *public interface ([^ <>]+) extends .*{.*'),

	'interface_generic': 

		InterfaceHandler('^ *public interface ([^ <>]+)(<(?!.*extends).+>) {.*'),

	'interface_generic_extends': 

		InterfaceHandler('^ *public interface ([^ <>]+)(<(.+) extends .+>) {.*'),

	'import': 

		ImportHandler('^ *import (.+;).*'),

	'method': 

		MethodHandler('^ *([\S]+) ([\S]+)\((.*)\);.*'),

	'public_method': 

		MethodHandler('^ *public ([\S]+) ([\S]+)\((.*)\);.*')
}


# some unit testing
if __name__ == '__main__':

	import_handler = handler_objects['import']
	interface_handler = handler_objects['interface_generic']
	method_handler = handler_objects['public_method']

	import_code = 'import java.util.*;'
	interface_code = 'public interface SampleInterface<X, Y> {'
	method_code = 'public boolean isValid(arg);'

	import_match = import_handler.match(import_code)
	interface_match = interface_handler.match(interface_code)
	method_match = method_handler.match(method_code)

	class_name = 'SampleClass'

	print(import_handler.generate_code(import_match, class_name), end='')
	print(interface_handler.generate_code(interface_match, class_name), end='')
	print(method_handler.generate_code(method_match, class_name), end='\n}\n')




