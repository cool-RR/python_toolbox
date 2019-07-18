# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import sequence_tools


class NumberEncoder:
    '''
    A very simple encoder between lines and strings.

    Example:

        >>> my_encoder = number_encoding.NumberEncoder('isogram')
        >>> my_encoder.encode(10000)
        'rssir'
        >>> my_encoder.encode(10000000)
        'saimmmgrg'
        >>> my_encoder.decode('saimmmgrg')
        10000000

    '''
    def __init__(self, characters):
        self.characters = \
               sequence_tools.ensure_iterable_is_immutable_sequence(characters)
        recurrences = sequence_tools.get_recurrences(self.characters)
        if recurrences:
            raise Exception('`characters` must not have recurring characters.')

    def encode(self, number, minimum_length=1):
        '''
        Encode the number into a string.

        If `minimum_length > 1`, the string will be padded (with the "zero"
        character) if the number isn't big enough.
        '''
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
        '''Decode `string` into a number'''

        assert isinstance(string, (str, bytes))
        return sum((len(self.characters)**i) * self.characters.index(x)
                                         for (i, x) in enumerate(string[::-1]))

    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, repr(self.characters))
