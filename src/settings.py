"""
This module contains global variables that serve as customizable settings for users of the JavaClassGenerator.
Note that modifying the comments variable could necessitate modifying line 89 of generate.py in order to resolve
any string formatting exceptions.

Written by: Andrew Greenwell
"""

author = 'Andrew Greenwell'
num_spaces = 2
comments = '/*\nThis class file has been automatically generated from ' + \
		   'its corresponding {interface} interface.\nIf that interface extends any ' + \
		   'others, you may need to define additional methods within this ' + \
		   'class.\n\nWritten by: {author}\n*/\n\n'.format(author=author)