# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines tools for testing `python_toolbox.pickle_tools`'''


class PickleableObject(object):
    _is_atomically_pickleable = True
    

class NonPickleableObject(object):
    _is_atomically_pickleable = False
    