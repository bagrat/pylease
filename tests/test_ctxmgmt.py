from unittest import TestCase
from nose.tools import eq_, ok_
import sys
from pylease.ctxmgmt import ReplacedSetup, Caution


class Test(TestCase):
    def test_replaced_setup(self):
        expected_version = 'expected'

        def callback(actual_version):
            eq_(expected_version, actual_version, "The ReplacedSetup must call the callback with the right value")

        with ReplacedSetup(callback):
            from setuptools import setup
            setup(version=expected_version)

    class Dummy():
            pass

    def test_caution(self):
        exit_code = 123

        def exiting_method():
            sys.exit(exit_code)


        obj = self.Dummy()  # Just an object that has __dict__
        attr = "someattr"
        val = "someval"

        raises_error = False
        try:
            with Caution(Rollback(obj, attr, val)):
                exiting_method()
        except SystemExit as ex:
            raises_error = True
            eq_(ex.code, exit_code)

        ok_(raises_error)
        eq_(getattr(obj, attr), val)

    def test_caution_no_exit(self):
        obj = self.Dummy()
        attr = "someattr"
        val = "someval"

        raises_error = False
        try:
            with Caution(Rollback(obj, attr, val)):
                pass
        except Exception:
            raises_error = True

        ok_(not raises_error)
        ok_(not hasattr(obj, attr))


class Rollback(object):
    def __init__(self, obj, attr, val):
        super(Rollback, self).__init__()

        self.obj = obj
        self.attr = attr
        self.val = val

    def rollback(self):
        setattr(self.obj, self.attr, self.val)