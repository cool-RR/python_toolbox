# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This package defines the `ProcessCruncher` class.

See its documentation for more information.

In order to actually use `ProcessCruncher`, you will have to have the
`multiprocessing` package installed. It is part of the standard library for
Python 2.6 and above, but not for earlier versions. A backport of it for Python
2.5 is available at http://pypi.python.org/pypi/multiprocessing .
'''

from .process_cruncher import ProcessCruncher


### Warning if `multiprocessing` isn't installed: #############################
#                                                                             #

from garlicsim.general_misc import import_tools

if not import_tools.exists('multiprocessing'):
    import warnings
    warnings.warn("You don't have the `multiprocessing` package installed. "
                  "GarlicSim will run, but it won't be able to use "
                  "`ProcessCruncher` in order to take advantage of multiple "
                  "processor cores for crunching.")
    
del import_tools

#                                                                             #
### Finished warning about `multiprocessing`. #################################
