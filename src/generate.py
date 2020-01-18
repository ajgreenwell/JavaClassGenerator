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
from handlers import handlers
from constants import CLASS_FILE_EXTENSION


def main():
    interface_name, class_name = get_user_input()
    with files(interface_name, class_name) as (interface_file, class_file):
        for handler, match in matching_lines(interface_file):
            class_file.write(handler.generate_code(match, class_name))


def get_user_input():
    return (get_interface_name(), prompt_for_class_name())


def get_interface_name():
    try:
        return sys.argv[1]
    except:
        handle_user_input_error('First Arg Must be a Valid Interface')


def prompt_for_class_name():
    class_name = input('Please enter the name of your class file: ')
    if is_java_file(class_name):
        return class_name
    handle_user_input_error(f'Your class name must end in "{CLASS_FILE_EXTENSION}"')


def handle_user_input_error(error_message):
    print(f'*** User Input Error *** : {error_message}', file=sys.stderr)
    exit(1)


def is_java_file(filename):
    return len(filename) > len(CLASS_FILE_EXTENSION) and  \
           filename[-5:] == CLASS_FILE_EXTENSION


@contextmanager
def files(interface_name, class_name):
    interface_file, class_file = init_files(interface_name, class_name)
    yield interface_file, class_file
    teardown_files(interface_file, class_file)


def init_files(interface_name, class_name):
    interface_file = open_interface_file(interface_name)
    path_to_interface = get_file_path(interface_name)
    class_file = open(path_to_interface + class_name, 'a')
    class_file.write(settings.comments.format(interface=interface_name))
    return (interface_file, class_file)


def teardown_files(interface_file, class_file):
    class_file.write(' ' * settings.num_spaces + \
                     'public static void main(String[] args) {}\n\n}\n')
    class_file.close()
    interface_file.close()


def open_interface_file(interface_name):
    try:
        return open(interface_name, 'r')
    except:
        handle_user_input_error('File or Relative Path Does Not Exist')


def get_file_path(filename):
    filename_has_path = '/' in filename
    if filename_has_path:
        directories = filename.split('/')
        return '/'.join(directories[:-1]) + '/'
    return ''


def matching_lines(file):
    for line in file:
        handler, match = parse_interface_code(line.rstrip('\n'))
        if handler and match: yield handler, match


def parse_interface_code(line):
    for handler in handlers:
        match = handler.match(line)
        if match:
            return (handler, match)
    return (False, False)
    
    
if __name__ == '__main__':
    main()
