import textwrap
from unittest import TestCase
from nose.tools import *
from pylease.ex import VersionSpecError
from pylease.filemgmt import replace_version, update_file

__author__ = 'bagrat'


class Test(TestCase):
    def test_replace_version(self):
        setup_py_tp = textwrap.dedent("""
                                      some line here
                                      and another here

                                      version("{version}")

                                      and the last one
                                      """)

        old_version = '0ld.v3rs10n'
        new_version = 'n3w.v3rs10n'

        old_setup_py = setup_py_tp.format(setup_py_tp, version=old_version)
        new_setup_py = setup_py_tp.format(setup_py_tp, version=new_version)

        replaced_setup_py = replace_version(old_setup_py, new_version)

        eq_(replaced_setup_py, new_setup_py, 'replace_version() must update the version')

    def test_more_than_one_spec(self):
        setup_py_tp = textwrap.dedent("""
                                      some line here
                                      and another here

                                      version("{version}")

                                      and the last one
                                      version("{version}")
                                      """)

        old_version = '0ld.v3rs10n'
        new_version = 'n3w.v3rs10n'

        old_setup_py = setup_py_tp.format(setup_py_tp, version=old_version)
        new_setup_py = setup_py_tp.format(setup_py_tp, version=new_version)

        raises_spec_error = False
        try:
            replaced_setup_py = replace_version(old_setup_py, new_version)
        except VersionSpecError:
            raises_spec_error = True

        ok_(raises_spec_error)

    def test_multiple_vspec(self):
        from pylease import vspec

        class A:
            pass

        vspec.__dict__['A'] = A

        from pylease import filemgmt

        raises_ver_spec_err = False
        try:
            filemgmt._find_version_class_name()
        except VersionSpecError:
            raises_ver_spec_err = True

        ok_(raises_ver_spec_err)

