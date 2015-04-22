from unittest import TestCase
from nose.tools import ok_, eq_
from pylease.util import SubclassIgnoreMark, get_caller_module


class UtilitiesTest(TestCase):
    def test_subclass_ignore_mark_should_be_true_only_for_marked_class(self):
        class Z(object):
            pass

        class A(Z):
            ignore = SubclassIgnoreMark('A')

        class B(A):
            pass

        class C(B):
            pass

        ok_(A.ignore)
        ok_(not B.ignore)
        ok_(not C.ignore)
        ok_(not hasattr(Z, 'ignore'))

    def test_get_caller_module_must_return_the_module_from_which_the_method_was_called(self):
        module = get_caller_module()

        eq_(module.__name__, 'tests.test_util')

        def wrapper():
            return get_caller_module(1)

        module = wrapper()

        eq_(module.__name__, 'tests.test_util')
