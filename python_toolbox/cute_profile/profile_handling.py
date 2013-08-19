# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import threading

import envelopes


class BaseProfileHandler(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __call__(self):
        pass
        
    

class AuxiliaryThreadProfileHandler(BaseProfileHandler):
    
    thread = None
    
    def __call__(self):
        self.thread = threading.Thread(target=self.thread_job)
        self.thread.start()
        
    @abc.abstractmethod
    def thread_job(self):
        pass
    

class EmailProfileHandler(BaseProfileHandler):
    def __init__(self, email_address, smtp_server, smtp_user, smtp_password,
                 use_tls=True):
        
        self.email_address = email_address
        
        s
        
    def thread_job(self):
        envelope = envelopes.Envelope(to_addr=self.email_address,
                                      subject='Profile data')
        
        envelope.add_attachment('/Users/bilbo/Pictures/helicopter.jpg')
        
        envelope.send('smtp.googlemail.com', login='from@example.com',
                      password='password', tls=True)
        
        ('profile-%s-%s' % (cleaned_path,
                            datetime_tools.get_now()),
         profile_data, 
         'application/octet-stream'), 





def get_profile_handler(profile_handler_string):
    
    
    