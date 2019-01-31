"""
This module contains global variables that serve as customizable settings for users of the JavaClassGenerator.
Note that modifying the comments variable could necessitate modifying line 60 of generate.py in order to resolve
any string formatting exceptions.

Written by: Andrew Greenwell
"""

num_spaces = 2
comments = '/*\nThis class file has been automatically generated from ' + \
		    'its corresponding {} interface.\nIf that interface extends any ' + \
		    'others, you may need to define additional methods within this ' + \
		    'class.\n\nWritten by: Andrew Greenwell\n*/\n\n'