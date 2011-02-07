#!/usr/bin/env python
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
'''

from __future__ import with_statement

import os.path
import zipfile
import contextlib
import shutil

def zipdir(basedir, archivename, ignored_extenstions=[]):
    # blocktodo: make pretty
    assert os.path.isdir(basedir)
    
    ### Ensuring ignored extensions start with '.': ###########################
    #                                                                         #
    for ignored_extenstion in ignored_extenstions:
        if not ignored_extenstion.startswith('.'):
            ignored_extenstions[
                ignored_extenstions.index(ignored_extenstion)
                ] = \
            ('.' + ignored_extenstion)
    #                                                                         #
    ### Finished ensuring ignored extensions start with '.'. ##################
            
    with contextlib.closing(
        zipfile.ZipFile(archivename, 'w', zipfile.ZIP_DEFLATED)
        ) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                extension = os.path.splitext(fn)[1]
                if extension in ignored_extenstions:
                    continue
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)

                
# todo: define function for zipping a folder, then use it to make garlicsim,
# garlicsim_lib and garlicsim_wx in build folder

###############################################################################
#                                                                             #
# tododoc: helpful error messages:
assert __name__ == '__main__'
module_path = os.path.split(__file__)[0]
assert module_path.endswith(os.path.sep.join('misc', 'testing', 'zip'))
repo_root_path = os.path.realpath(os.path.join(module_path, '../../..'))
assert os.path.realpath(os.getcwd()) == repo_root_path
assert module_path == \
    os.path.realpath(os.path.join(repo_root_path, 'misc', 'testing', 'zip'))
#                                                                             #
###############################################################################
       
### Preparing build folder: ###################################################
#                                                                             #
build_folder = os.path.join(module_path, 'build')
if os.path.exists(build_folder):
    shutil.rmtree(build_folder)
os.mkdir(build_folder)
#                                                                             #
### Finished preparing build folder. ##########################################

### Zipping packages into zip files: ##########################################
#                                                                             #
package_names = ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']

for package_name in package_names:
    package_path = os.path.join(repo_root_path, package_name, package_name)
    assert os.path.isdir(package_path)
    zip_destination_path = os.path.join(build_folder,
                                        (package_name + '.zip'))    
    zipdir(package_path, zip_destination_path,
           ignored_extenstions=['.pyc', '.pyo'])
#                                                                             #
### Finished zipping packages into zip files. #################################

