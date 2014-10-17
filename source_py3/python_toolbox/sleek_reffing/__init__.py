# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `SleekRef` class and various data types using it.

See documentation of `SleekRef` for more details. `SleekCallArgs` and
`CuteSleekValueDict` are data types which rely on `SleekRef`.
'''

from .sleek_ref import SleekRef
from .exceptions import SleekRefDied
from .sleek_call_args import SleekCallArgs
from .cute_sleek_value_dict import CuteSleekValueDict


__all__ = ['SleekRef', 'SleekRefDied', 'SleekCallArgs', 'CuteSleekValueDict']
