# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackPlace` class.

See its documentation for more information.
'''

import garlicsim.general_misc.third_party.namedtuple

from garlicsim.general_misc import module_tasting
from garlicsim.general_misc import caching


_SimpackPlaceBase = garlicsim.general_misc.\
                       third_party.namedtuple.namedtuple(
                           '_SimpackPlaceBase',
                           'path package_prefix name',
                       )


class SimpackPlace(_SimpackPlaceBase):
    

    __metaclass__ = caching.CachedType
    
    
    def __init__(self, path, package_prefix='', name=None):
        
        ### Determining name: #################################################
        #                                                                     #
        if name is None:
            if package_prefix:
                parent_package = address_tools.resolve(package_prefix[:-1])
                if hasattr(parent_package, 'simpack_place_name'):
                    name = getattr(parent_package, 'simpack_place_name')
            else:
                name = os.path.split(path)[-1]
        #                                                                     #
        ### Finished determining name. ########################################
        
        _SimpackPlaceBase.__init__(self,
                                   path=path,
                                   package_prefix=package_prefix,
                                   name=name)
                
        assert isinstance(self.path, basestring)
        assert isinstance(self.package_prefix, basestring)
        assert isinstance(self.name, basestring)
        
        if False: # This section gives us better source assistance in Wing IDE:
            self.path = self.path
            self.package_prefix = self.package_prefix
            self.name = self.name
        
    

