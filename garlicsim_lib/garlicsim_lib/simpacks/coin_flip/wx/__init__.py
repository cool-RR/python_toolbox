# This is your `wx` package. It's a sub-package inside your simpack, and like
# most things in your simpack, completely optional. You will only want to fill
# it if you are interested in running your simulation in `garlicsim_wx`.
# Actually, even if you don't fill it in, your simulation will run in
# `garlicsim_wx`-- Just not very prettily.
#
# To make your simulation be prettier, you should start with filling in a state
# viewer. That's in the `wx/widgets/state_viewer.py` module. You may also make a
# state creation dialog, in `wx/widgets/state_creation_dialog`.
#
# When you're done, don't forget to visit `wx/settings.py` to link to the new
# classes you created.
