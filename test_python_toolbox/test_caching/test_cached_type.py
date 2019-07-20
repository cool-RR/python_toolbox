# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.caching.CachedType`.'''

from python_toolbox.caching import CachedType


def test():
    '''Test basic workings of `CachedType`.'''
    class A(metaclass=CachedType):
        def __init__(self, a=1, b=2, *args, **kwargs):
            pass

    assert A() is A(1) is A(b=2) is A(1, 2) is A(1, b=2)
    assert A() is not A(3) is not A(b=7) is not A(1, 2, 'meow') is not A(x=9)

def test_keyword_only_separator_and_annotations():
    class B(metaclass=CachedType):
        def __init__(self, a: int, b: float, *, c: 'lol' = 7) -> None:
            pass

    assert B(1, 2) is B(b=2, a=1, c=7) is not B(b=2, a=1, c=8)