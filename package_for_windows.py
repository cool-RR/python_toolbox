#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `` class.

See its documentation for more information.
tododoc
'''

import shutil
import os.path
import sys
import glob

if os.name != 'nt':
    raise Exception('Py2exe may only be used on Windows.')

produce_installer = ('--installer' in sys.argv) or ('-i' in sys.argv)

if produce_installer:
    sys.stdout('Preparing to package GarlicSim with py2exe and produce '
               'Windows installer.\n')
else: # not produce_installer
    sys.stdout('Preparing to package GarlicSim with py2exe.\n')

repo_root_path = os.path.realpath(os.path.split(__file__)[0])
garlicsim_wx_path = os.path.join(repo_root_path, 'garlicsim_wx')
assert __name__ == '__main__'

### Deleting old build files: #################################################
#                                                                             #
def assert_no_unknown_folders():
    existing_folders = set(
        [name for name in os.listdir(garlicsim_wx_path) if
         os.path.isdir(os.path.join(garlicsim_wx_path, name))]
    )
    assert existing_folders == \
           set(('garlicsim_wx', 'test_garlicsim_wx', 'py2exe_cruft'))

folders_to_delete = []
for folder in [os.path.join(garlicsim_wx_path, 'build'),
               os.path.join(garlicsim_wx_path, 'garlicsim_wx.egg-info'),
               os.path.join(repo_root_path, 'py2exe_dist')]:
    if os.path.exists(folder):
        folders_to_delete.append(folder)

if folders_to_delete:
    sys.stdout.write('Preparing to delete old build folders.\n')
    for folder_to_delete in folders_to_delete:
        short_name = os.path.split(folder_to_delete)[1]
        sys.stdout.write("Deleting the '%s' folder... " % short_name)
        shutil.rmtree(folder_to_delete)
        sys.stdout.write('Done.\n')
    assert_no_unknown_folders()
else: # No folders to delete
    assert_no_unknown_folders()
    sys.stdout.write('No previous build folders to delete.\n')


if produce_installer:
    existing_installers = \
        glob.glob(os.path.join(repo_root_path, 'GarlicSim-*.exe'))
    if existing_installers:
        sys.stdout.write('Preparing to remove old installer file%s.\n' % \
                         ('s' if (len(existing_installers) > 1) else ''))
        for existing_installer in existing_installers:
            sys.stdout('Removing old `%s` file... ' % existing_installer)
            os.remove(existing_installer)
            sys.stdout('Done.')

sys.stdout.write('Working area clean.\n')
#                                                                             #
### Finished deleting old build files. ########################################



### Packaging with py2exe: ####################################################
#                                                                             #
sys.stdout.write('Launching py2exe.\n')

old_cwd = os.getcwd()
os.chdir(garlicsim_wx_path)
try:
    temp_result = os.system(sys.executable + ' setup.py py2exe'))
else:
    if temp_result != 0:
        sys.exit(temp_result)
finally:
    os.chdir(old_cwd)

sys.stdout('Py2exe packaging complete. Distribution in the `py2exe_dist` '
           'folder.')
#                                                                             #
### Finished packaging with py2exe. ###########################################
    
os.chdir(repo_root_path)
try:
    temp_result = os.system(
        os.path.join(repo_root_path, ' installer_script.iss')
    )
else:
    if temp_result != 0:
        sys.exit(temp_result)
finally:
    os.chdir(old_cwd)