# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import nose.tools

from python_toolbox import temp_file_tools

from python_toolbox.misc_tools import phrase_iterable_in_english


def test():
    iterables_and_results = (
        ((), ''),
        (['foo'], 'foo'),
        ((1, 2), '1 and 2'),
        ((1, 2, 'meow'), '1, 2 and meow'),
        (iter((1, 2, 'meow')), '1, 2 and meow'),
        ([{'a'}, {'b'}, {'c'}, {'d'}], "{'a'}, {'b'}, {'c'} and {'d'}"),
    )
    for iterable, result in iterables_and_results:
        assert phrase_iterable_in_english(iterable) == result