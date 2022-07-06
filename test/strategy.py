import unittest

from mod_hooking.strategy import after, override


class TestStrategy(unittest.TestCase):
    def test_two_hooks_on_same_method(self):
        class Foo(object):
            def foo(self):
                pass

        @after(Foo, "foo")
        def first_hook(_, foo):
            self.assertIsInstance(foo, Foo)

        @after(Foo, "foo")
        def second_hook(_, foo):
            self.assertIsInstance(foo, Foo)

        Foo().foo()
