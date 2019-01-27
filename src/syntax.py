"""
This module contains a dictionary that maps categories of regular expressions to 
their corresponding regex strings. These regex strings are then accessed and compiled 
in generate.py to find matches while parsing the provided interface.

Written by: Andrew Greenwell
"""

valid = {
	'interface': '^ *public interface ([^ <>]+) {.*|^ *public interface ([^ <>]+) extends .*{.*',
	'interface_generic': '^ *public interface [^ <>]+(<(?!.*extends).+>) {.*',
	'interface_generic_extends': '^ *public interface ([^ <>]+)(<(.+) extends .+>) {.*',
	'import': '^ *(import .+;).*',
	'method': '^ *([\S]+) ([\S]+)\((.*)\);.*',
	'public_method': '^ *(public) ([\S]+) ([\S]+)\((.*)\);.*'
}

expressions = {
	'interface': {

				"regex": '^ *public interface ([^ <>]+) {.*|^ *public interface ([^ <>]+) extends .*{.*'

				 },
	'interface_generic': {

				"regex": '^ *public interface [^ <>]+(<(?!.*extends).+>) {.*'

				 },
	'interface_generic_extends': {

				"regex": '^ *public interface ([^ <>]+)(<(.+) extends .+>) {.*'

				},
	'import': {

				"regex": '^ *(import .+;).*'

				},
	'method': {

				"regex": '^ *([\S]+) ([\S]+)\((.*)\);.*'

				},
	'public_method': {

				"regex": '^ *(public) ([\S]+) ([\S]+)\((.*)\);.*'
				
				}
}