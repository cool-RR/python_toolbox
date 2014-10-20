# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for handling ReStructuredText.'''

import docutils.core


def rst_to_html(rst_text):
    '''Convert a piece of `rst_text` into HTML.'''
    return docutils.core.publish_parts(rst_text, writer_name='html')['body']