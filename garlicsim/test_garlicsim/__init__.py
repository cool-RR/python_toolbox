# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `garlicsim`.'''

from .shared import verify_sample_simpack_settings

def __bootstrap():
    import os
    import sys
    from garlicsim.general_misc import import_tools    
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