import textwrap
from mock import MagicMock
from nose.tools import eq_, ok_
import pylease
from pylease.command import StatusCommand
from pylease.main import main
from tests import PyleaseTest, MockedSetupPy, CapturedStdout, MockedFile


class CommandLineTest(PyleaseTest):
    def test_status_command_must_show_project_info(self):
        name = 'Some Project'
        version = 'Some Version'

        setup_py = """
                   from setuptools import setup

                   setup(name='{name}', version='{version}')
                   """

        with MockedSetupPy(setup_py.format(name=name, version=version), self):
            with CapturedStdout() as stdout:
                main(['status'])

        eq_(StatusCommand.OUTPUT_FMT.format(name=name, version=version) + '\n', stdout.output)

    def test_make_release_must_update_the_version_correspondingly(self):
        version = '0.12'
        setup_py_contents = textwrap.dedent("""
                                            from setuptools import setup

                                            setup(version='{version}')
                                            """)

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            with MockedFile('setup.cfg', '', self):
                main(['make', '--dev'])
                expected_version = '0.12.dev1'
                eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            with MockedFile('setup.cfg', '', self):
                main(['make', '--patch'])
                expected_version = '0.12.1'
                eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            with MockedFile('setup.cfg', '', self):
                main(['make', '--minor'])
                expected_version = '0.13'
                eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            with MockedFile('setup.cfg', '', self):
                main(['make', '--major'])
                expected_version = '1.0'
                eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

    def test_make_command_must_return_error_when_no_version_spec_is_found(self):
        setup_py_contents = textwrap.dedent("""
                                            from setuptools import setup

                                            setup()
                                            """)
        with MockedSetupPy(setup_py_contents, self):
            ok_(main(['make', '--major']) != 0)

    def test_make_command_must_warn_wwhen_more_than_one_version_specs_are_found(self):
        pylease.LOGME.warn = MagicMock()

        setup_py_contents = textwrap.dedent("""
                                            from setuptools import setup
                                            version='1.0'
                                            setup(version='1.0')
                                            """)

        with MockedSetupPy(setup_py_contents, self):
            with MockedFile('setup.cfg', '', self):
                main(['make', '--major'])

        ok_(pylease.LOGME.warn.called)

    def test_pylease_must_load_configuration_into_pylease_object(self):
        key1 = 'key1'
        key2 = 'key2'
        val1 = 'val1'
        val2 = 'val2'
        contents = textwrap.dedent("""
                [pylease]
                {} = {}
                {} = {}
                   """.format(key1, val1, key2, val2))
        with MockedFile('setup.cfg', contents, self):
            lizy = pylease.Pylease(None, None, None)

            ok_(key1 in lizy.config)
            ok_(key2 in lizy.config)
            eq_(lizy.config[key1], val1)
            eq_(lizy.config[key2], val2)

    def test_make_release_must_update_the_version_in_all_provided_files(self):
        version = '0.12'
        file1_name = 'file1'
        file2_name = 'file2'
        file1_contents = textwrap.dedent("""file1
                                            version='{version}'
                                            """)
        file2_contents = textwrap.dedent("""file2
                                            version='{version}'
                                            """)
        config_contents = textwrap.dedent("""
                                          [pylease]
                                          version-files = {}, {}
                                          """.format(file1_name, file2_name))
        setup_py_contents = textwrap.dedent("""
                                            from setuptools import setup
                                            setup(version='{}')
                                            """.format(version))

        with MockedSetupPy(setup_py_contents, self):
            with MockedFile('setup.cfg', config_contents, self):
                with MockedFile(file1_name, file1_contents.format(version=version), self) as file1:
                    with MockedFile(file2_name, file2_contents.format(version=version), self) as file2:
                        main(['make', '--minor'])
                        expected_version = '0.13'
                        eq_(file1.contents(), file1_contents.format(version=expected_version))
                        eq_(file2.contents(), file2_contents.format(version=expected_version))

    # def test_git(self):
    #     setup_py_contents = textwrap.dedent("""
    #                                         from setuptools import setup
    #                                         setup(version='1.0')
    #                                         """)
    #     with MockedSetupPy(setup_py_contents, self):
    #         main(['make', '--major', '--git-tag'])
