#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Zip all the GarlicSim packages into zip archives in the `build` folder.

This is used for testing that GarlicSim works properly when running from zip
archive.

Note: The only reason we create zip files with numbers (e.g. '1.zip') instead
of names (e.g. 'garlicsim_lib.zip') is for Windows XP compatibility; Windows XP
limits the length of a path that a file may have, so we can't afford to have a
15-letter long zip name, and then under that serve the GarlicSim packages,
because it will cause Python to raise an `ImportError` under Windows XP.
'''

# blocktodo: should work with python 3, try it

from __future__ import with_statement

import sys
import re
import fnmatch
import os.path
import zipfile
import contextlib
import shutil


def zip_folder(folder, zip_path, ignored_patterns=[]):
    '''

    note: creates a folder inside the zip with the same name of the original
    folder, in contrast to other implementation which put all of the files on
    the root level of the zip.
    
    Doesn't put empty folders in the zip file.
    
    tododoc ignored_patterns, they're fnmatch style
    '''
    assert os.path.isdir(folder)
    source_folder = os.path.realpath(folder)
    
    ignored_re_patterns = [re.compile(fnmatch.translate(ignored_pattern)) for
                           ignored_pattern in ignored_patterns]
    
    zip_name = os.path.splitext(os.path.split(zip_path)[1])[0]
    source_folder_name = os.path.split(source_folder)[1]
            
    with contextlib.closing(
        zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        ) as zip_file:
        
        for root, subfolders, files in os.walk(source_folder):
            
            for file_path in files:
                
                if any(ignored_re_pattern.match(file_path) for
                       ignored_re_pattern in ignored_re_patterns):
                    continue
                
                absolute_file_path = os.path.join(root, file_path)
                
                destination_file_path = os.path.join(
                    source_folder_name,
                    absolute_file_path[(len(source_folder) + len(os.sep)):]
                )
                
                zip_file.write(absolute_file_path, destination_file_path)

                
    
def make_zip():
    ###########################################################################
    #                                                                         #
    module_path = os.path.realpath(os.path.split(__file__)[0])
    assert module_path.endswith(os.path.sep.join(('misc', 'testing', 'zip')))
    repo_root_path = os.path.realpath(os.path.join(module_path, '../../..'))
    assert module_path == os.path.realpath(
        os.path.join(repo_root_path, 'misc', 'testing', 'zip')
    )
    #                                                                         #
    ###########################################################################
           
    ### Preparing build folder: ###############################################
    #                                                                         #
    build_folder = os.path.join(module_path, 'build')
    if os.path.exists(build_folder):
        sys.stdout.write('Deleting old `build` folder... ')
        shutil.rmtree(build_folder)
        sys.stdout.write('Done.\n')
    sys.stdout.write('Creating `build` folder... ')
    os.mkdir(build_folder)
    sys.stdout.write('Done.\n')
    #                                                                         #
    ### Finished preparing build folder. ######################################
    
    ### Zipping packages into zip files: ######################################
    #                                                                         #
    package_names = ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']
    
    for i, package_name in enumerate(package_names):
        
        sys.stdout.write("Preparing to zip folder '%s'... " % package_name)
        package_path = os.path.join(repo_root_path, package_name, package_name)
        assert os.path.isdir(package_path)
        zip_destination_path = os.path.join(build_folder,
                                            (str(i) + '.zip'))
        
        sys.stdout.write('Zipping... ')
        zip_folder(package_path, zip_destination_path,
                   ignored_patterns=['*.pyc', '*.pyo', '*__pycache__*'])
        
        sys.stdout.write('Done.\n')
    #                                                                         #
    ### Finished zipping packages into zip files. #############################
    
    sys.stdout.write('Finished zipping all folders.\n')
    
    # todo: can make some test here that checks that the files were zipped
    # properly, have a correct data, and no pyo or pyc files were copied.

if __name__ == '__main__':
    make_zip()