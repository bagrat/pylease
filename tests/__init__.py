from cStringIO import StringIO
import sys
import textwrap
from unittest import TestCase
import shutil
import __builtin__

__author__ = 'bagrat'

import mock
import os


class TestError(Exception):
    pass


class PyleaseTest(TestCase):
    MOCK_SUBDIR = os.path.join('tests', 'mock')

    def setUp(self):
        super(PyleaseTest, self).setUpClass()

        cwd = os.getcwd()
        self.mock_path = os.path.join(cwd, self.MOCK_SUBDIR)

        if os.path.exists(self.mock_path):
            shutil.rmtree(self.MOCK_SUBDIR)

        os.makedirs(self.mock_path)

    def tearDown(self):
        super(PyleaseTest, self).tearDownClass()

        shutil.rmtree(self.MOCK_SUBDIR)


class MockedFile(object):
    def __init__(self, filename, content, test=None, mock_path=None, for_import=False):
        super(MockedFile, self).__init__()

        if not mock_path:
            if not test:
                raise TestError("While mocking file without a mock path, you have to provide the test class.")
            if not issubclass(test.__class__, PyleaseTest):
                raise TestError("While mocking a file you have provided '{}' as test class which is not a subclass of PyleaseTest, "
                                "though it is supposed to be.". format(test.__name__))

            mock_path_attr_name = 'mock_path'
            if not hasattr(test, mock_path_attr_name):
                raise TestError("While mocking file you have provided '{}' as test class which does not have '{}' attribute, "
                                "though it is supposed to have.". format(test.__name__, mock_path_attr_name))

            mock_path = getattr(test, mock_path_attr_name)

        self._mock_path = mock_path
        self._content = content
        self._filename = filename
        self.mock_file_path = os.path.join(self._mock_path, self._filename)
        self._for_import = for_import
        self._orig_open = None
        self._orig_getcwd = None

    def __enter__(self):
        with open(self.mock_file_path, 'w') as file_mock:
            file_mock.write(self._content)

        self._orig_open = getattr(__builtin__, 'open')
        __builtin__.open = self._open_mock()

        if self._for_import:
            self._orig_getcwd = os.getcwd
            os.getcwd = mock.Mock(return_value=self._mock_path)

            sys.path = [os.getcwd()] + sys.path

            if 'setup' in sys.modules:
                del sys.modules['setup']

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __builtin__.open = self._orig_open

        if self._for_import:
            os.getcwd = self._orig_getcwd

    def contents(self):
        with self._orig_open(self.mock_file_path, 'r') as f:
            return f.read()

    def _open_mock(self):
        mocked_abs_file = os.path.abspath(self._filename)

        def open_mock(filename, *args, **kwargs):
            if self._for_import:
                os.getcwd = self._orig_getcwd
            provided_abs_file = os.path.abspath(filename)
            if self._for_import:
                os.getcwd = mock.Mock(return_value=self._mock_path)

            if mocked_abs_file == provided_abs_file:
                return self._orig_open(self.mock_file_path, *args, **kwargs)
            return self._orig_open(filename, *args, **kwargs)

        return open_mock


class MockedSetupPy(MockedFile):
    FILENAME = 'setup.py'

    def __init__(self, content, test=None, mock_path=None, for_import=True):
        if for_import:
            content = textwrap.dedent(content)

        super(MockedSetupPy, self).__init__(self.FILENAME, content, test, mock_path, for_import)


class CapturedStdout(object):
    def __init__(self):
        super(CapturedStdout, self).__init__()

        self._stdout = None
        self.output = None
        self._stringio = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()

        return self

    def __exit__(self, *args):
        self.output = self._stringio.getvalue()

        sys.stdout = self._stdout
