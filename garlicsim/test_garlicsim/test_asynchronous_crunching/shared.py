# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for testing `garlicsim.asynchronous_crunching`.'''

from garlicsim.asynchronous_crunching.crunchers import ThreadCruncher


class MustachedThreadCruncher(ThreadCruncher):
    '''A trivial subclass of `ThreadCruncher` for use in testing.'''