from nose.tools import eq_
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
        version = '0.1'
        setup_py_contents = """
                   from setuptools import setup

                   setup(version='{version}')
                   """

        with MockedSetupPy(setup_py_contents.format(version=version), self) as setup_py:
            main(['make', '--dev'])

        print(setup_py.contents())
