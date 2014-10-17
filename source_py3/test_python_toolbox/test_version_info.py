# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.version_info.VersionInfo`.'''

from python_toolbox.version_info import VersionInfo


def test():
    '''Test the basic workings of `VersionInfo`.'''
    
    version_info_0 = VersionInfo(1, 7, 8)
    version_info_1 = VersionInfo(9, 7, 3)
    version_info_2 = VersionInfo(major=22)
    
    assert version_info_0 < version_info_1 < version_info_2
    assert version_info_0 <= version_info_1 <= version_info_2
    
    assert version_info_0.major == 1
    assert version_info_0.minor == version_info_1.minor == 7
    assert version_info_0.modifier == version_info_1.modifier == \
                                           version_info_2.modifier == 'release'
    
    
    version_info_4 = VersionInfo(9, 7, 8)
    version_info_5 = VersionInfo(9, 7, 8, 'alpha')
    version_info_6 = VersionInfo(9, 7, 8, 'beta')
    version_info_7 = VersionInfo(9, 7, 8, 'rc')
    version_info_8 = VersionInfo(9, 7, 8, 'release')
    
    assert version_info_4 == version_info_8
    assert sorted((version_info_5, version_info_6, version_info_7,
                   version_info_8)) == \
           [version_info_5, version_info_6, version_info_7, version_info_8]
    
    
def test_version_text():
    assert VersionInfo(1, 5, 3).version_text == '1.5.3'
    assert VersionInfo(1, 0, 3).version_text == '1.0.3'
    assert VersionInfo(1, 0).version_text == '1.0.0'
    assert VersionInfo(1).version_text == '1.0.0'
    assert VersionInfo(1, 0, modifier='rc').version_text == '1.0.0 rc'
    assert VersionInfo(4, modifier='beta').version_text == '4.0.0 beta'