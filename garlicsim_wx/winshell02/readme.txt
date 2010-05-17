**********************
Python winshell Module
**********************

What is it?
===========

Certain aspects of the Windows user interface are grouped by
 Microsoft as Shell functions. These include the Desktop, shortcut
 icons, special folders (such as My Documents) and a few other things.

These are mostly available via the shell module of the win32all
 extensions, but whenever I need to use them, I've forgotten the
 various constants and so on.

Several of the shell items have two variants: personal and common,
 or User and All Users. These refer to systems with profiles in use:
 anything from NT upwards, and 9x with Profiles turned on. Where
 relevant, the Personal/User version refers to that owned by the
 logged-on user and visible only to that user; the Common/All Users
 version refers to that maintained by an Administrator and visible
 to all users of the system.
 
There are other generally useful functions which are grouped under
 the heading of shell-related, for example moving & copying files
 with animated progress icons and deleting them into the system
 recycle bin.


Where do I get it?
==================

http://timgolden.me.uk/python/winshell.html


Copyright & License?
====================

(c) Tim Golden <mail@timgolden.me.uk> 25th November 2003
Licensed under the (GPL-compatible) MIT License:
http://www.opensource.org/licenses/mit-license.php


How do I install it?
====================

When all's said and done, it's just a module. But for those
who like setup programs:

python setup.py install


Prerequisites
=============

If you're running a recent Python (2.1+) on a recent Windows (2k, 2k3, XP)
and you have Mark Hammond's win32 extensions installed, you're probably
up-and-running already. Otherwise...

  Python
  ------
  http://www.python.org/ (just in case you didn't know)

  pywin32 (was win32all)
  ----------------------
  http://starship.python.net/crew/mhammond/win32/Downloads.html


How do I use it?
================

There are (brief) examples at: http://timgolden.me.uk/python/winshell.html
