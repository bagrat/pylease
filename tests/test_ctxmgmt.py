from mock import Mock
from nose.tools import eq_, ok_
import sys

from pylease.ctxmgmt import Caution, ReplacedSetup
from tests import PyleaseTest, MockedSetupPy


class ContextManagersTest(PyleaseTest):
    def test_replaced_setup_must_replace_the_setuptools_setup_with_provided_callback(self):
        key1 = 'key1'
        val1 = 'val1'
        key2 = 'key2'
        val2 = 'val2'

        kwargs = {key1: val1, key2: val2}
        setup_py = """
                   from setuptools import setup

                   kwargs = {{'{}': '{key1}', '{}': '{key2}'}}
                   setup(**kwargs)
                   """. format(key1, key2, **kwargs)

        callback = Mock()

        with ReplacedSetup(callback):
            with MockedSetupPy(setup_py, self):
                __import__('setup')

            callback.assert_called_once_with(**kwargs)

    class Dummy():
            pass

    def test_caution_context_manager_must_rollback_everything_if_error_occurs(self):
        exit_code = 123

        def exiting_method():
            sys.exit(exit_code)

        obj = self.Dummy()  # Just an object that has __dict__
        attr = "someattr"
        val = "someval"

        raises_error = False
        try:
            with Caution(self.Rollback(obj, attr, val)):
                exiting_method()
        except SystemExit as ex:
            raises_error = True
            eq_(ex.code, exit_code)

        ok_(raises_error)
        eq_(getattr(obj, attr), val)

    def test_caution_context_manager_should_leave_everythin_as_is_if_no_error_occurs(self):
        obj = self.Dummy()
        attr = "someattr"
        val = "someval"

        raises_error = False
        try:
            with Caution(self.Rollback(obj, attr, val)):
                pass
        except Exception:
            raises_error = True

        ok_(not raises_error)
        ok_(not hasattr(obj, attr))

    class Rollback(object):
        def __init__(self, obj, attr, val):
            super(ContextManagersTest.Rollback, self).__init__()

            self.obj = obj
            self.attr = attr
            self.val = val

        def rollback(self):
            setattr(self.obj, self.attr, self.val)
