# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools related to temporary files.'''

from __future__ import with_statement

import tempfile
import shutil

from garlicsim.general_misc.context_manager import ContextManager



class TemporaryDirectory(ContextManager):
    '''tododoc Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everthing contained
    in it are removed.
    
    blocktodo: should this act on __init__ or on __enter__? wait for answer
    from python-dev
    '''

    def __init__(self, suffix='', prefix=tempfile.template):
        self.suffix = suffix
        self.prefix = prefix
        self.path = None
        self._closed = False

        
    def __enter__(self):
        return self

    
    def __exit__(self, type_, value, traceback):
        assert not self._closed
        shutil.rmtree(self.path)
        self._closed = True