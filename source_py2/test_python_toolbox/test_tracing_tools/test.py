# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import tracing_tools


def my_function():
    ''' '''

def test():
    ''' '''

    with tracing_tools.TempFunctionCallCounter(my_function) as \
                                                    temp_function_call_counter:
        assert temp_function_call_counter.call_count == 0
        my_function()
        assert temp_function_call_counter.call_count == 1
        my_function()
        my_function()
        my_function()
        assert temp_function_call_counter.call_count == 4

    assert temp_function_call_counter.call_count == 4
    my_function()
    assert temp_function_call_counter.call_count == 4
