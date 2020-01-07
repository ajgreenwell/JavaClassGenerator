"""
This is a script for generating type-correct Java classes (implementations) from their 
corresponding interfaces. By passing a java interface to this generator at the command line,
an implementation file will be automatically constructed with all the proper method definitions. 
Each method will return a predefined value in order to make the file compilable, as specified in 
the returntypes.py module. See handlers.py for details about regex matching and class file generation.

Written by: Andrew Greenwell
"""

import settings
import sys
from contextlib import contextmanager
from handlers import handler_objects
from constants import CLASS_FILE_EXTENSION


def is_java_file(filename):
    return len(filename) > len(CLASS_FILE_EXTENSION) and  \
           CLASS_FILE_EXTENSION in filename


def get_interface_name():
    try:
        interface_name = sys.argv[1]
        return interface_name
    except:
        print('***UserInputError*** : First Arg Must be a Valid Interface',
              file=sys.stderr)
        exit(1)


def prompt_for_class_name():
    class_name = input('Please enter the name of your class file: ')
    if not is_java_file(class_name):
        print(f'***UserInputError*** : Your class name must end in "{CLASS_FILE_EXTENSION}"',
              file=sys.stderr)
        exit(1)
    return class_name


def get_user_input():
    return (get_interface_name(), prompt_for_class_name())


def open_interface_file(filename, mode):
    try:
        interface_file = open(filename, mode)
        return interface_file
    except:
        print('***UserInputError*** : File or Relative Path Does Not Exist', 
              file=sys.stderr)
        exit(1)


def get_file_path(filename):
    path = ''
    filename_has_path = '/' in filename
    if filename_has_path:
        directories = filename.split('/')
        path = '/'.join(directories[:-1]) + '/'
    return path


def init_files(interface_name, class_name):
    interface_file = open_interface_file(interface_name, 'r')
    path_to_interface = get_file_path(interface_name)
    class_file = open(path_to_interface + class_name, 'a')
    class_file.write(settings.comments.format(interface=interface_name))
    return (interface_file, class_file)


def teardown_files(interface_file, class_file):
    class_file.write(' ' * settings.num_spaces + \
                     'public static void main(String[] args) {}\n\n}\n')
    class_file.close()
    interface_file.close()


@contextmanager
def files(interface_name, class_name):
    interface_file, class_file = init_files(interface_name, class_name)
    yield interface_file, class_file
    teardown_files(interface_file, class_file)


# checks each handler object to look for regex matches on provided line
def parse_interface_code(line):
    for category, handler in handler_objects.items():
        match = handler.match(line)
        if match:
            return (handler, match)
    return (False, False)


# generator that finds relevant lines of java interface
# code and yields the appropriate handlers and match objects
def matching_lines(file):
    for line in file:
        handler, match = parse_interface_code(line.rstrip('\n'))
        if handler and match: yield handler, match


def main():
    interface_name, class_name = get_user_input()
    with files(interface_name, class_name) as (interface_file, class_file):
        # parses each line of the interface and generates the corresponding java code
        for handler, match in matching_lines(interface_file):
            class_file.write(handler.generate_code(match, class_name))
    
    
if __name__ == '__main__':
    main()
