# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.


from python_toolbox.misc_tools import name_mangling
from python_toolbox.misc_tools.name_mangling import \
                                              unmangle_attribute_name_if_needed


def test():
    assert unmangle_attribute_name_if_needed('_Cat__meow',
                                             'Cat') == '__meow'
    assert unmangle_attribute_name_if_needed('_Cat__meow',
                                             'Dog') == '_Cat__meow'
    assert unmangle_attribute_name_if_needed('_Cat__meow',
                                             '__Cat') == '__meow'
    assert unmangle_attribute_name_if_needed('_Cat__meow',
                                             '__Cat_') == '_Cat__meow'
    assert unmangle_attribute_name_if_needed('_Cat___meow',
                                             '__Cat_') == '__meow'
    assert unmangle_attribute_name_if_needed('_Cat___meow',
                                             '_Cat') == '___meow'
    assert unmangle_attribute_name_if_needed('_Cat___meow',
                                             '_Cat') == '___meow'
    assert unmangle_attribute_name_if_needed('_Cat___meow_',
                                             '_Cat') == '___meow_'
    assert unmangle_attribute_name_if_needed('_Cat___meow__',
                                             '_Cat') == '_Cat___meow__'