# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import numbers

from python_toolbox.dict_tools import remove_keys


def test():
    '''Test the basic workings of `sum_dicts`.'''
    origin_dict = {1: 2, 3: 4, 5: 6, 7: 8, 9: 10, 11: 12, 13: 14, 15: 16,}

    not_divide_by_three_dict = dict(origin_dict)
    remove_keys(not_divide_by_three_dict, range(0, 50, 3))
    assert not_divide_by_three_dict == {1: 2, 5: 6, 7: 8, 11: 12, 13: 14}

    below_ten_dict = dict(origin_dict)
    remove_keys(below_ten_dict, lambda value: value >= 10)
    assert below_ten_dict == {1: 2, 3: 4, 5: 6, 7: 8, 9: 10}

    class HoledNumbersContainer:
        '''Contains only numbers that have a digit with a hole in it.'''
        def __contains__(self, number):
            if not isinstance(number, numbers.Integral):
                return False
            return bool(set(str(number)).intersection({'0', '4', '6', '8', '9'}))


    non_holed_numbers_dict = dict(origin_dict)
    remove_keys(non_holed_numbers_dict, HoledNumbersContainer())
    assert non_holed_numbers_dict == {1: 2, 3: 4, 5: 6, 7: 8, 11: 12, 13: 14,
                                      15: 16,}

