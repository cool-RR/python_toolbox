import sys

from .temp_value_setter import TempValueSetter


class TempRecursionLimitSetter(TempValueSetter):
    def __init__(self, value):
        assert isinstance(value, int)
        TempValueSetter.__init__(
            self,
            (sys.getrecursionlimit, sys.setrecursionlimit),
            value=value
        )