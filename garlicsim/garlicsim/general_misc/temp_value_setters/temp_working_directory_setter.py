import os

from .temp_value_setter import TempValueSetter


class TempWorkingDirectorySetter(TempValueSetter):
    def __init__(self, value):
        assert isinstance(value, basestring)
        TempValueSetter.__init__(self, (os.getcwd, os.chdir), value=value)