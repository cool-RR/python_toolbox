# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.sys_tools.OutputCapturer`.'''

from __future__ import with_statement

from garlicsim.general_misc.sys_tools import OutputCapturer


def test():
    '''Test the basic workings of `OutputCapturer`.'''
    with OutputCapturer() as output_capturer:
        print('meow')
    assert output_capturer.output == 'meow\n'
    
    
def test_nested():
    '''Test an `OutputCapturer` inside an `OutputCapturer`.'''
    with OutputCapturer() as output_capturer_1:
        print('123')
        with OutputCapturer() as output_capturer_2:
            print('456')
        assert output_capturer_2.output == '456\n'
    assert output_capturer_1.output == '123\n'
