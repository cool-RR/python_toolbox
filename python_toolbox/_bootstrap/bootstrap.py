# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] == 2:
    raise Exception("This is a Python 3.x distribution of `python_toolbox`, "
                    "and you're using Python 2.x. Please get the Python 2.x "
                    "distribution.")
#                                                                             #
### Finished confirming correct Python version. ###############################
