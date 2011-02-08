#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''

'''

# blocktodo: make friendly error message if `nose` is missing
# blocktodo: make friendly error message if launched from wrong path

import os.path
import sys
import imp

import nose


our_path = os.path.realpath(os.path.split(__file__)[0])

if os.path.realpath(os.getcwd()) != our_path:
    raise Exception("This script may only be launched from its own folder, "
                    "i.e., when the folder that it's located in is the "
                    "working directory.")


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
        

class TestProgram(nose.core.TestProgram):
    '''
    Tester for GarlicSim.
    
    We subclass `nose.core.TestProgram` to make it collect test configurations
    from all the different packages in this repo.
    '''
    def makeConfig(self, env, plugins=None):
        '''
        Load a Config, pre-filled with user config files if any are found.
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
    '''
    Nose configuration.
    '''
        
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

    
if __name__ == '__main__':
    
    argv = sys.argv[:]
    
    package_names = ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']
    
    testing_from_zip = '--from-zip' in argv
    if testing_from_zip:
        argv.remove('--from-zip')
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
        
        for package_name in package_names:
            zip_file = os.path.realpath(
                os.path.join(our_path, 'misc', 'testing', 'zip', 'build',
                             (package_name + '.zip'))
            )
            assert zip_file not in sys.path
            sys.path.append(zip_file)
            package = __import__(package_name)
            assert '.zip' in package.__file__
            
        
    argv += ['garlicsim/test_garlicsim',
             'garlicsim_lib/test_garlicsim_lib',
             'garlicsim_wx/test_garlicsim_wx'][::-1]
    TestProgram(argv=argv)
    
    if testing_from_zip:
        for package_name in package_names:
            assert package_name in sys.modules
            package = sys.modules[package_name]
            assert '.zip' in package.__file__