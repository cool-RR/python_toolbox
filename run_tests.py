#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Script for running tests on all GarlicSim packages together.

Nose is used to run the tests, and any arguments will be passed to Nose; type
`nosetests --help` to see Nose's list of arguments.

GarlicSim-specific arguments:

    --from-zip     Zip GarlicSim and import the modules from a zip file
    --from-py2exe  Package GarlicSim with py2exe and test from there
    
'''

import os.path
import sys
import imp
import types


frozen = getattr(sys, 'frozen', None)

if frozen:
    our_path = os.path.split(sys.executable)[0]
else: # not frozen
    our_path = os.path.realpath(os.path.split(__file__)[0])
    
#if os.path.realpath(os.getcwd()) != our_path:
    #raise Exception("This script may only be launched from its own "
                    #"folder, i.e., when the folder that it's located in "
                    #"is the working directory.")


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

### Tweaking nose code: #######################################################
#                                                                             #
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
        if frozen:
            cfg_files = [os.path.join(our_path, 'setup.cfg')]
        else: # not frozen
            cfg_files = [os.path.join(our_path, 'garlicsim/setup.cfg'),
                         os.path.join(our_path, 'garlicsim_lib/setup.cfg'),
                         os.path.join(our_path, 'garlicsim_wx/setup.cfg')]
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


def wantFile(self, file):
    '''
    Is the file a wanted test file?
    
    We are overriding `nose.selector.Selector.wantFile` by monkeypatching it;
    the original implementation doesn't take tests from `.pyc` and `.pyo`
    files, which is problematic for us because when packaging with `py2exe`, we
    get only `.pyc` files in the distribution. So here we override it to take
    `.pyc` and `.pyo` files, but only if they don't have a source module
    associated with them, so we won't run the same test twice.
    '''
    log = nose.selector.log
    # never, ever load files that match anything in ignore
    # (.* _* and *setup*.py by default)
    base = nose.selector.op_basename(file)
    ignore_matches = [ ignore_this for ignore_this in self.ignoreFiles
                       if ignore_this.search(base) ]
    if ignore_matches:
        log.debug('%s matches ignoreFiles pattern; skipped',
                  base) 
        return False
    if not self.config.includeExe and os.access(file, os.X_OK):
        log.info('%s is executable; skipped', file)
        return False
    dummy, ext = nose.selector.op_splitext(base)
    pysrc = ext == '.py'
    
    ### Taking sourceless binary python files: ################################
    #                                                                         #
    is_binary_python_module = (ext in ['.pyc', '.pyo'])

    if is_binary_python_module:
        corresponding_python_source_file = (os.path.splitext(file)[0] + '.py')
        has_corresponding_source_file = \
            os.path.exists(corresponding_python_source_file)
    
    wanted = self.matches(base) and (pysrc or 
         (is_binary_python_module and not has_corresponding_source_file))
    #                                                                         #
    ### Finished taking sourceless binary python files. #######################
    
    plug_wants = self.plugins.wantFile(file)
    if plug_wants is not None:
        log.debug("plugin setting want %s to %s", file, plug_wants)
        wanted = plug_wants
    log.debug("wantFile %s? %s", file, wanted)
    return wanted    
nose.selector.Selector.wantFile = \
    types.MethodType(wantFile, None, nose.selector.Selector)


def loadTestsFromDir(self, path):
    """Load tests from the directory at path. This is a generator
    -- each suite of tests from a module or other file is yielded
    and is expected to be executed before the next file is
    examined.
    """
    from nose.loader import (log, add_path, op_abspath, op_isfile, op_isdir,
                             Failure, remove_path, sort_list, regex_last_key,
                             op_join, ispackage)
    
    log.debug("load from dir %s", path)
    plugins = self.config.plugins
    plugins.beforeDirectory(path)
    if self.config.addPaths:
        paths_added = add_path(path, self.config)

    entries = os.listdir(path)
    sort_list(entries, regex_last_key(self.config.testMatch))
    for entry in entries:
        # this hard-coded initial-dot test will be removed:
        # http://code.google.com/p/python-nose/issues/detail?id=82
        if entry.startswith('.'):
            continue
        entry_path = op_abspath(op_join(path, entry))
        is_file = op_isfile(entry_path)
        wanted = False
        if is_file:
            is_dir = False
            wanted = self.selector.wantFile(entry_path)
        else:
            is_dir = op_isdir(entry_path)
            if is_dir:
                # this hard-coded initial-underscore test will be removed:
                # http://code.google.com/p/python-nose/issues/detail?id=82
                if entry.startswith('_'):
                    continue
                wanted = self.selector.wantDirectory(entry_path)
        is_package = ispackage(entry_path)
        if wanted:
            if is_file:
                plugins.beforeContext()
                ### Identifying python files: #################################
                #                                                             #
                if '.py' in entry[-4:]:
                    yield self.loadTestsFromName(
                        entry_path, discovered=True)
                else:
                    yield self.loadTestsFromFile(entry_path)
                #                                                             #
                ### Finished identifying Python files. ########################
                plugins.afterContext()
            elif is_package:
                # Load the entry as a package: given the full path,
                # loadTestsFromName() will figure it out
                yield self.loadTestsFromName(
                    entry_path, discovered=True)
            else:
                # Another test dir in this one: recurse lazily
                yield self.suiteClass(
                    lambda: self.loadTestsFromDir(entry_path))
    tests = []
    for test in plugins.loadTestsFromDir(path):
        tests.append(test)
    # TODO: is this try/except needed?
    try:
        if tests:
            yield self.suiteClass(tests)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        yield self.suiteClass([Failure(*sys.exc_info())])
    
    # pop paths
    if self.config.addPaths:
        for p in paths_added:
          remove_path(p)
    plugins.afterDirectory(path)
nose.loader.TestLoader.loadTestsFromDir = \
    types.MethodType(loadTestsFromDir, None, nose.loader.TestLoader)
#                                                                             #
### Finished tweaking Nose code. ##############################################

    
### Defining functions for testing from zip archives: #########################
#                                                                             #
def prepare_zip_testing():
    '''Zip all GarlicSim modules and import them for testing.'''
    
    sys.stdout.write('Preparing to zip GarlicSim packages, and then run tests '
                     'with GarlicSim imported from zip files.\n')
    
    assert not frozen
    
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
#                                                                             #
### Finished defining functions for testing from zip archives. ################

    
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
    
    if exists('multiprocessing'):
        import multiprocessing
        multiprocessing.freeze_support()
    
    argv = sys.argv[:]
    
    if '--help' in argv:
        sys.stdout.write(__doc__ + '\n')
        exit()
    
    sys.stdout.write('Preparing to run tests using Python %s\n' % sys.version)    
    
    testing_from_zip = '--from-zip' in argv
    testing_from_py2exe = ('--from-py2exe' in argv) or frozen
    
    assert not (testing_from_zip and testing_from_py2exe)
    
    if testing_from_zip:
        argv.remove('--from-zip')
        prepare_zip_testing()
        
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
        TestProgram(argv=argv)
        #######################################################################
    
    finally:
        if testing_from_zip:
            ensure_zip_testing_was_legit()
        elif testing_from_py2exe:
            sys.stdout.write('Finished testing from py2exe distribution.\n')

