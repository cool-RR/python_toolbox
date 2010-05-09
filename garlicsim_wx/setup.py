#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Setuptools setup file for garlicsim_wx.'''

import os.path
import sys
import glob
import setuptools
import distutils # Just for deleting the "build" directory.


if 'py2exe' in sys.argv:
    # We have a separate file for doing stuff that is needed when packaaging
    # with py2exe.
    import py2exe_cruft.setup_extension


# Automatically deleting the build directory, in case one was left over from
# last time.
try:
    distutils.dir_util.remove_tree('build', verbose=True)
except Exception:
    pass


def get_garlicsim_wx_packages():
    '''
    Get all the packages in garlicsim_wx.
    
    This returns an answer in the form: ['garlicsim_wx.frame',
    'garlicsim_wx.widgets', 'garlicsim_wx.misc', ...]
    '''
    return ['garlicsim_wx.' + p for p
            in setuptools.find_packages('./garlicsim_wx')] + \
           ['garlicsim_wx']

garlicsim_wx_packages = get_garlicsim_wx_packages()


my_long_description = \
'''\
A wxPython-based GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.
'''


my_classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Topic :: Scientific/Engineering',
]



setup_kwargs = {
    'name': 'garlicsim_wx',
    'version': '0.4',
    
    # `garlicsim_lib` is not really required, but in practice the vast majority
    # of users will want it, so we mark it as required in order it to simplify
    # installation.
    'requires': [
        'garlicsim (== 0.4)',
        'garlicsim_lib (== 0.4)'
        ],
    'install_requires': [
        'garlicsim == 0.4',
        'garlicsim_lib == 0.4'
        ],
    
    'description': \
        'GUI for garlicsim, a Pythonic framework for computer simulations',
    'author': 'Ram Rachum',
    'author_email': 'cool-rr@cool-rr.com',
    'url': 'http://garlicsim.org',
    'packages': garlicsim_wx_packages,
    'license': 'Proprietary',
    'long_description': my_long_description,
    'classifiers': my_classifiers,
    'include_package_data': True,
}


if 'py2exe' in sys.argv:
    
    path_to_add = os.path.abspath('./py2exe_cruft')
    if path_to_add not in sys.path:
        sys.path.append(path_to_add)
        # Adding it because there's some dll there that we need, and py2exe
        # looks on sys.path.
    
    setup_kwargs.update(py2exe_cruft.setup_extension.py2exe_kwargs)

    
setuptools.setup(**setup_kwargs)


