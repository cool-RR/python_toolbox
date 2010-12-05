from __future__ import print_function

from garlicsim.general_misc.sys_tools import OutputCapturer


def test():
    with OutputCapturer() as output_capturer:
        print('meow')
    assert output_capturer.output == 'meow\n'
    
    
def test_nested():
    with OutputCapturer() as output_capturer_1:
        print('123')
        with OutputCapturer() as output_capturer_2:
            print('456')
        assert output_capturer_2.output == '456\n'
    assert output_capturer_1.output == '123\n'
        