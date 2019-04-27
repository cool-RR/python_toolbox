# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.sys_tools.OutputCapturer`.'''

import sys

from python_toolbox.sys_tools import OutputCapturer


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


def test_streams():
    '''Test capturing different streams with `OutputCapturer`.'''
    with OutputCapturer() as catch_all_output_capturer:
        with OutputCapturer(True, False) as stdout_output_capturer:
            print('Woo!')
            sys.stdout.write('frrr.')
            sys.stderr.write('qwerty')
        assert stdout_output_capturer.output == 'Woo!\nfrrr.'
        assert catch_all_output_capturer.output == 'qwerty'

        with OutputCapturer(False, False) as blank_output_capturer:
            print('zort')
            sys.stdout.write('zort')
            sys.stderr.write('zort')
        assert blank_output_capturer.output == ''
        assert catch_all_output_capturer.output.endswith('zort\nzortzort')

        with OutputCapturer(stdout=False) as stderr_output_capturer:
            print('one')
            sys.stdout.write('two')
            sys.stderr.write('three')

            with OutputCapturer():
                print('spam')
                sys.stdout.write('spam')
                sys.stderr.write('spam')

        assert stderr_output_capturer.output == 'three'
        assert catch_all_output_capturer.output.endswith('one\ntwo')
        assert 'spam' not in stderr_output_capturer.output
        assert 'spam' not in catch_all_output_capturer.output



