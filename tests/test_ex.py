from unittest import TestCase
from nose.tools import eq_
from pylease.ex import VersionRetrievalError


class TestExceptions(TestCase):
    def test_version_retrieval(self):
        ver = 'someversion'

        try:
            raise VersionRetrievalError(ver)
        except VersionRetrievalError as ex:
            eq_(ex.version, ver)
