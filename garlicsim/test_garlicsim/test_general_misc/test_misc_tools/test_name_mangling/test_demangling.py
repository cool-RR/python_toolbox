# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for name demangling.'''


from garlicsim.general_misc.misc_tools import name_mangling
from garlicsim.general_misc.misc_tools.name_mangling import \
                                              demangle_attribute_name_if_needed


def test():
    assert demangle_attribute_name_if_needed('_Cat__meow',
                                             'Cat') == '__meow'
    assert demangle_attribute_name_if_needed('_Cat__meow',
                                             'Dog') == '_Cat__meow'
    assert demangle_attribute_name_if_needed('_Cat__meow',
                                             '__Cat') == '__meow'
    assert demangle_attribute_name_if_needed('_Cat__meow',
                                             '__Cat_') == '_Cat__meow'
    assert demangle_attribute_name_if_needed('_Cat___meow',
                                             '__Cat_') == '__meow'
    assert demangle_attribute_name_if_needed('_Cat___meow',
                                             '_Cat') == '___meow'
    assert demangle_attribute_name_if_needed('_Cat___meow',
                                             '_Cat') == '___meow'
    assert demangle_attribute_name_if_needed('_Cat___meow_',
                                             '_Cat') == '___meow_'
    assert demangle_attribute_name_if_needed('_Cat___meow__',
                                             '_Cat') == '_Cat___meow__'