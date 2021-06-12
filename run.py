#!/usr/bin/env python

import os
from jinja2 import Environment, FileSystemLoader
import configparser
from distutils.dir_util import copy_tree

# copy subdirectory example
fromDirectory = "static"
toDirectory = "docs"

copy_tree(fromDirectory, toDirectory)

def dir_str(path):
    # Create dir if desired
    if not os.path.isdir(path):
        os.makedirs(path)

def get_contents(config, section, property):
    contains_files = [os.path.join('contents', file_) for file_ in config[section][property].split(',')]
    contains_valid = [file_ for file_ in contains_files if os.path.isfile(file_)]
    invalid_files = [file_ for file_ in contains_files if not os.path.isfile(file_)]

    if len(invalid_files) != 0:
        print('WARN: %s : All files in %s doesn\'t exist in contents folder'%(section, property))
    
    content = ''
    for filename in contains_valid:
        with open(filename, 'r') as file_:
            content = content + '\n<!-- ' + os.path.basename(filename).split('.')[0] + ' Start-->\n' + \
            file_.read() + '\n<!-- ' + os.path.basename(filename).split('.')[0] + ' End-->\n'

    return content

def main():
    # Read Configuration File
    config = configparser.ConfigParser()
    config.read('pages.ini')
    pages = config.sections()
    # copy subdirectory example
    fromDirectory = "static"
    toDirectory = "docs"

    copy_tree(fromDirectory, toDirectory)
    # Create Page
    for page in pages:
        dir_str('docs')
        fname = os.path.join('docs', page.lower()+'.html')
        template_file = os.path.join('templates', config[page]['file_template'])
        content = get_contents(config, page, 'main_contains')
        sidebar = get_contents(config, page, 'sidebar_contains')             

        with open(template_file, 'r') as file_:
            templet = Environment(loader=FileSystemLoader('templates/')).from_string(file_.read())

        with open(fname, 'w') as file_:
            file_.write(templet.render(content=content, sidebar=sidebar))

if __name__ == '__main__':
    main()