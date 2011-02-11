#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Script for running tests on all GarlicSim packages together.

Nose is used to run the tests, and any arguments will be passed to Nose; type
`nosetests --help` to see Nose's list of arguments.

GarlicSim-specific arguments:

    --from-zip            Test GarlicSim when import from zip files
    --from-py2exe         Test GarlicSim when imported from py2exe distribution
    --from-win-installer  Test GarlicSim when installed from Windows installer
    
'''

# blocktodo: --from-win-installer

import os.path
import sys
import imp
import types


frozen = getattr(sys, 'frozen', None)


if frozen:
    our_path = os.path.split(sys.executable)[0]
else: # not frozen
    our_path = os.path.realpath(os.path.split(__file__)[0])

    
### Defining import-related utilities: ########################################
#                                                                             #
def exists(module_name):
    '''
    Return whether a module by the name `module_name` exists.
    
    This seems to be the best way to carefully import a module.
    
    Currently implemented for top-level packages only. (i.e. no dots.)
    
    Doesn't support modules imported from a zip file.
    '''
    assert '.' not in module_name
    try:
        imp.find_module(module_name)
    except ImportError:
        return False
    else:
        return True

def import_by_path(path, name=None):
    '''Import module/package by path.'''
    short_name = os.path.splitext(os.path.split(path)[1])[0]
    if name is None: name = short_name
    path_to_dir = os.path.dirname(path)
    my_file = None
    try:
        (my_file, pathname, description) = \
            imp.find_module(short_name, [path_to_dir])
        module = imp.load_module(name, my_file, pathname, description)
    finally:
        if my_file is not None:
            my_file.close()
        
    return module
#                                                                             #
### Finished defining import-related utilities. ###############################
    

tweak_nose = import_by_path(
    os.path.join(our_path, 'misc', 'testing', 'tweak_nose')
)


package_names = ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']
if frozen:
    test_packages_paths = [os.path.join(our_path, 'lib/test_%s') % package_name
                           for package_name in package_names]
    
else: # not frozen
    test_packages_paths = \
        [os.path.join(our_path, ('%s/test_%s' % (package_name, package_name)))
         for package_name in package_names]

###############################################################################

if __name__ == '__main__':
    
    try:
        import multiprocessing
    except ImportError:
        pass
    else:
        multiprocessing.freeze_support()
    
    argv = sys.argv[:] if frozen else sys.argv[1:]
    
    if '--help' in argv:
        sys.stdout.write(__doc__ + '\n')
        exit()
    
    sys.stdout.write('Preparing to run tests using Python %s\n' % sys.version)    
    
    testing_from_zip = '--from-zip' in argv
    testing_from_py2exe = ('--from-py2exe' in argv) or frozen
    
    assert not (testing_from_zip and testing_from_py2exe)
    
    if testing_from_zip:
        argv.remove('--from-zip')
        zip_testing_utilities = import_by_path(
            os.path.join(our_path, 'misc', 'testing', 'zip', 'testing_utilities')
        )
        zip_testing_utilities.prepare_zip_testing(package_names)
        
    if testing_from_py2exe and not frozen:
        argv.remove('--from-py2exe')
        
        temp_result = \
            os.system(sys.executable + ' "%s"' % os.path.join(our_path,
                      'package_for_windows.py'))
        if temp_result != 0:
            sys.exit(temp_result)
            
        sys.exit(os.system('"%s" %s' % (os.path.join(our_path,
                           'py2exe_dist\\run_tests.exe'), ' '.join(argv))))
            
        
    # Adding test packages to arguments to have Nose take tests from them:
    argv += test_packages_paths[::-1]
    # (Reversing package order for now, to put the shorter tests first.)
    
    
    try:
        #######################################################################
        # This is the heavy line, which actually causes Nose to start running
        # tests:
        tweak_nose.TestProgram(argv=argv)
        #######################################################################
    
    finally:
        if testing_from_zip:
            zip_testing_utilities.ensure_zip_testing_was_legit(package_names)
        elif testing_from_py2exe:
            sys.stdout.write('Finished testing from py2exe distribution.\n')

