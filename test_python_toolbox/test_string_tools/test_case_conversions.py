# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.string_tools import case_conversions


def test():
    assert case_conversions.camel_case_to_space_case('HelloWorld') == \
                                                                  'Hello world'
    assert case_conversions.camel_case_to_lower_case('HelloWorld') == \
                                                                  'hello_world'
    assert case_conversions.lower_case_to_camel_case('hello_world') == \
                                                                   'HelloWorld'
    assert case_conversions.camel_case_to_upper_case('HelloWorld') == \
                                                                  'HELLO_WORLD'
    assert case_conversions.upper_case_to_camel_case('HELLO_WORLD') == \
                                                                   'HelloWorld'