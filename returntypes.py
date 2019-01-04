"""
This module contains a dictionary that maps return types to type-correct default return values.
These default return values are then used in generate.py according to the return type of each 
method in the corresponding interface.

Written by: Andrew Greenwell
Last edited: Jan 3, 2019
"""

values = {
	'boolean': 'false',
	'byte': '0',
	'char': '\'-\'',
	'character': '\'-\'',
	'double': '0.0d',
	'float': '0.0f',
	'int': '0',
	'integer': '0',
	'long': '0L',
	'short': '0',
}
