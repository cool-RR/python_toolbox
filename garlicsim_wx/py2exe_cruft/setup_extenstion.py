# tododoc: document extensively

import setuptools
import py2exe
import imp
import sys, os.path, glob

path_to_garlicsim = os.path.abspath('../../garlicsim')
path_to_garlicsim_lib = os.path.abspath('../../garlicsim_lib')
paths_to_add = [path_to_garlicsim, path_to_garlicsim_lib]
for path_to_add in paths_to_add:
    if path_to_add not in sys.path:
        sys.path.append(path_to_add)


def package_to_path(package):
    return package.replace('.', '/')


def get_garlicsim_packages():
    return ['garlicsim.' + p for p
            in setuptools.find_packages('../../garlicsim/garlicsim')] + \
           ['garlicsim']

garlicsim_packages = get_garlicsim_packages()


def get_garlicsim_lib_packages():
    return ['garlicsim_lib.' + p for p
            in setuptools.find_packages('../../garlicsim_lib/garlicsim_lib')] + \
           ['garlicsim_lib']

garlicsim_lib_packages = get_garlicsim_lib_packages()


def get_garlicsim_wx_packages():
    return ['garlicsim_wx.' + p for p
            in setuptools.find_packages('../garlicsim_wx')] + \
           ['garlicsim_wx']

garlicsim_wx_packages = get_garlicsim_wx_packages()


def get_garlicsim_data_files():
    total_data_files = []
    for package in garlicsim_packages:
        path = package_to_path(package)
        all_files_and_folders = glob.glob(path_to_garlicsim + '/' + path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files


def get_garlicsim_lib_data_files():
    total_data_files = []
    for package in garlicsim_lib_packages:
        path = package_to_path(package)
        all_files_and_folders = glob.glob(path_to_garlicsim + '/' + path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files


def get_garlicsim_wx_data_files():
    total_data_files = []
    for package in garlicsim_wx_packages:
        path = package_to_path(package)
        all_files_and_folders = glob.glob(path + '/*')
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
    return get_garlicsim_data_files() + get_garlicsim_lib_data_files() + \
           get_garlicsim_wx_data_files() + get_dlls_and_stuff()


def get_all_subpackages(package_name):
    return [
        (package_name + '.' + m) for m in 
        setuptools.find_packages(
            imp.find_module(package_name)[1]
        )
    ]


packages_to_include_with_all_subpackages = [
    
    'garlicsim', 'garlicsim_lib',
    
    'numpy', 'scipy'
    
]


includes = reduce(
    list.__add__,
    [get_all_subpackages(package_name) for package_name in \
     packages_to_include_with_all_subpackages]
)


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
    'zipfile': 'lib/library.zip', #tododoc: probably cancel
    'data_files': get_all_data_files(),
    'options': {
        'py2exe': {
            'dist_dir': 'py2exe_dist',
            'skip_archive': True,
            
            # tododoc.Here you put packages you want py2exe to include with all
            # subpackages. Problem is, there's a bug in py2exe which will make
            # it think a non-package directory is a package if it contains a
            # package within it. Then it'll get listed as a package, and when
            # import time comes the script will fail.
            
            # So there's a danger for us here: For example, we can't include
            # `numpy` because it has some `tests` folder which falls under this
            # bug.
            
            'includes': includes,
                
        }
    }
}