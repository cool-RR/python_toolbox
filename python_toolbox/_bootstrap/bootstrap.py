# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception("Python 3.x is not supported, only Python 2.6 and Python "
                    "2.7.")
if sys.version_info[1] <= 5:
    raise Exception(
        "You're using Python <= 2.5, but this package requires either Python "
        "2.6 or Python 2.7, so you can't use it unless you upgrade your "
        "Python version."
    )
#                                                                             #
### Finished confirming correct Python version. ###############################


#frozen = getattr(sys, 'frozen', None)
#is_pypy = ('__pypy__' in sys.builtin_module_names)
