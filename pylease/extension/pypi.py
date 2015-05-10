import sys
from pylease import LOGME as logme
from pylease.command import AfterTask
from pylease.extension import Extension


class PypiExtension(Extension):
    def load(self):
        logme.info('loading pypi')
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
            logme.info('Uploading to PyPI')
            logme.info(sys.argv)
            orig_args = sys.argv
            sys.argv = ['setup.py', 'sdist', 'upload']
            __import__('setup')
            sys.argv = orig_args


def rollback():  # pragma: no cover
    logme.info('Unable to rollback PyPI upload, please delete the uploaded version manually.')
