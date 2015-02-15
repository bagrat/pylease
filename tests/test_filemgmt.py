import textwrap
from unittest import TestCase
from nose.tools import ok_, eq_
from pylease.ex import VersionSpecError
from pylease.filemgmt import replace_version

__author__ = 'bagrat'


class Test(TestCase):
    def test_replace_version(self):
        setup_py_tp = textwrap.dedent("""
                                      some line here
                                      and another here

                                      version = "{version}"

                                      and the last one
                                      """)

        old_version = '0ld.v3rs10n'
        new_version = 'n3w.v3rs10n'

        old_setup_py = setup_py_tp.format(setup_py_tp, version=old_version)
        expected_new_setup_py = setup_py_tp.format(setup_py_tp, version=new_version)

        actual_new_setup_py, _ = replace_version(old_setup_py, old_version, new_version)

        eq_(actual_new_setup_py, expected_new_setup_py, 'replace_version() must update the version')

    def test_more_than_one_spec(self):
        setup_py_tp = textwrap.dedent("""
                                      some line here
                                      and another here

                                      version = "{version}"

                                      and the last one
                                      version = "{version}"
                                      """)

        old_version = '0ld.v3rs10n'
        new_version = 'n3w.v3rs10n'

        old_setup_py = setup_py_tp.format(setup_py_tp, version=old_version)
        expected_new_setup_py = setup_py_tp.format(setup_py_tp, version=new_version)
        expected_count = 2

        actual_new_setup_py, actual_count = replace_version(old_setup_py, old_version, new_version)

        eq_(expected_new_setup_py, actual_new_setup_py, "replace_version() must update version")
        eq_(expected_count, actual_count, "replace_version() must return correct number of occurrences")

    def test_no_version_spec(self):
        setup_py_tp = textwrap.dedent("""
                                      some line here
                                      and another here

                                      and the last one
                                      """)

        non_existing_text = "some text that does not appear in setup_py"

        _, count = replace_version(setup_py_tp, non_existing_text, 'does not matter')

        eq_(count, 0)
