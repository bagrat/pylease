import sys
from unittest import TestCase
import shutil

__author__ = 'bagrat'

import mock
import os


class TestError(Exception):
    pass


class PyleaseTest(TestCase):
    MOCK_SUBDIR = os.path.join('tests', 'mock')

    @classmethod
    def setUpClass(cls):
        super(PyleaseTest, cls).setUpClass()

        cwd = os.getcwd()
        cls.mock_path = os.path.join(cwd, cls.MOCK_SUBDIR)

        if os.path.exists(cls.mock_path):
            shutil.rmtree(cls.MOCK_SUBDIR)

        os.makedirs(cls.mock_path)

    @classmethod
    def tearDownClass(cls):
        super(PyleaseTest, cls).tearDownClass()

        shutil.rmtree(cls.MOCK_SUBDIR)


class MockedSetupPy(object):
    def __init__(self, content, test=None, mock_path=None):
        super(MockedSetupPy, self).__init__()

        if not mock_path:
            if not test:
                raise TestError("While mocking setup.py without a mock path, you have to provide the test class.")
            if not isinstance(test, type):
                test = test.__class__
            if not issubclass(test, PyleaseTest):
                raise TestError("While mocking setup.py you have provided '{}' as test class which is not a subclass of PyleaseTest, "
                                "though it is supposed to be.". format(test.__name__))

            mock_path_attr_name = 'mock_path'
            if not hasattr(test, mock_path_attr_name):
                raise TestError("While mocking setup.py you have provided '{}' as test class which does not have '{}' attribute"
                                "though it is supposed to have.". format(test.__name__, mock_path_attr_name))

            mock_path = getattr(test, mock_path_attr_name)

        self._mock_path = mock_path
        self._content = content

    def __enter__(self):
        self._orig = os.getcwd
        os.getcwd = mock.Mock(return_value=self._mock_path)

        sys.path = [os.getcwd()] + sys.path

        setup_py_file = os.path.join(self._mock_path, 'setup.py')
        with open(setup_py_file, 'w') as setup_py_mock:
            setup_py_mock.write(self._content)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.getcwd = self._orig
