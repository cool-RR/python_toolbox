#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Script for running tests on all GarlicSim packages together.

Nose is used to run the tests, and any arguments will be passed to Nose; type
`nosetests --help` to see Nose's list of arguments.

GarlicSim-specific arguments:

    --from-zip  Zip GarlicSim and import the modules from a zip file
    
'''

import os.path
import sys
import imp


frozen = getattr(sys, 'frozen', None)

if frozen:
    
else: # not frozen
    our_path = os.path.realpath(os.path.split(__file__)[0])
    if os.path.realpath(os.getcwd()) != our_path:
        raise Exception("This script may only be launched from its own "
                        "folder, i.e., when the folder that it's located in "
                        "is the working directory.")


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

    
try:
    import nose
except ImportError:
    import warnings
    warnings.warn('Is Nose installed? It must be for the GarlicSim tests to '
                  'run.')
    raise
    
    
class TestProgram(nose.core.TestProgram):
    '''
    Tester for GarlicSim.
    
    We subclass `nose.core.TestProgram` to make it collect test configurations
    from all the different packages in this repo, and use our own `Config`
    class.
    '''
    def makeConfig(self, env, plugins=None):
        '''
        Load a Config, pre-filled with user config files if any are found.
        
        We override `nose.core.TestProgram.makeConfig` to make it collect test
        configurations from all the different packages in this repo, and use
        our own `Config` class.
        '''
        cfg_files = ['garlicsim/setup.cfg',
                     'garlicsim_lib/setup.cfg',
                     'garlicsim_wx/setup.cfg']
        if plugins:
            manager = nose.core.PluginManager(plugins=plugins)
        else:
            manager = nose.core.DefaultPluginManager()
        return Config(
            env=env, files=cfg_files, plugins=manager)

    
class Config(nose.config.Config):
    '''Nose configuration.''' 
    def configureWhere(self, where):
        '''
        Configure the working directory or directories for the test run.
        
        We override `nose.config.Config.configureWhere` to avoid adding
        together the locations from all the `setup.cfg` files, because Nose
        doesn't handle that well. So we use this script's path, which doesn't
        have any tests on it, as the official 'where' directory, while we pass
        the real test folders as arguments to `TestProgram`, without any
        `--where` flag.
        '''
        return nose.config.Config.configureWhere(
            self,
            our_path
        )

    
def prepare_zip_testing():
    '''Zip all GarlicSim modules and import them for testing.'''
    
    sys.stdout.write('Preparing to zip GarlicSim packages, and then run tests '
                     'with GarlicSim imported from zip files.\n')
    
    result = os.system(
        '"%s"' % \
        os.path.realpath(
            os.path.join(our_path, 'misc', 'testing', 'zip', 'make_zip.py')
        )
    )
    
    if result != 0:
        exit(result)
        
    for package_name in package_names:
        assert not exists(package_name)
        assert package_name not in sys.modules

    sys.stdout.write('Importing all GarlicSim packages from zip files... ')
        
    for i, package_name in enumerate(package_names):
        zip_file = os.path.realpath(
            os.path.join(our_path, 'misc', 'testing', 'zip', 'build',
                         (str(i) + '.zip'))
        )
        assert zip_file not in sys.path
        sys.path.append(zip_file)
        package = __import__(package_name)
        assert '.zip' in package.__file__
    
    sys.stdout.write('Done.\n')
    
    
def ensure_zip_testing_was_legit():
    '''
    Ensure GarlicSim packages were indeed used from zip.
    
    This is used only in `--from-zip` testing, to ensure that the GarlicSim
    packages weren't used from the source folders accidentally.
    '''
    sys.stdout.write('Confirming all GarlicSim packages were used from zip '
                     'files... ')
    for i, package_name in enumerate(package_names):
        assert package_name in sys.modules
        package = sys.modules[package_name]
        assert '.zip' in package.__file__
        
        raw_module_names = \
            [module_name for module_name in sys.modules.keys() if
             module_name.split('.')[0] == package_name]
        
        # Filtering out module names that map to `None`, because of a bug,
        # probably in `zipimport`, which litters `sys.modules` with
        # non-sense modules:
        
        module_names = [module_name for module_name in raw_module_names if
                        sys.modules[module_name] is not None]
        
        module_paths = [sys.modules[module_name].__file__ for
                        module_name in module_names]
        
        zip_file_name = str(i) + '.zip'
        snippet_from_real_folder_path = \
            os.path.sep.join((package_name, package_name))
        for module_path in module_paths:
            assert zip_file_name in module_path
            assert snippet_from_real_folder_path not in module_path
    sys.stdout.write('Done.\n')

    
package_names = ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']



if __name__ == '__main__':
    
    argv = sys.argv[:]
    
    if '--help' in argv:
        sys.stdout.write(__doc__ + '\n')
        exit()
    
    sys.stdout.write('Preparing to run tests using Python %s\n' % sys.version)    
    
    testing_from_zip = '--from-zip' in argv
    if testing_from_zip:
        argv.remove('--from-zip')
        prepare_zip_testing()
        
    # Adding test packages to arguments to have Nose take tests from them:
    argv += ['%s/test_%s' % (package_name, package_name) for 
             package_name in package_names][::-1]
    # (Reversing package order for now, to put the shorter tests first.)
    
    
    try:
        #######################################################################
        # This is the heavy line, which actually causes Nose to start running
        # tests:
        TestProgram(argv=argv)
        #######################################################################
    
    finally:
        if testing_from_zip:
            ensure_zip_testing_was_legit()

