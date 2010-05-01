#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Setuptools setup file for garlicsim_wx.'''

import os.path
import sys
import glob
import setuptools
import distutils # Just for deleting the "build" directory.
try:
    import py2exe
except ImportError:
    pass

# tododoc: the py2exe parts assume `garlicsim` is in the neighboring directory
# like in the git repo

path_to_garlicsim = os.path.abspath('../garlicsim')
if path_to_garlicsim not in sys.path:
    sys.path.append(path_to_garlicsim)

try:
    distutils.dir_util.remove_tree('build', verbose=True)
except Exception:
    pass

def package_to_path(package):
    return package.replace('.', '/')

def get_garlicsim_packages():
    return ['garlicsim.' + p for p
            in setuptools.find_packages('../garlicsim/garlicsim')] + \
           ['garlicsim']

garlicsim_packages = get_garlicsim_packages()

def get_garlicsim_wx_packages():
    return ['garlicsim_wx.' + p for p
            in setuptools.find_packages('./garlicsim_wx')] + \
           ['garlicsim_wx']

garlicsim_wx_packages = get_garlicsim_wx_packages()

def get_garlicsim_wx_data_files():
    total_data_files = []
    for package in garlicsim_wx_packages:
        path = package_to_path(package)
        all_files_and_folders = glob.glob(path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files

def get_garlicsim_data_files():
    total_data_files = []
    for package in garlicsim_packages:
        path = package_to_path(package)
        all_files_and_folders = glob.glob(path_to_garlicsim + '/' + path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files

def get_all_data_files():
    return get_garlicsim_wx_data_files() + get_garlicsim_data_files()

g=get_garlicsim_data_files()

my_long_description = \
'''\
garlicsim_wx, a wxPython GUI for garlicsim.

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


more_kwargs = {}

if 'py2exe' in sys.argv:

    py2exe_kwargs = {
        'windows': [
            {
                'script': 'py2exe_cruft/GarlicSim.py',
                'icon_resources': [
                    (
                        0,
                        'garlicsim_wx/misc/icon_bundle/images/garlicsim.ico'
                    )
                ]
            }
            ],
        'zipfile': 'lib/library.zip',
        'data_files': get_all_data_files(),
        'options': {
            'py2exe': {
                'dist_dir': 'py2exe_dist',
                'packages': garlicsim_wx_packages,
                'skip_archive': True,
                'packages': 'garlicsim.bundled.simulation_packages',
            }
        }
    }

    more_kwargs.update(py2exe_kwargs)

    
setuptools.setup(
    name='garlicsim_wx',
    version='0.4',
    requires=['garlicsim (== 0.4)'],
    install_requires=['garlicsim == 0.4'],
    description='Gui for garlicsim, a Pythonic framework for working with simulations',
    author='Ram Rachum',
    author_email='cool-rr@cool-rr.com',
    url='http://garlicsim.org',
    packages=garlicsim_wx_packages,
    license='Proprietary',
    long_description = my_long_description,
    classifiers = my_classifiers,
    include_package_data = True,
    **more_kwargs
)
