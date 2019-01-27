"""
This module contains global variables that serve as customizable settings for users of the JavaClassGenerator.
Note that modifying the _comments variable could necessitate modifying line 50 of generate.py in order to resolve
any string formatting exceptions.

Written by: Andrew Greenwell
"""

_num_spaces = 2
_comments = '/*\nThis class file has been automatically generated from ' + \
		    'its corresponding {} interface.\nIf that interface extends any ' + \
		    'others, you may need to define additional methods within this ' + \
		    'class.\n\nWritten by: Andrew Greenwell\n*/\n\n'