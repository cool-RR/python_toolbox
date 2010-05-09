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

# tododoc: move all the py2exe parts to `py2exe_cruft`

# tododoc: document this module exhaustively.


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

def get_dlls_and_stuff():
    total_data_files = []
    path_to_folder = './py2exe_cruft/dlls_and_stuff'
    folders_to_do = [path_to_folder]
    while folders_to_do:
        path = folders_to_do.pop()
        assert not os.path.isabs(path)
        all_files_and_folders = glob.glob(path + '/*')
        files = [f for f in all_files_and_folders if (not os.path.isdir(f))]
        folders = [f for f in all_files_and_folders if os.path.isdir(f)]
        folders_to_do += folders
        total_data_files.append(
            (
                os.path.relpath(path, './py2exe_cruft/dlls_and_stuff'),
                files
            )
        )
    return total_data_files


def get_all_data_files():
    '''For use in py2exe only.tododoc'''
    return get_garlicsim_wx_data_files() + get_garlicsim_data_files() + \
           get_dlls_and_stuff()


my_long_description = \
'''\
garlicsim_wx, a wxPython GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.
d'''


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
    'requires': ['garlicsim (== 0.4)'],
    'install_requires': ['garlicsim == 0.4'],
    'description': 'Gui for garlicsim, a Pythonic framework for computer simulations',
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
        # Adding it because there's some dll there that we need.
    
    py2exe_kwargs = {
        'description': 'Pythonic framework for computer simulations',
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
                'skip_archive': True,
                'packages': [
                    
                    # Here you put packages you want py2exe to include with all
                    # subpackages. Problem is, there's a bug in py2exe which
                    # will make it think a non-package directory is a package if
                    # it contains a package within it. Then it'll get listed as
                    # a package, and when import time comes the script will
                    # fail.
                    
                    # So there's a danger for us here: For example, we can't
                    # include `numpy` because it has some `tests` folder which
                    # falls under this bug.
                    
                    'garlicsim_lib.simpacks',
                    
                    'numpy.core', 'numpy.lib', 'numpy.matlib', 'numpy.dual',
                    'numpy.numarray', 'numpy.oldnumeric', 'numpy.ctypeslib',
                    'numpy.testing', 'numpy.random', 'numpy.linalg', 'numpy.fft',
                    
                    'scipy',
                    
                    ],
                    
            }
        }
    }

    setup_kwargs.update(py2exe_kwargs)

    
setuptools.setup(
    **setup_kwargs
)
