# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to temporary files.'''

from __future__ import generator_stop

import tempfile
import shutil
import pathlib

from python_toolbox import context_management


@context_management.ContextManagerType
def create_temp_folder(*, prefix=tempfile.template, suffix='',
                       parent_folder=None, chmod=None):
    '''
    Context manager that creates a temporary folder and deletes it after usage.

    After the suite finishes, the temporary folder and all its files and
    subfolders will be deleted.

    Example:

        with create_temp_folder() as temp_folder:

            # We have a temporary folder!
            assert temp_folder.is_dir()

            # We can create files in it:
            (temp_folder / 'my_file').open('w')

        # The suite is finished, now it's all cleaned:
        assert not temp_folder.exists()

    Use the `prefix` and `suffix` string arguments to dictate a prefix and/or a
    suffix to the temporary folder's name in the filesystem.

    If you'd like to set the permissions of the temporary folder, pass them to
    the optional `chmod` argument, like this:

        create_temp_folder(chmod=0o550)

    '''
    temp_folder = pathlib.Path(tempfile.mkdtemp(prefix=prefix, suffix=suffix,
                                                dir=parent_folder))
    try:
        if chmod is not None:
            temp_folder.chmod(chmod)
        yield temp_folder
    finally:
        shutil.rmtree(str(temp_folder))