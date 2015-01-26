from unittest import TestCase
from nose.tools import eq_, ok_
from pylease import releasemgmt
from pylease.ex import ReleaseError

__author__ = 'bagrat'


class TestReleaseMgmt(TestCase):

    def test_release(self):
        expected_version = '0.0'

        def get_expected_version():
            return expected_version

        def mock_update_file(version):
            eq_(version, get_expected_version())
        releasemgmt.update_file = mock_update_file

        raises_error = False
        try:
            releasemgmt.release('1.0', 'unknown')
        except ReleaseError:
            raises_error = True

        ok_(raises_error)

        expected_version = '1.2.3.dev4'
        releasemgmt.release('1.2.3.dev3', 'dev')
        expected_version = '1.2.4'
        releasemgmt.release('1.2.3.dev3', 'patch')
        expected_version = '1.3'
        releasemgmt.release('1.2.3.dev3', 'minor')
        expected_version = '2.0'
        releasemgmt.release('1.2.3.dev3', 'major')