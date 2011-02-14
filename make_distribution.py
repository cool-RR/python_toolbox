#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Script for packaging GarlicSim as a complete program to end users.

Currently implemented only for Windows.

Options:

    General:

    	--help
    	    Show this help screen

    Different operating systems:
    
        --win [OR] -w
            Create a Windows distribution.
    
        --mac [OR] -m
            Create a Mac distribution. Not implemented yet.
    
        --deb [OR] -d
            Create a Debian Linux distribution. Not implemented yet.
    
            
        --installer [OR] -i
            After running py2exe, produce an installer using Inno Setup
            
    Windows-only options:        
            
        --issc=[PATH]            
            Path to `issc.exe`, needed only if (a) making a Windows installer
            and (b) `issc.exe` is in a non-standard location)
        
'''

import shutil
import os.path
import sys
import glob


repo_root_path = os.path.realpath(os.path.split(__file__)[0])
garlicsim_wx_path = os.path.join(repo_root_path, 'garlicsim_wx')
assert __name__ == '__main__'


if '--help' in sys.argv:
    sys.stdout.write(__doc__ + '\n')
    exit()

if os.name != 'nt':
    raise Exception('Py2exe may only be used on Windows.')

produce_installer = ('--installer' in sys.argv) or ('-i' in sys.argv)

if produce_installer:
    sys.stdout.write('Preparing to package GarlicSim with py2exe and produce '
                     'Windows installer.\n')
else: # not produce_installer
    sys.stdout.write('Preparing to package GarlicSim with py2exe.\n')

if produce_installer:
    ### Figuring out location of inno setup compiler: #########################
    #                                                                         #
    issc_specifiers = [arg for arg in sys.argv if arg.startswith('--issc=')]
    if issc_specifiers:
        (issc_specifier,) = issc_specifiers
        path_to_issc = issc_specifier[7:]
        if path_to_issc[0] == path_to_issc[-1] == '"':
            path_to_issc = path_to_issc[1:-1]
        if not os.path.isfile(path_to_issc):
            raise Exception('The path to `ISSC.exe` that you specified does '
                            'not exist. Make sure to include the `.exe` file '
                            'itself in the path.')
    else:
        path_to_issc = \
            'c:\\Program Files\\Inno Setup 5\\ISCC.exe'
        if not os.path.isfile(path_to_issc):
            raise Exception("The Inno Setup compiler `ISSC.exe` could not be "
                            "found. If you don't have Inno Setup installed, "
                            "install it. If it's installed and you still get "
                            "this message, specify the path to `ISSC.exe` by "
                            "using the `--issc=[PATH]` flag.")
        
    #                                                                         #
    ### Finished figuring out location of Inno Setup compiler. ################
    

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
               os.path.join(repo_root_path, 'win_dist')]:
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
            sys.stdout.write('Removing old `%s` file... ' % existing_installer)
            os.remove(existing_installer)
            sys.stdout.write('Done.')

sys.stdout.write('Working area clean.\n')
#                                                                             #
### Finished deleting old build files. ########################################



### Packaging with py2exe: ####################################################
#                                                                             #
sys.stdout.write('Launching py2exe.\n')

old_cwd = os.getcwd()
os.chdir(garlicsim_wx_path)
try:
    temp_result = os.system('"%s" setup.py py2exe' % sys.executable)
    if temp_result != 0:
        sys.exit(temp_result)
finally:
    os.chdir(old_cwd)

sys.stdout.write('Py2exe packaging complete. Distribution files are in the '
                 '`win_dist` folder.\n')
#                                                                             #
### Finished packaging with py2exe. ###########################################
    
### Creating windows installer with inno setup: ###############################
#                                                                             #
if produce_installer:
    
    sys.stdout.write('Preparing to create Windows installer using Inno '
                     'Setup.\n')
    
    os.chdir(garlicsim_wx_path)
    try:
        # (There are no less than six quotes in this command, because of weird
        # `cmd.exe /C` conventions.)
        create_installer_command = '""%s" "%s""' % (
            path_to_issc,
            os.path.join(garlicsim_wx_path, 'installer_script.iss')
        )
        sys.exit(os.system(create_installer_command))
    finally:
        os.chdir(old_cwd)
#                                                                             #
### Finished creating Windows installer with Inno Setup. ######################
