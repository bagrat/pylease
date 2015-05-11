import sys
from pylease.logger import LOGME as logme  # noqa
from pylease.command import AfterTask
from pylease.extension import Extension


class PypiExtension(Extension):
    def load(self):
        make_command = self._lizy.commands['make']
        parser = make_command.parser

        pypi_group = parser.add_argument_group(title='PyPI arguments')

        pypi_group.add_argument('--pypi',
                                action='store_true',
                                dest='to_pypi',
                                default=False,
                                help='Upload package to PyPI')

        make_command.add_after_task(PypiAfterTask(rollback))


class PypiAfterTask(AfterTask):  # pragma: no cover - Unable to test this other than manually TODO: try to test
    def execute(self, lizy, args):
        if args.to_pypi:
            self.enable_rollback()

            orig_args = sys.argv
            sys.argv = ['setup.py', 'sdist', 'upload']
            __import__('setup')
            sys.argv = orig_args


def rollback():  # pragma: no cover
    logme.debug('Unable to rollback PyPI upload, please delete the uploaded version manually.')
