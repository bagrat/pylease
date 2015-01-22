from unittest import TestCase
from nose.tools import eq_, ok_
from pylease.vermgmt import DevedVersion

__author__ = 'bagrat'


class Test(TestCase):
    def test_deved_version(self):
        ver = DevedVersion('1.1')

        eq_(ver.version, (1, 1, 0))

        ver = DevedVersion('1.2dev45')

        eq_(ver.version, (1, 2, 0))
        eq_(ver.dev, 45)

        ver = DevedVersion('2.3.1dev78')

        eq_(str(ver), '2.3.1dev78')

        ver = DevedVersion('1.2.3dev4')

        ver.increase_major()
        ver.increase_minor()
        ver.increase_patch()
        ver.increase_dev()

        eq_(str(ver), '2.3.4dev5')

        raises_value_error = False
        try:
            DevedVersion('wrongversion')
        except ValueError:
            raises_value_error = True

        ok_(raises_value_error)
