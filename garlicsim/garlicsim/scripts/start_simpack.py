#!/usr/bin/env python
# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Script for starting a new simpack.

Usage:
start_simpack.py quantum_mechanics
'''


from __future__ import with_statement

import os.path
import sys
import re
import shutil

import pkg_resources

from garlicsim.scripts import simpack_template
simpack_template_package_name = simpack_template.__name__

    
def _walk_folder(package_name, folder):
    '''
    Walk on subfolders of a folder using pkg_resources.

    `package_name` is the name of the package in which this folder lives.
    `folder` is the path of the folder.
    
    Of course, since we are operating using pkg_resources, all paths are
    relative to the pkg_resources-managed package.
    '''
    folders = [folder]
    
    while folders:
        folder = folders.pop()
        for f in pkg_resources.resource_listdir(package_name, folder):
            path = '/'.join((folder, f))
            if pkg_resources.resource_isdir(package_name, path):
                folders.append(path)
            else:
                yield path
        

def _make_path_to_file(file):
    '''
    Create the folders needed before creating a file.
    
    Given a path to a file that doesn't exist, this function creates all the
    folders up to the file, so the file could be later created without thinking
    whether these folders exist or not.
    '''
    dir = os.path.split(file)[0]
    if os.path.isdir(dir):
        return
    parent_dir = os.path.split(dir)[0]
    _make_path_to_file(dir)
    os.mkdir(dir)
    
                
    
def start_simpack(containing_folder, name):
    """
    Create a new simpack.
    
    This is the main function of this module. `containing_folder` is the folder
    in which the simpack folder should be created. `name` is the name of the new
    simpack, which will also be the name of its folder.
    """
    
    if not re.search(r'^[_a-zA-Z]\w*$', name): # If not valid folder name.
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
        raise Exception("%r is not a valid simpack name. Please %s." %
                        (name, message))
    folder = os.path.join(containing_folder, name)
    
    os.mkdir(folder)
    
    for file in _walk_folder(simpack_template_package_name, './simpack_name'):
        
        if os.path.splitext(file)[1] in ('.pyc', '.pyo'):
            continue
        
        dest_file = '/'.join(
            (containing_folder, file.replace('simpack_name', name))
        )
        
        _make_path_to_file(dest_file)
        
        with pkg_resources.resource_stream(simpack_template_package_name, file) as source:
            with open(dest_file, 'wb') as destination:
                
                string_to_write = source.read().replace('simpack_name', name)
                
                destination.write(string_to_write)
            
        try:
            shutil.copymode('/'.join(('simpack_template', file)), dest_file)
            _make_writeable(dest_file)
        except Exception:
            pass
    print('''%s simpack created successfully! Explore the %s folder and start \
filling in the contents of your new simpack.''' % (name, name))
                
    
def _make_writeable(filename):
    """
    Make sure that the file is writeable. Useful if our source is
    read-only.
    """
    import stat
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)

        
def show_help():
    '''Print some help text that describes how to use this script'''
    print '''\
This is a script for creating a skeleton for a garlicsim simpack. Use this when
you want to make a new simpack to have the basic folders and files created for
you.

    Usage: start_simpack.py my_simpack_name

The simpack will be created in the current path, in a directory with the name of
the simpack.'''
    return

    
if __name__ == '__main__':

    if len(sys.argv) != 2:
        show_help()
        sys.exit()
    arg = sys.argv[1]

    if arg == '--help':
        show_help()
        sys.exit()
    
    start_simpack(os.curdir, arg)
    
        