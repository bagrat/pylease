from unittest import TestCase
import sys

__author__ = 'bagrat'

import mock
import os


class MockSetupPy(object):
    def __init__(self):
        super(MockSetupPy, self).__init__()

    def __enter__(self):
        cwd = os.getcwd()
        path = os.path.join(cwd, 'tests/static')
        self._orig = os.getcwd
        os.getcwd = mock.Mock(return_value=path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.getcwd = self._orig
