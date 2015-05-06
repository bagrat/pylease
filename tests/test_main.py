import textwrap
from mock import MagicMock
from nose.tools import eq_, ok_
import pylease
from pylease.command import StatusCommand
from pylease.main import main
from tests import PyleaseTest, MockedSetupPy, CapturedStdout


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
            main(['make', '--dev'])
            expected_version = '0.12.dev1'
            eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            main(['make', '--patch'])
            expected_version = '0.12.1'
            eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            main(['make', '--minor'])
            expected_version = '0.13'
            eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            main(['make', '--major'])
            expected_version = '1.0'
            eq_(setup_py.contents(), setup_py_contents.format(version=expected_version))

    def test_make_command_must_return_error_when_no_version_spec_is_found(self):
        setup_py_contents = textwrap.dedent("""
                                            from setuptools import setup

                                            setup()
                                            """)
        with MockedSetupPy(setup_py_contents, self):
            self.assertRaises(pylease.ex.PyleaseError, main, ['make', '--major'])

    def test_make_command_must_warn_wwhen_more_than_one_version_specs_are_found(self):
        pylease.logme.warn = MagicMock()

        setup_py_contents = textwrap.dedent("""
                                            from setuptools import setup
                                            version='1.0'
                                            setup(version='1.0')
                                            """)
        with MockedSetupPy(setup_py_contents, self):
            main(['make', '--major'])

        ok_(pylease.logme.warn.called)

    # def test_git(self):
    #     setup_py_contents = textwrap.dedent("""
    #                                         from setuptools import setup
    #                                         setup(version='1.0')
    #                                         """)
    #     with MockedSetupPy(setup_py_contents, self):
    #         main(['make', '--major', '--git-tag'])
