# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.cute_iter_tools import get_single_if_any


def test_get_single_if_any():
    
    assert get_single_if_any(()) is get_single_if_any([]) is \
           get_single_if_any({}) is get_single_if_any(iter({})) is \
           get_single_if_any('') is None
    
    assert get_single_if_any(('g',)) == get_single_if_any(['g']) == \
           get_single_if_any(set(('g'))) == \
           get_single_if_any(iter(set(('g', )))) == \
           get_single_if_any('g') == 'g'

    with cute_testing.RaiseAssertor():
        get_single_if_any(('g', 'e', 'e'))

    with cute_testing.RaiseAssertor():
        get_single_if_any('gee')
        
    assert get_single_if_any('gee', exception_on_multiple=False) == 'g'
    assert get_single_if_any('gee', none_on_multiple=True) is None
    assert get_single_if_any('gee', none_on_multiple=True,
                             exception_on_multiple=False) is None