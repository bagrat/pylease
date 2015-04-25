import textwrap
from nose.tools import eq_
from pylease.filemgmt import replace_version, update_files, VersionRollback
from tests import PyleaseTest, MockedFile, MockedSetupPy

__author__ = 'bagrat'


class FileManagementTest(PyleaseTest):
    def test_replace_version_must_replace_a_version_specification_in_the_provided_string(self):
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

    def test_replace_version_must_return_the_number_of_occurrences_of_version_specifications(self):
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

    def test_Replace_version_must_return_zero_occurrences_if_no_version_specification_found(self):
        setup_py_tp = textwrap.dedent("""
                                      some line here
                                      and another here

                                      and the last one
                                      """)

        non_existing_text = "some text that does not appear in setup_py"

        _, count = replace_version(setup_py_tp, non_existing_text, 'does not matter')

        eq_(count, 0)

    def test_update_files_must_update_version_in_provided_files(self):
        old_version = 'old_version'
        new_version = 'new_version'

        file_contents = textwrap.dedent("""
                        line one
                        version = {}
                        """)

        old_contents = file_contents.format(old_version)
        expected_contents = file_contents.format(new_version)

        filename = 'some_file'

        with MockedFile(filename, old_contents, self) as mocked_file:
            update_files(old_version, new_version, [filename])

            new_contents = mocked_file.contents()

            eq_(expected_contents, new_contents)

        with MockedSetupPy(old_contents, self, for_import=False) as setup_py_mock:
            update_files(old_version, new_version)

            new_contents = setup_py_mock.contents()

            eq_(expected_contents, new_contents)

    def test_update_files_must_update_version_in_setuppy_if_no_files_are_provided(self):
        old_version = 'old_version'
        new_version = 'new_version'

        file_contents = textwrap.dedent("""
                        line one
                        version = {}
                        """)

        old_contents = file_contents.format(old_version)
        expected_contents = file_contents.format(new_version)

        with MockedSetupPy(old_contents, self, for_import=False) as setup_py_mock:
            update_files(old_version, new_version)

            new_contents = setup_py_mock.contents()

            eq_(expected_contents, new_contents)

    def test_version_rollback_must_reset_the_old_version(self):
        old_version = 'old_version'
        new_version = 'new_version'

        file_contents = textwrap.dedent("""
                        line one
                        version = {}
                        """)

        current_contents = file_contents.format(new_version)
        expected_contents = file_contents.format(old_version)

        with MockedSetupPy(current_contents, self, for_import=False) as setup_py:
            rollback = VersionRollback(old_version, new_version)

            rollback.rollback()

            new_contents = setup_py.contents()

            eq_(expected_contents, new_contents)
