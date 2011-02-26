# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools related to temporary files.'''

from __future__ import with_statement

import tempfile
import sys
import os as _os

from garlicsim.general_misc.context_manager import ContextManager



class TemporaryDirectory(ContextManager):
    '''tododoc Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everthing contained
    in it are removed.
    '''

    def __init__(self, suffix='', prefix=template, dir=None):
        self._closed = False
        self.name = None # Handle mkdtemp throwing an exception
        self.name = tempfile.mkdtemp(suffix, prefix, dir)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def cleanup(self, _warn=False):
        if self.name and not self._closed:
            try:
                self._rmtree(self.name)
            except (TypeError, AttributeError) as ex:
                # Issue #10188: Emit a warning on stderr
                # if the directory could not be cleaned
                # up due to missing globals
                if 'None' not in str(ex):
                    raise
                sys.stderr.write(
                    'ERROR: %s while cleaning up %s\n' % (ex, self)
                )
                return
            self._closed = True
            if _warn:
                self._warn('Implicitly cleaning up %s' % self,
                           RuntimeWarning)

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def __del__(self):
        # Issue a warning if implicit cleanup needed
        self.cleanup(_warn=True)

    # XXX (ncoghlan): The following code attempts to make
    # this class tolerant of the module nulling out process
    # that happens during CPython interpreter shutdown
    # Alas, it doesn't actually manage it. See issue #10188
    _listdir = staticmethod(_os.listdir)
    _path_join = staticmethod(_os.path.join)
    _isdir = staticmethod(_os.path.isdir)
    _remove = staticmethod(_os.remove)
    _rmdir = staticmethod(_os.rmdir)
    _os_error = _os.error
    _warn = _warnings.warn

    def _rmtree(self, path):
        # Essentially a stripped down version of shutil.rmtree.  We can't
        # use globals because they may be None'ed out at shutdown.
        for name in self._listdir(path):
            fullname = self._path_join(path, name)
            try:
                isdir = self._isdir(fullname)
            except self._os_error:
                isdir = False
            if isdir:
                self._rmtree(fullname)
            else:
                try:
                    self._remove(fullname)
                except self._os_error:
                    pass
        try:
            self._rmdir(path)
        except self._os_error:
            pass
