# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `garlicsim_lib`.'''


def __bootstrap():
    '''
    Add needed packages in repo to path if we can't find them.
    
    This adds `garlicsim`'s, `garlicsim_lib`'s and `garlicsim_wx`'s root
    folders to `sys.path` if they can't currently be imported.
    '''
    import os
    import sys
    from garlicsim.general_misc import import_tools    
    if not import_tools.exists('garlicsim'):
        garlicsim_candidate_path = os.path.realpath(
            os.path.join(
                os.path.split(__file__)[0],
                '..',
                '..',
                'garlicsim'
            )
        )
        sys.path.append(garlicsim_candidate_path)
    if not import_tools.exists('garlicsim_lib'):
        garlicsim_lib_candidate_path = os.path.realpath(
            os.path.join(
                os.path.split(__file__)[0],
                '..',
                '..',
                'garlicsim_lib'
            )
        )
        sys.path.append(garlicsim_lib_candidate_path)
    if not import_tools.exists('garlicsim_wx'):
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