# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Tests taken from Python's `contextlib'.'''

import sys

import nose
from python_toolbox.third_party import unittest2

import python_toolbox
from python_toolbox.context_management import (ContextManager,
                                                    ContextManagerType)


class ContextManagerTestCase(unittest2.TestCase):

    def test_contextmanager_plain(self):
        state = []
        @ContextManagerType
        def woohoo():
            state.append(1)
            yield 42
            state.append(999)
        with woohoo() as x:
            self.assertEqual(state, [1])
            self.assertEqual(x, 42)
            state.append(x)
        self.assertEqual(state, [1, 42, 999])

    def test_contextmanager_finally(self):
        state = []
        @ContextManagerType
        def woohoo():
            state.append(1)
            try:
                yield 42
            finally:
                state.append(999)
        with self.assertRaises(ZeroDivisionError):
            with woohoo() as x:
                self.assertEqual(state, [1])
                self.assertEqual(x, 42)
                state.append(x)
                raise ZeroDivisionError()
        self.assertEqual(state, [1, 42, 999])

    def test_contextmanager_no_reraise(self):
        @ContextManagerType
        def whee():
            yield
        ctx = whee()
        ctx.__enter__()
        # Calling __exit__ should not result in an exception
        self.assertFalse(ctx.__exit__(TypeError, TypeError("foo"), None))

    def test_contextmanager_trap_yield_after_throw(self):
        @ContextManagerType
        def whoo():
            try:
                yield
            except:
                yield
        ctx = whoo()
        ctx.__enter__()
        self.assertRaises(
            RuntimeError, ctx.__exit__, TypeError, TypeError("foo"), None
        )

    #def test_contextmanager_except(self):
        #state = []
        #@ContextManagerType
        #def woohoo():
            #state.append(1)
            #try:
                #yield 42
            #except ZeroDivisionError as e:
                #state.append(e.args[0])
                #self.assertEqual(state, [1, 42, ZeroDivisionError(999)])
        #with woohoo() as x:
            #self.assertEqual(state, [1])
            #self.assertEqual(x, 42)
            #state.append(x)
            #raise ZeroDivisionError(999)
        #self.assertEqual(state, [1, 42, 999])

    def _create_contextmanager_attribs(self):
        raise nose.SkipTest
        def attribs(**kw):
            def decorate(func):
                for k,v in kw.items():
                    setattr(func,k,v)
                return func
            return decorate
        @ContextManagerType
        @attribs(foo='bar')
        def baz(spam):
            """Whee!"""
        return baz

    def test_contextmanager_attribs(self):
        baz = self._create_contextmanager_attribs()
        self.assertEqual(baz.__name__,'baz')
        self.assertEqual(baz.foo, 'bar')

    @unittest2.skipIf(hasattr(sys, 'flags') and sys.flags.optimize >= 2,
                      "Docstrings are omitted with -O2 and above")
    def test_contextmanager_doc_attrib(self):
        raise nose.SkipTest('Not sure what to do about this.')
        baz = self._create_contextmanager_attribs()
        self.assertEqual(baz.__doc__, "Whee!")


class MyContextManager(ContextManager):
    started = False
    exc = None
    catch = False

    def __enter__(self):
        self.started = True
        return self

    def __exit__(self, *exc):
        self.exc = exc
        return self.catch


class TestContextDecorator(unittest2.TestCase):

    def test_contextdecorator(self):
        context = MyContextManager()
        with context as result:
            self.assertIs(result, context)
            self.assertTrue(context.started)

        self.assertEqual(context.exc, (None, None, None))


    def test_contextdecorator_with_exception(self):
        context = MyContextManager()

        def f():
            with context:
                raise NameError('foo')
        self.assertRaises(NameError, f)
        self.assertIsNotNone(context.exc)
        self.assertIs(context.exc[0], NameError)

        context = MyContextManager()
        context.catch = True
        with context:
            raise NameError('foo')
        self.assertIsNotNone(context.exc)
        self.assertIs(context.exc[0], NameError)


    def test_decorator(self):
        context = MyContextManager()

        @context
        def test():
            self.assertIsNone(context.exc)
            self.assertTrue(context.started)
        test()
        self.assertEqual(context.exc, (None, None, None))


    def test_decorator_with_exception(self):
        context = MyContextManager()

        @context
        def test():
            self.assertIsNone(context.exc)
            self.assertTrue(context.started)
            raise NameError('foo')

        self.assertRaises(NameError, test)
        self.assertIsNotNone(context.exc)
        self.assertIs(context.exc[0], NameError)


    def test_decorating_method(self):
        context = MyContextManager()

        class Test(object):

            @context
            def method(self, a, b, c=None):
                self.a = a
                self.b = b
                self.c = c

        # these tests are for argument passing when used as a decorator
        test = Test()
        test.method(1, 2)
        self.assertEqual(test.a, 1)
        self.assertEqual(test.b, 2)
        self.assertEqual(test.c, None)

        test = Test()
        test.method('a', 'b', 'c')
        self.assertEqual(test.a, 'a')
        self.assertEqual(test.b, 'b')
        self.assertEqual(test.c, 'c')

        test = Test()
        test.method(a=1, b=2)
        self.assertEqual(test.a, 1)
        self.assertEqual(test.b, 2)


    def test_typo_enter(self):
        raise nose.SkipTest
        class MyContextManager(ContextManager):
            def __unter__(self):
                pass
            def __exit__(self, *exc):
                pass

        with self.assertRaises(AttributeError):
            with MyContextManager():
                pass


    def test_typo_exit(self):
        raise nose.SkipTest
        class MyContextManager(ContextManager):
            def __enter__(self):
                pass
            def __uxit__(self, *exc):
                pass

        with self.assertRaises(AttributeError):
            with MyContextManager():
                pass


    def test_contextdecorator_as_mixin(self):
        
        class somecontext(object):
            started = False
            exc = None

            def __enter__(self):
                self.started = True
                return self

            def __exit__(self, *exc):
                self.exc = exc

        class MyContextManager(somecontext, ContextManager):
            pass

        context = MyContextManager()
        @context
        def test():
            self.assertIsNone(context.exc)
            self.assertTrue(context.started)
        test()
        self.assertEqual(context.exc, (None, None, None))


    def test_contextmanager_as_decorator(self):
        state = []
        @ContextManagerType
        def woohoo(y):
            state.append(y)
            yield
            state.append(999)

        @woohoo(1)
        def test(x):
            self.assertEqual(state, [1])
            state.append(x)
        test('something')
        self.assertEqual(state, [1, 'something', 999])


