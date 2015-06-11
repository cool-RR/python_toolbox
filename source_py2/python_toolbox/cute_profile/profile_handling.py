# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import datetime as datetime_module
import marshal
try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib

import abc
import pstats

from python_toolbox.third_party import envelopes

from python_toolbox import caching
from python_toolbox import misc_tools

from . import base_profile


class BaseProfileHandler(object):
    '''Profile handler which saves the profiling result in some way.'''

    __metaclass__ = abc.ABCMeta
    
    def __call__(self, profile):
        self.profile = profile
        self.profile_data = marshal.dumps(profile.stats)
        return self.handle()
    
    @abc.abstractmethod
    def handle(self):
        pass
    
    make_file_name = lambda self: ('%s.profile' %
                              datetime_module.datetime.now()).replace(':', '.')
        
    

class AuxiliaryThreadProfileHandler(BaseProfileHandler):
    '''Profile handler that does its action on a separate thread.'''
    thread = None
    
    def handle(self):
        self.thread = threading.Thread(target=self.thread_job)
        self.thread.start()
    
    @abc.abstractmethod
    def thread_job(self):
        pass
    

class EmailProfileHandler(AuxiliaryThreadProfileHandler):
    '''Profile handler that sends the profile via email on separate thread.'''
    def __init__(self, email_address, smtp_server, smtp_user, smtp_password,
                 use_tls=True):
        
        if use_tls == 'False':
            use_tls = False
        
        self.email_address = email_address
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.use_tls = use_tls
        
    def thread_job(self):
        envelope = envelopes.Envelope(
            to_addr=self.email_address,
            subject='Profile data', 
        )
        
        envelope.add_attachment_from_string(self.profile_data,
                                            self.make_file_name(), 
                                            'application/octet-stream')
        
        envelope.send(self.smtp_server, login=self.smtp_user,
                      password=self.smtp_password, tls=self.use_tls)
        
        


class FolderProfileHandler(AuxiliaryThreadProfileHandler):
    '''Profile handler that saves the profile to disk on separate thread.'''
    
    def __init__(self, folder):
        self.folder = pathlib.Path(folder)
        
    def thread_job(self):
        with (self.folder / self.make_file_name()).open('wb') as output_file:
            output_file.write(self.profile_data)
        


class PrintProfileHandler(BaseProfileHandler):
    '''Profile handler that prints profile data to standard output.'''
    def __init__(self, sort_order):
        self.sort_order = sort_order
        
    def handle(self):
        self.profile.print_stats(self.sort_order)
        
        


def get_profile_handler(profile_handler_string):
    '''Parse `profile_handler_string` into a `ProfileHandler` class.'''
    if isinstance(profile_handler_string, pathlib.Path):
        assert profile_handler_string.is_dir()
        return FolderProfileHandler(profile_handler_string)
    if not profile_handler_string or profile_handler_string in \
                                                     ['0', '1', '2', '3', '4']:
        try:
            sort_order = int(profile_handler_string)
        except (ValueError, TypeError):
            sort_order = -1
        return PrintProfileHandler(sort_order)    
    elif misc_tools.is_legal_email_address(profile_handler_string.split('\n')
                                                                          [0]):
        return EmailProfileHandler(*profile_handler_string.split('\n'))
    else:
        assert pathlib.Path(profile_handler_string).is_dir()
        return FolderProfileHandler(profile_handler_string)
