#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Script for running tests on all GarlicSim packages together.

Nose is used to run the tests, and any extraneous arguments will be passed to
Nose; type `nosetests --help` to see Nose's list of arguments.

## GarlicSim-specific arguments: ##

    --help
        Show this help screen

        
  #### Load GarlicSim from: ####
  
    --from-zip
        Test GarlicSim when imported from zip files
    
    --from-py2exe
        Test GarlicSim when imported from py2exe distribution
      
    --from-win-installer
        Test GarlicSim when installed from Windows installer.    
        Currently not fully implemented; only creates a Windows installer for
        you as `GarlicSim-x.y.z.exe`, you have to run it yourself and then run
        `run_tests.exe` in the installation folder.
      
        
  #### Choosing tests: ####
  
    --test-only=PATH  
        Load tests from specified file/folder instead of loading GarlicSim's
        test suite. Useful for picking just a few tests. Note that you can only
        put a single path in one of these, so if you want to use multiple
        locations, you'll have to put multiple `--test-only=` segments.

'''

import os.path
import sys
import imp
import types
import glob


frozen = getattr(sys, 'frozen', None)
is_pypy = ('__pypy__' in sys.builtin_module_names)


if frozen:
    our_path = os.path.realpath(os.path.split(sys.executable)[0])
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
    
### Tweaking nose: ############################################################
#                                                                             #
try:
    import nose
except ImportError:
    import warnings
    warnings.warn('Is Nose installed? It must be for the GarlicSim tests to '
                  'run.')
    raise

if nose.__versioninfo__ < (1, 0, 0):
    raise Exception('Nose version 1.0.0 or higher is required to run tests.')
    
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
            cfg_files = [
                os.path.join(our_path, 'garlicsim', 'setup.cfg'),
                os.path.join(our_path, 'garlicsim_lib', 'setup.cfg'),
                os.path.join(our_path, 'garlicsim_wx', 'setup.cfg')
            ]
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
    
    ### Taking sourceless binary Python files: ################################
    #                                                                         #
    is_binary_python_module = (ext in ['.pyc', '.pyo'])

    if is_binary_python_module:
        corresponding_python_source_file = (os.path.splitext(file)[0] + '.py')
        has_corresponding_source_file = \
            os.path.exists(corresponding_python_source_file)
    
    wanted = self.matches(base) and (pysrc or 
         (is_binary_python_module and not has_corresponding_source_file))
    #                                                                         #
    ### Finished taking sourceless binary Python files. #######################
    
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
                ### Identifying Python files: #################################
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
### Finished tweaking Nose. ###################################################


package_names = ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']
if frozen:
    test_packages_paths = [os.path.join(our_path, 'lib', 'test_%s' %
                           package_name) for package_name in package_names]
    
else: # not frozen
    test_packages_paths = \
        [os.path.join(our_path, package_name, 'test_%s' % package_name)
         for package_name in package_names]

###############################################################################

if __name__ == '__main__':
    
    try:
        import multiprocessing
    except ImportError:
        pass
    else:
        multiprocessing.freeze_support()
    
    argv = sys.argv[:]
    
    if '--help' in argv:
        sys.stdout.write(__doc__ + '\n')
        exit()
    
    sys.stdout.write('Preparing to run tests using Python %s\n' % \
                     sys.version)    
    
    testing_from_zip = '--from-zip' in argv
    testing_from_py2exe = ('--from-py2exe' in argv) or \
        ((frozen is not None) and ('win_dist' in our_path))
    testing_from_win_installer = bool(
        ('--from-win-installer' in argv) or
        ((frozen is not None) and glob.glob(os.path.join(our_path, 'unins*')))
    )
    
    if testing_from_zip + testing_from_py2exe + testing_from_win_installer > 1:
        raise Exception("Can test either from repo, or from zip, or from "
                        "py2exe, or from Windows installer. Can't have more "
                        "than one.")
    
    ### Handling manually-specified test locations: ###########################
    #                                                                         #
    manually_specified_test_locations = []
    manually_specified_test_location_arguments = \
        [argument for argument in argv if argument.startswith('--test-only=')]
    if manually_specified_test_location_arguments:
        if testing_from_py2exe or testing_from_win_installer:
            raise NotImplementedError
        for argument in manually_specified_test_location_arguments:
            argv.remove(argument)
            location = argument[12:]
            assert os.path.exists(location)
            manually_specified_test_locations.append(location)
    #                                                                         #
    ### Finished handling manually-specified test locations. ##################
        
    if testing_from_py2exe:
        
        if os.name != 'nt':
            raise Exception("Can't run tests from `py2exe` on a non-Windows "
                            "platform.")
        
        sys.stdout.write('Running tests from `py2exe` distribution.\n')
    
        if not frozen:
            
            argv.remove('--from-py2exe')
            
            temp_result = os.system(
                '""%s" "%s""' % (
                    sys.executable,
                    os.path.join(
                        our_path,
                        'make_distribution.py'
                    )
                )
            )
            
            if temp_result != 0:
                sys.exit(temp_result)
                
            sys.exit(
                os.system('"%s" %s' % (os.path.join(our_path,
                          'win_dist', 'run_tests.exe'), ' '.join(argv[1:])))
            )

            
    if testing_from_win_installer:
        
        if os.name != 'nt':
            raise Exception("Can't run tests from Windows installation on "
                            "a non-Windows platform.")
        
        if '--from-win-installer' in argv:            
            argv.remove('--from-win-installer')
        
        sys.stdout.write('Running tests from Windows Inno Setup '
                         'installation.\n')

        if not frozen:
            
            temp_result = os.system(
                    '""%s" "%s" --installer"' % (
                        sys.executable,
                        os.path.join(
                            our_path,
                            'make_distribution.py'
                        )
                    )
                )
            
            if temp_result != 0:
                sys.exit(temp_result)
                
            sys.stdout.write(
                'Now please manually run the `GarlicSim-x.y.z.exe` '
                'installer and then run `run_tests.exe` in the '
                'installation folder. Sorry about that.\n'
            )
            sys.exit(0)
    
    if testing_from_zip:
        argv.remove('--from-zip')
        zip_testing_utilities = import_by_path(
            os.path.join(our_path, 'misc', 'testing', 'zip',
                         'testing_utilities')
        )
        zip_testing_utilities.prepare_zip_testing(package_names)
        
    if not (testing_from_zip or testing_from_py2exe or
            testing_from_win_installer):
        
        sys.stdout.write('Running tests directly from GarlicSim repo.\n')
        
    ## Adding test packages to arguments to have Nose take tests from them: ###
    #                                                                         #
    if manually_specified_test_locations:
        argv += manually_specified_test_locations
        
    else: # not manually_specified_test_locations
        
        # (Reversing package order for now, to put the shorter tests first.)
        if is_pypy:
            sys.stdout.write("Pypy doesn't have wxPython, not loading "
                             "`garlicsim_wx` tests.\n")
            argv += test_packages_paths[-2::-1]
        else: # not is_pypy
            argv += test_packages_paths[::-1]
    #                                                                         #
    ###########################################################################
    
    try:
        #######################################################################
        # This is the heavy line, which actually causes Nose to start running
        # tests:
        TestProgram(argv=argv)
        #######################################################################
    
    finally:
        if testing_from_zip:
            zip_testing_utilities.ensure_zip_testing_was_legit(package_names)
        elif testing_from_py2exe:
            sys.stdout.write('Finished testing from `py2exe` distribution.\n')
        elif testing_from_win_installer:
            sys.stdout.write('Finished testing from Windows installation.\n')
        else:
            sys.stdout.write('Finished testing from repo.\n')

