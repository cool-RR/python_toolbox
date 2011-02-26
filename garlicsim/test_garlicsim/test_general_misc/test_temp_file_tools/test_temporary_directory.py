# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''

'''

from __future__ import with_statement

import re
import os
import tempfile
import warnings

import nose.tools
from garlicsim.general_misc.third_party import unittest2

import garlicsim

from garlicsim.general_misc.temp_file_tools import TemporaryDirectory
from garlicsim.general_misc.sys_tools import OutputCapturer

has_stat = hasattr(os, 'stat')
if has_stat:
    import stat
    

class TestCase(unittest2.TestCase):

    str_check = re.compile(r'[a-zA-Z0-9_-]{6}$')

    def setUp(self):
        #self._warnings_manager = support.check_warnings()
        #self._warnings_manager.__enter__()
        warnings.filterwarnings('ignore', category=RuntimeWarning,
                                message='mktemp', module=__name__)

    def tearDown(self):
        pass #self._warnings_manager.__exit__(None, None, None)


    def failOnException(self, what, ei=None):
        if ei is None:
            ei = sys.exc_info()
        self.fail('%s raised %s: %s' % (what, ei[0], ei[1]))

    def nameCheck(self, name, dir, pre, suf):
        (ndir, nbase) = os.path.split(name)
        npre  = nbase[:len(pre)]
        nsuf  = nbase[len(nbase)-len(suf):]

        # check for equality of the absolute paths!
        self.assertEqual(os.path.abspath(ndir), os.path.abspath(dir),
                         "file '%s' not in directory '%s'" % (name, dir))
        self.assertEqual(npre, pre,
                         "file '%s' does not begin with '%s'" % (nbase, pre))
        self.assertEqual(nsuf, suf,
                         "file '%s' does not end with '%s'" % (nbase, suf))

        nbase = nbase[len(pre):len(nbase)-len(suf)]
        self.assertTrue(self.str_check.match(nbase),
                     "random string '%s' does not match /^[a-zA-Z0-9_-]{6}$/"
                     % nbase)

        
class test_TemporaryDirectory(TestCase):
    '''Test TemporaryDirectory().'''

    def do_create(self, dir=None, pre="", suf="", recurse=1):
        if dir is None:
            dir = tempfile.gettempdir()
        try:
            tmp = TemporaryDirectory(dir=dir, prefix=pre, suffix=suf)
        except:
            self.failOnException("TemporaryDirectory")
        self.nameCheck(tmp.name, dir, pre, suf)
        # Create a subdirectory and some files
        if recurse:
            self.do_create(tmp.name, pre, suf, recurse-1)
        with open(os.path.join(tmp.name, "test.txt"), "wb") as f:
            f.write("Hello world!")
        return tmp

    def test_mkdtemp_failure(self):
        # Check no additional exception if mkdtemp fails
        # Previously would raise AttributeError instead
        # (noted as part of Issue #10188)
        with TemporaryDirectory() as nonexistent:
            pass
        with self.assertRaises(os.error):
            TemporaryDirectory(dir=nonexistent)

    def test_explicit_cleanup(self):
        # A TemporaryDirectory is deleted when cleaned up
        dir = tempfile.mkdtemp()
        try:
            d = self.do_create(dir=dir)
            self.assertTrue(os.path.exists(d.name),
                            "TemporaryDirectory %s does not exist" % d.name)
            d.cleanup()
            self.assertFalse(os.path.exists(d.name),
                        "TemporaryDirectory %s exists after cleanup" % d.name)
        finally:
            os.rmdir(dir)

    def test_del_on_collection(self):
        if garlicsim.__version_info__ <= (0, 6, 2):
            raise nose.SkipTest('Not handling this yet.')
        # A TemporaryDirectory is deleted when garbage collected
        dir = tempfile.mkdtemp()
        try:
            d = self.do_create(dir=dir)
            name = d.name
            del d # Rely on refcounting to invoke __del__
            self.assertFalse(os.path.exists(name),
                        "TemporaryDirectory %s exists after __del__" % name)
        finally:
            os.rmdir(dir)

    @unittest2.expectedFailure # See issue #10188
    def test_del_on_shutdown(self):
        # A TemporaryDirectory may be cleaned up during shutdown
        # Make sure it works with the relevant modules nulled out
        with self.do_create() as dir:
            d = self.do_create(dir=dir)
            # Mimic the nulling out of modules that
            # occurs during system shutdown
            modules = [os, os.path]
            if has_stat:
                modules.append(stat)
            # Currently broken, so suppress the warning
            # that is otherwise emitted on stdout
            with OutputCapturer(stdout=False, stderr=True) as output_capturer:
                with NulledModules(*modules):
                    d.cleanup()
            # Currently broken, so stop spurious exception by
            # indicating the object has already been closed
            d._closed = True
            # And this assert will fail, as expected by the
            # unittest decorator...
            self.assertFalse(os.path.exists(d.name),
                        "TemporaryDirectory %s exists after cleanup" % d.name)

    def test_warnings_on_cleanup(self):
        # Two kinds of warning on shutdown
        #   Issue 10888: may write to stderr if modules are nulled out
        #   ResourceWarning will be triggered by __del__
        with self.do_create() as dir:
            if os.sep != '\\':
                # Embed a backslash in order to make sure string escaping
                # in the displayed error message is dealt with correctly
                suffix = '\\check_backslash_handling'
            else:
                suffix = ''
            d = self.do_create(dir=dir, suf=suffix)

            #Check for the Issue 10888 message
            modules = [os, os.path]
            if has_stat:
                modules.append(stat)
            with OutputCapturer(stdout=False, stderr=True) as output_capturer:
                with NulledModules(*modules):
                    d.cleanup()
            output_capturer
            message = err.getvalue().replace('\\\\', '\\')
            self.assertIn("while cleaning up",  message)
            self.assertIn(d.name,  message)

            # Check for the resource warning
            with support.check_warnings(('Implicitly', ResourceWarning),
                                        quiet=False):
                warnings.filterwarnings("always", category=ResourceWarning)
                d.__del__()
            self.assertFalse(os.path.exists(d.name),
                        "TemporaryDirectory %s exists after __del__" % d.name)

    def test_multiple_close(self):
        # Can be cleaned-up many times without error
        d = self.do_create()
        d.cleanup()
        try:
            d.cleanup()
            d.cleanup()
        except:
            self.failOnException("cleanup")

    def test_context_manager(self):
        # Can be used as a context manager
        d = self.do_create()
        with d as name:
            self.assertTrue(os.path.exists(name))
            self.assertEqual(name, d.name)
        self.assertFalse(os.path.exists(name))
