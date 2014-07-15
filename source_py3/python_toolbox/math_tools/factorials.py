# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

infinity = float('inf')


def reverse_factorial(number, round_up=True):
    assert number >= 0
    if number == 0:
        return 0
    elif number < 1:
        return int(round_up) # Heh.
    elif number == 1:
        return 1
    else:
        current_number = 1
        for multiplier in itertools.count(2):
            current_number *= multiplier
            if current_number == number:
                return multiplier
            elif current_number > number:
                return multiplier if round_up else (multiplier - 1)
        
    
def from_factoradic(factoradic_number):
    assert isinstance(factoradic_number, collections.Iterable)
    factoradic_number = \
              sequence_tools.ensure_iterable_is_sequence(factoradic_number)
    number = 0
    for i, value in enumerate(reversed(factoradic_number)):
        assert 0 <= value <= i
        number += value * math.factorial(i)
    return number
        

def to_factoradic(number, n_digits_pad=None):
    assert isinstance(number, int)
    assert number >= 0
    n_digits = reverse_factorial(number, round_up=False) + 1
    digits = [None] * n_digits
    current_number = number
    for i in range(n_digits)[::-1]:
        unit = math.factorial(i)
        digits[n_digits - i - 1], current_number = \
                                                   divmod(current_number, unit)
    result = tuple(digits)
    if n_digits_pad and (len(result) < n_digits_pad):
        return ((0,) * (n_digits_pad - len(result))) + result
    else:
        return result
    
