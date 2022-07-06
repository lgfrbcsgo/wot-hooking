import unittest

from mod_hooking.hooking import Hook, unhook


class TestHooking(unittest.TestCase):
    def test_bound_hook(self):
        class Foo(object):
            def foo(self):
                pass

        def strategy(_, __, foo):
            self.assertIsInstance(foo, Foo)

        Foo.foo = Hook(strategy, Foo.foo, lambda: 42)

        Foo().foo()

    def test_chained_hooks(self):
        class Foo(object):
            def foo(self):
                pass

        def record_strategy(orig_func, func, *args, **kwargs):
            func(*args, **kwargs)
            return orig_func(*args, **kwargs)

        def func1(*args, **kwargs):
            called[func1.__name__] = True

        def func2(*args, **kwargs):
            called[func2.__name__] = True

        called = {
            func1.__name__: False,
            func2.__name__: False,
        }

        Foo.foo = Hook(record_strategy, Hook(record_strategy, Foo.foo, func2), func1)

        Foo().foo()

        self.assertDictEqual(called, {func1.__name__: True, func2.__name__: True})

    def test_unhook_func1(self):
        class Foo(object):
            def foo(self):
                pass

        def record_strategy(orig_func, func, *args, **kwargs):
            func(*args, **kwargs)
            return orig_func(*args, **kwargs)

        def func1(*args, **kwargs):
            called[func1.__name__] = True

        def func2(*args, **kwargs):
            called[func2.__name__] = True

        called = {
            func1.__name__: False,
            func2.__name__: False,
        }

        Foo.foo = Hook(record_strategy, Hook(record_strategy, Foo.foo, func2), func1)

        unhook(Foo, "foo", None, func1)

        Foo().foo()

        self.assertDictEqual(called, {func1.__name__: False, func2.__name__: True})

    def test_unhook_func2(self):
        class Foo(object):
            def foo(self):
                pass

        def before(orig_func, func, *args, **kwargs):
            func(*args, **kwargs)
            return orig_func(*args, **kwargs)

        def func1(*args, **kwargs):
            called[func1.__name__] = True

        def func2(*args, **kwargs):
            called[func2.__name__] = True

        called = {
            func1.__name__: False,
            func2.__name__: False,
        }

        Foo.foo = Hook(before, Hook(before, Foo.foo, func2), func1)

        unhook(Foo, "foo", None, func2)

        Foo().foo()

        self.assertDictEqual(called, {func1.__name__: True, func2.__name__: False})

    def test_unhook_before(self):
        class Foo(object):
            def foo(self):
                pass

        def before(orig_func, func, *args, **kwargs):
            func(*args, **kwargs)
            return orig_func(*args, **kwargs)

        def func1(*args, **kwargs):
            called[func1.__name__] = True

        def func2(*args, **kwargs):
            called[func2.__name__] = True

        called = {
            func1.__name__: False,
            func2.__name__: False,
        }

        Foo.foo = Hook(before, Hook(before, Foo.foo, func2), func1)

        unhook(Foo, "foo", before)

        Foo().foo()

        self.assertDictEqual(called, {func1.__name__: False, func2.__name__: False})
