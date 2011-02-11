# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import os.path
import sys

our_path = os.path.realpath(os.path.split(__file__)[0])
repo_root_path = os.path.realpath(os.path.join(our_path, '..', '..'))

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
            cfg_files = [os.path.join(repo_root_path, 'setup.cfg')]
        else: # not frozen
            cfg_files = [
                os.path.join(repo_root_path, 'garlicsim/setup.cfg'),
                os.path.join(repo_root_path, 'garlicsim_lib/setup.cfg'),
                os.path.join(repo_root_path, 'garlicsim_wx/setup.cfg')
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
            repo_root_path
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
