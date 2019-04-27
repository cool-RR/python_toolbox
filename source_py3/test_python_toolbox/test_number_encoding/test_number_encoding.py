# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import number_encoding

numbers = (234123, 63435, 2222, 643534, 34, 233)

def test_number_encoding():
    my_encoder = number_encoding.NumberEncoder('isogram')

    for number in numbers:
        string = my_encoder.encode(number)
        assert my_encoder.decode(string) == number
        assert set(string) <= set(my_encoder.characters)

        padded_string = my_encoder.encode(number, 100)
        assert len(padded_string) >= 100
        assert padded_string.endswith(string)
