# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This is a bootstrap module for garlicsim.

It checks all prerequisites are installed.
'''

def __check_prerequisites():
    '''
    Check that all modules required for garlicsim are installed.
    
    Returns a list of some imported modules: A reference to this list should be
    kept alive so to prevent the imported modules from being garbage-collected,
    which would cause Python to load them twice, which would needlessly increase
    startup time.
    '''
    
    modules = []
    
    class MissingModule(Exception):
        '''An error to raise when a required module is not found.'''
        pass
    
    def check_distribute():
        try:
            import pkg_resources
            modules.append(pkg_resources)
            assert pkg_resources.require('Distribute >= 0.6')
        except:
            raise MissingModule('''Distribute (version 0.6 and upwards) is \
required, but it's not currently installed on your system. Please find it \
online and install it, then try again.''')
        return [pkg_resources]
    
    modules += check_distribute()
    
    return modules

__modules_list = __check_prerequisites()