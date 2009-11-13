# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import pkg_resources

'''
This module defines the require function and the DistributionNotFound error.

See their documentation for more information.
'''

__all__ = ['DistributionNotFound', 'require']

class DistributionNotFound(Exception):
    '''An error to raise when a distribution is not found.'''
    pass

def require(distribution_name, silent=False):
    '''
    Require that the distribution be installed on the user's system
    
    The distribution is given by its name, as a string. The optional `silent`
    flag will make the function not raise an error if the module is not found,
    but just return False.
    '''
    try:
        module_installed = bool(pkg_resources.require(distribution_name))
        assert module_installed
        return True
    except pkg_resources.DistributionNotFound:
        if silent:
            return False
        else:
            raise DistributionNotFound('''The '%s' module is required, but \
it's not currently installed on your system. Please find it online and \
install it, then try again.''' % distribution_name)
        
        
    
