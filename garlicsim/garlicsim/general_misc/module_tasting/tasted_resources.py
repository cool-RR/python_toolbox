# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import types
import sys

import pkg_resources


from .module_tasting import taste_module


def get_provider(module_or_name_or_req):
    '''Get an `IResourceProvider` for the named module or requirement.'''
    if isinstance(module_or_name_or_req, pkg_resources.Requirement):
        return pkg_resources.working_set.find(module_or_name_or_req) or \
                           pkg_resources.require(str(module_or_name_or_req))[0]
    elif isinstance(module_or_name_or_req, types.ModuleType):
        tasted_module = module_or_name_or_req
    else:
        assert isinstance(module_or_name_or_req, basestring)
        try:
            tasted_module = sys.modules[module_or_name_or_req]
        except KeyError:
            tasted_module = taste_module(module_or_name_or_req)
    loader = getattr(tasted_module, '__loader__', None)
    adapter = pkg_resources._find_adapter(
        pkg_resources._provider_factories,
        loader
    )
    return adapter(tasted_module)


def resource_exists(package_or_requirement, resource_name):
    '''Does the named resource exist?'''
    return get_provider(package_or_requirement).has_resource(resource_name)


def resource_isdir(package_or_requirement, resource_name):
    '''Is the named resource an existing directory?'''
    return get_provider(package_or_requirement).resource_isdir(
        resource_name
    )


def resource_filename(package_or_requirement, resource_name):
    '''Return a true filesystem path for specified resource.'''
    return get_provider(package_or_requirement).get_resource_filename(
        pkg_resources._manager, resource_name
    )


def resource_stream(package_or_requirement, resource_name):
    '''Return a readable file-like object for specified resource.'''
    return get_provider(package_or_requirement).get_resource_stream(
        pkg_resources._manager, resource_name
    )


def resource_string(package_or_requirement, resource_name):
    '''Return specified resource as a string.'''
    return get_provider(package_or_requirement).get_resource_string(
        pkg_resources._manager, resource_name
    )


def resource_listdir(package_or_requirement, resource_name):
    '''List the contents of the named resource directory.'''
    return get_provider(package_or_requirement).resource_listdir(
        resource_name
    )