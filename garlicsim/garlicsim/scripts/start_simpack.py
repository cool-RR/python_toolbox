#!/usr/bin/env python

from __future__ import with_statement

import os.path
import sys
import re
import shutil

import pkg_resources

import simpack_template
simpack_template_package_name = simpack_template.__name__


def _walk_folder(package_name, folder):
    '''pkg_resources'''
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
    dir = os.path.split(file)[0]
    if os.path.isdir(dir):
        return
    parent_dir = os.path.split(dir)[0]
    _make_path_to_file(dir)
    os.mkdir(dir)
    
                
    
def start_simpack(containing_folder, name):
    """
    
    """
    
    if not re.search(r'^[_a-zA-Z]\w*$', name): # If it's not a valid directory name.
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
        raise Exception("%r is not a valid simpack name. Please %s." % (name, app_or_project, message))
    folder = os.path.join(containing_folder, name)
    
    os.mkdir(folder)
    
    for file in _walk_folder(simpack_template_package_name, '.'):
        dest_file = '/'.join((containing_folder, f.replace('simpack_name', name)))
        
        _make_path_to_file(file)
        
        with pkg_resources.resource_stream(file) as source:
            with open(dest, 'w') as destination:
            
                destination.write(source.read().replace('simpack_name', name))
            
        try:
            shutil.copymode(path_old, path_new)
            _make_writeable(path_new)
        except OSError:
            pass
    

                
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
    '''tododoc'''
    print 'help! meow.'
    
if __name__ == '__main__':

    if len(sys.argv) != 2:
        show_help()
        sys.exit()
    arg = sys.argv[1]

    if arg == '--help':
        show_help()
        sys.exit()
    
    start_simpack(os.curdir, arg)
    
        