# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `garlicsim_wx`.'''


def __bootstrap():
    '''
    Add needed packages in repo to path if we can't find them.
    
    This adds `garlicsim`'s, `garlicsim_lib`'s and `garlicsim_wx`'s root
    folders to `sys.path` if they can't currently be imported.
    '''
    import os
    import sys
    import imp

    def exists(module_name):
        '''
        Return whether a module by the name `module_name` exists.
        
        This seems to be the best way to carefully import a module.
        
        Currently implemented for top-level packages only. (i.e. no dots.)
        '''
        assert '.' not in module_name
        try:
            imp.find_module(module_name)
        except ImportError:
            return False
        else:
            return True
    
    if not exists('garlicsim'):
        garlicsim_candidate_path = os.path.realpath(
            os.path.join(
                os.path.split(__file__)[0],
                '..',
                '..',
                'garlicsim'
            )
        )
        sys.path.append(garlicsim_candidate_path)
    if not exists('garlicsim_lib'):
        garlicsim_lib_candidate_path = os.path.realpath(
            os.path.join(
                os.path.split(__file__)[0],
                '..',
                '..',
                'garlicsim_lib'
            )
        )
        sys.path.append(garlicsim_lib_candidate_path)
    if not exists('garlicsim_wx'):
        garlicsim_wx_candidate_path = os.path.realpath(
            os.path.join(
                os.path.split(__file__)[0],
                '..',
                '..',
                'garlicsim_wx'
            )
        )
        sys.path.append(garlicsim_wx_candidate_path)
        
        
__bootstrap()