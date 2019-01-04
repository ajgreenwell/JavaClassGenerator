"""
This module contains a dictionary that maps categories of regular expressions to 
their corresponding regex strings. These regex strings are then accessed and compiled 
in generate.py to find matches while parsing the provided interface.

Written by: Andrew Greenwell
Last edited: Jan 4, 2019
"""

valid = {
	'interface': '^ *public interface [\S]+.*',
	'method': '^ *([\S]+) ([\S]+)\((.*)\);.*',
	'public_method': '^ *(public) ([\S]+) ([\S]+)\((.*)\);.*',
	'public_static_method': '^ *(public static) ([\S]+) ([\S]+)\((.*)\);.*',
	'static_method': '^ *(static) ([\S]+) ([\S]+)\((.*)\);.*',
}