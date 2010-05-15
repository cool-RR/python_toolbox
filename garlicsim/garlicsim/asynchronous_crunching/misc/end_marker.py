# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines objects for working with simulations that crunch asynchronically.

(Asynchronously means in a separate thread/process.)

The most important class defined here is Project, and it is the only class that
the user needs to interact with. It employs all the other classes.
'''


class EndMarker(object):
    pass