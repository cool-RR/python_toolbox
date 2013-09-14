# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception("This is a Python 2.x distribution of `python_toolbox`, "
                    "and you're using Python 3.x. Please get the Python 3.x "
                    "distribution.")
if sys.version_info[1] <= 6:
    raise Exception(
        "You're using Python <= 2.6, but this package requires Python 2.7, "
        "(or Python 3.3+ on a different distribution,) so you can't use it "
        "unless you upgrade your Python version."
    )
#                                                                             #
### Finished confirming correct Python version. ###############################

