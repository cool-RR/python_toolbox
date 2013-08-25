# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import datetime as datetime_module
import os.path
import pstats

import envelopes

from python_toolbox import caching
from python_toolbox import misc_tools

from . import base_profile


class BaseProfileHandler(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __call__(self):
        pass
    
    default_file_name = caching.CachedProperty(
        lambda self: 'profile-%s' % datetime_module.datetime.now()
    )
        
    

class AuxiliaryThreadProfileHandler(BaseProfileHandler):
    
    thread = None
    
    def __call__(self):
        self.thread = threading.Thread(target=self.thread_job)
        self.thread.start()
        
    @abc.abstractmethod
    def thread_job(self):
        pass
    

class EmailProfileHandler(AuxiliaryThreadProfileHandler):
    def __init__(self, email_address, smtp_server, smtp_user, smtp_password,
                 use_tls=True):
        
        if use_tls == 'False':
            use_tls = False
        
        self.email_address = email_address
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.use_tls = use_tls
        
    def thread_job(self, profile_data):
        envelope = envelopes.Envelope(
            to_addr=self.email_address,
            subject='Profile data', 
        )
        
        envelope.add_attachment_from_memory(profile_data,
                                            self.default_file_name, 
                                            'application/octet-stream')
        
        envelope.send(self.smtp_server, login=self.smtp_user,
                      password=self.smtp_password, tls=self.use_tls)
        
        


class FolderProfileHandler(AuxiliaryThreadProfileHandler):
    
    def __init__(self, folder_path):
        self.folder_path = folder_path
        
    def thread_job(self, profile_data):
        with open(os.path.join(self.folder_path, self.default_file_name), \
                                                          'wb') as output_file:
            output_file.write(profile_data)
        


class PrintProfileHandler(BaseProfileHandler):
    
    def __init__(self, sort_order):
        self.sort_order = sort_order
        
    def __call__(self, profile_data):
        pstats.Stats(self).strip_dirs().sort_stats(self.sort_order). \
                                                                  print_stats()
        


def get_profile_handler(profile_handler_string):
    if misc_tools.is_legal_email_address(profile_handler_string.split('\n')
                                                                          [0]):
        return EmailProfileHandler(*profile_handler_string.split('\n'))
    elif os.path.isdir(profile_handler_string):
        return FolderProfileHandler(profile_handler_string)
    else:
        assert profile_handler_string == '' or int(profile_handler_string)
        try:
            sort_order = int(profile_handler_string)
        except ValueError:
            sort_order = -1
        return PrintProfileHandler(sort_order)