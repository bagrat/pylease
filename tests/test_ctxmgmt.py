from mock import Mock, MagicMock
from nose.tools import ok_

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

    def test_caution_context_manager_must_rollback_everything_if_error_occurs(self):
        rb1 = MagicMock()
        rb2 = MagicMock()
        rb3 = MagicMock()

        with Caution() as caution:
            caution.add_rollback(rb1)
            caution.add_rollback(rb2)

            raise Exception()

        rb1.assert_called_once_with()
        rb2.assert_called_once_with()
        ok_(not rb3.called)

    def test_caution_context_manager_should_leave_everythin_as_is_if_no_error_occurs(self):
        rb1 = MagicMock()

        with Caution() as caution:
            caution.add_rollback(rb1)

        ok_(not rb1.called)
