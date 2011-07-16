# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for handling ReStructuredText.'''

import docutils.core


def rst_to_html(rst_text):
    '''Convert a piece of `rst_text` into HTML.'''
    return docutils.core.publish_parts(rst_text, writer_name='html')['body']