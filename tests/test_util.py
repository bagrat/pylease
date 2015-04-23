from unittest import TestCase
from nose.tools import ok_, eq_
from pylease.util import get_caller_module, ignore_subclass, IgnoreSubclass


class UtilitiesTest(TestCase):
    def test_subclass_ignore_mark_should_be_true_only_for_marked_class(self):
        class Z(object):
            pass

        @ignore_subclass
        class A1(Z):
            pass

        class B1(A1):
            pass

        class C1(B1):
            pass

        ok_(A1.ignore)
        ok_(not B1.ignore)
        ok_(not C1.ignore)
        ok_(not hasattr(Z, IgnoreSubclass.DEFAULT_MARK_NAME))

        ignore_mark_name = 'ignore_mark'

        @IgnoreSubclass(ignore_mark_name)
        class A2(Z):
            pass

        class B2(A2):
            pass

        class C2(B2):
            pass

        ok_(getattr(A2, ignore_mark_name))
        ok_(not getattr(B2, ignore_mark_name))
        ok_(not getattr(C2, ignore_mark_name))
        ok_(not hasattr(Z, ignore_mark_name))

    def test_get_caller_module_must_return_the_module_from_which_the_method_was_called(self):
        module = get_caller_module()

        eq_(module.__name__, 'tests.test_util')

        def wrapper():
            return get_caller_module(1)

        module = wrapper()

        eq_(module.__name__, 'tests.test_util')
