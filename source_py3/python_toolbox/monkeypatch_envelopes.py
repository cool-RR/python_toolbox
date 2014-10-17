# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for monkeypatching our own copy of `envelopes`.'''

### Monkeypatching envelopes: #################################################
#                                                                             #
from python_toolbox.third_party import envelopes
from python_toolbox import monkeypatching_tools


@monkeypatching_tools.monkeypatch(envelopes.Envelope)
def add_attachment_from_string(self, file_data, file_name, 
                               mimetype='application/octet-stream'):
    from python_toolbox.third_party.envelopes.envelope import \
                                                   MIMEBase, email_encoders, os
    type_maj, type_min = mimetype.split('/')
        
    part = MIMEBase(type_maj, type_min)
    part.set_payload(file_data)
    email_encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="%s"'
                    % file_name)

    self._parts.append((mimetype, part))

#                                                                             #
### Finished monkeypatching envelopes. ########################################
