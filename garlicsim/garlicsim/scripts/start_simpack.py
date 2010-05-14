import re


if not re.search(r'^[_a-zA-Z]\w*$', name): # If it's not a valid directory name.
    # Provide a smart error message, depending on the error.
    if not re.search(r'^[_a-zA-Z]', name):
        message = 'make sure the name begins with a letter or underscore'
    else:
        message = 'use only numbers, letters and underscores'
    raise Exception("%r is not a valid simpack name. Please %s." % (name, message))