from unittest import TestCase
from nose.tools import eq_, ok_
from pylease import releasemgmt
from pylease.ex import ReleaseError

__author__ = 'bagrat'


class TestReleaseMgmt(TestCase):
    def test_release(self):
        raises_error = False
        try:
            releasemgmt.release('1.0', 'unknown')
        except ReleaseError:
            raises_error = True

        ok_(raises_error)

        expected_version = '1.2.3.dev4'
        eq_(str(releasemgmt.release('1.2.3.dev3', 'dev')), expected_version)

        expected_version = '1.2.4'
        eq_(str(releasemgmt.release('1.2.3.dev3', 'patch')), expected_version)

        expected_version = '1.3'
        eq_(str(releasemgmt.release('1.2.3.dev3', 'minor')), expected_version)

        expected_version = '2.0'
        eq_(str(releasemgmt.release('1.2.3.dev3', 'major')), expected_version)
