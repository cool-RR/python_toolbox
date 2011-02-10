# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''

'''

import sys

frozen = getattr(sys, 'frozen', None)

if frozen:
    if sys.version_info[:2] != (2, 6):
        raise NotImplementedError('For Python versions other than 2.6 need to '
                                  'bundle their respective `site.py` modules.')
    assert 'site' not in sys.modules
    from . import python26_site
    