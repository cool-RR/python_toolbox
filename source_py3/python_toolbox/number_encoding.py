# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import sequence_tools


class NumberEncoder:
    def __init__(self, characters):
        self.characters = \
               sequence_tools.ensure_iterable_is_immutable_sequence(characters)
        recurrences = sequence_tools.get_recurrences(self.characters)
        if recurrences:
            raise Exception('`characters` must not have recurring characters.')
        
    def encode(number, minimum_length=1):
        current_number = number
        result = ''
        while current_number:
            current_number, modulo = divmod(current_number,
                                            len(self.characters))
            result = self.characters[modulo] + result
        if len(result) <= minimum_length:
            result = (self.characters[0] * (minimum_length - len(result))) + result
        return result

    def decode(self, string):
        assert isinstance(string, (str, bytes))
        return sum((len(self.characters)**i) * self.characters.index(x)
                                         for (i, x) in enumerate(string[::-1]))
