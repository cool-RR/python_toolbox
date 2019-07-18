# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import is_legal_ascii_variable_name


def test():
    '''Test `is_legal_variable_name` on various legal and illegal inputs.'''
    legals = ['qwerqw', 'wer23434f3', 'VDF4vr', '_4523ga', 'AGF___43___4_',
              '_', '__', '___']
    illegals = ['1dgfads', 'aga`fdg', '-haeth', '4gag5h+sdfh.', '.afdg',
                'fdga"adfg', 'afdga afd']

    for legal in legals:
        assert is_legal_ascii_variable_name(legal)

    for illegal in illegals:
        assert not is_legal_ascii_variable_name(illegal)