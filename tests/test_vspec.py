from unittest import TestCase
from nose.tools import eq_
from pylease.vspec import version

__author__ = 'bagrat'


class Test(TestCase):
    def test_base(self):
        v = 'testversion'
        version(v)

        eq_(version, v)

        # from pylease.vspec import version as anothername
        #
        # anothername(v, var_name='anothername')
        #
        # eq_(anothername, v)
