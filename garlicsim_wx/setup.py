#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for `garlicsim_wx`.'''

import os.path
import sys
import glob
import setuptools


### Ensuring correct Python version: ##########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception('This package is not compatible with Python 3.x.')
if sys.version_info[1] <= 4:
    raise Exception('This package requires Python 2.5 and upwards. (Not '
                    'including 3.x).')
#                                                                             #
### Finished ensuring correct Python version. #################################


if 'py2exe' in sys.argv:
    # We have a separate file for doing stuff that is needed when packaging
    # with `py2exe`.
    import py2exe_cruft.setup_extension


def get_garlicsim_wx_packages():
    '''
    Get all the packages in `garlicsim_wx`.
    
    Returns something like:
    
        ['garlicsim_wx', 'garlicsim_wx.app', 'garlicsim_wx.widgets', ... ]
        
    '''
    return ['garlicsim_wx.' + p for p in
            setuptools.find_packages('./garlicsim_wx')] + \
           ['garlicsim_wx']


def get_test_garlicsim_wx_packages():
    '''
    Get all the packages in `test_garlicsim_wx`.
    
    Returns something like:
    
        ['test_garlicsim_wx', 'test_garlicsim_wx.test_import', ...]
        
    '''
    return ['test_garlicsim_wx.' + p for p in
            setuptools.find_packages('./test_garlicsim_wx')] + \
           ['test_garlicsim_wx']


def get_packages():
    '''
    Get all the packages in `garlicsim_wx` and `test_garlicsim_wx`.
    
    Returns something like:
    
        ['test_garlicsim_wx', 'garlicsim_wx', 'garlicsim_wx.app',
        'test_garlicsim_wx.test_import', ... ]
        
    '''
    return get_garlicsim_wx_packages() + get_test_garlicsim_wx_packages()


my_long_description = \
'''\
A wxPython-based GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.
'''


my_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    ('License :: OSI Approved :: GNU Library or Lesser General '
     'Public License (LGPL)'),
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering',
]



setup_kwargs = {
    'name': 'garlicsim_wx',
    'version': '0.6.3',
    
    # `garlicsim_lib` is not really required, but in practice the vast majority
    # of users will want it, so we mark it as required in order it to simplify
    # installation.
    'requires': [
        'garlicsim (== 0.6.3)',
        'garlicsim_lib (== 0.6.3)'
        ],
    'install_requires': [
        'garlicsim == 0.6.3',
        'garlicsim_lib == 0.6.3'
        ],
    
    'tests_require': ['nose>=1.0.0'],
    'description': \
        'GUI for garlicsim, a Pythonic framework for computer simulations',
    'author': 'Ram Rachum',
    'author_email': 'ram@rachum.com',
    'url': 'http://garlicsim.org',
    'packages': get_packages(),
    'scripts': ['garlicsim_wx/scripts/GarlicSim.py',
                'test_garlicsim_wx/scripts/_test_garlicsim_wx.py'],
    'license': 'LGPL v2.1',
    'long_description': my_long_description,
    'classifiers': my_classifiers,
    'include_package_data': True,
    'zip_safe': False,
}


if 'py2exe' in sys.argv:
    
    path_to_add = os.path.realpath('./py2exe_cruft')
    if path_to_add not in sys.path:
        sys.path.append(path_to_add)
        # Adding it because there's some dll there that we need, and `py2exe`
        # looks on `sys.path`.
    
    setup_kwargs.update(py2exe_cruft.setup_extension.py2exe_kwargs)

    
setuptools.setup(**setup_kwargs)


