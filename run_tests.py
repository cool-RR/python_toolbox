# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''

'''

# blocktodo: make friendly error message if `nose` is missing
# blocktodo: make friendly error message if launched from wrong path

import os.path
import sys
import nose

our_path = os.path.realpath(os.path.split(__file__)[0])
test_suites = [
    os.path.realpath(
        os.path.join(our_path, package_name + '/test_' + package_name)
        ) for package_name in ['garlicsim', 'garlicsim_lib', 'garlicsim_wx']
]

class TestProgram(nose.core.TestProgram):    
    def makeConfig(self, env, plugins=None):
        """Load a Config, pre-filled with user config files if any are
        found.
        """
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
    ''' '''
        
    #def configureWhere(self, where):
        #"""Configure the working directory or directories for the test run.
        #"""
        #return nose.config.Config.configureWhere(
            #self,
            #test_suites
        #)

    
if __name__ == '__main__':
    
    argv = sys.argv[:]
    #argv.append('--where=garlicsim/test_garlicsim,'
                        #'garlicsim_lib/test_garlicsim_lib,'
                        #'garlicsim_wx/test_garlicsim_wx')
    argv += ['"garlicsim/test_garlicsim"',
             '"garlicsim_lib/test_garlicsim_lib"',
             '"garlicsim_wx/test_garlicsim_wx"'][::-1]
    TestProgram(argv=argv)