import sys
from pylease.command.rollback import Rollback, Stage
from pylease.logger import LOGME as logme  # noqa
from pylease.command.task import AfterTask
from pylease.extension import Extension


class PypiExtension(Extension):
    # pylint: disable=too-few-public-methods
    def load(self):
        make_command = self._lizy.commands['make']
        parser = make_command.parser

        pypi_group = parser.add_argument_group(title='PyPI arguments')

        pypi_group.add_argument('--pypi',
                                action='store_true',
                                dest='to_pypi',
                                default=False,
                                help='Upload package to PyPI')

        make_command.add_after_task(PypiAfterTask())


class PypiAfterTask(AfterTask):  # pragma: no cover - Unable to test this other than manually TODO: try to test
    # pylint: disable=too-few-public-methods
    def execute(self, lizy, args):
        # pylint: disable=unused-argument
        if args.to_pypi:
            self.enable_rollback(PypiRollback(sys.argv))

            sys.argv = ['setup.py', 'sdist', 'upload']
            self._rollback.enable_stage(PypiRollback.UPLOADING_STAGE)

            __import__('setup')
            self._rollback.enable_stage(PypiRollback.UPLOADED_STAGE)


class PypiRollback(Rollback):  # pragma: no cover
    UPLOADED_STAGE = 'uploaded'
    UPLOADING_STAGE = 'uploading'

    def __init__(self, orig_args):
        super(PypiRollback, self).__init__()

        self._orig_args = orig_args

    @Stage(UPLOADING_STAGE)
    def rollback_args(self):
        sys.argv = self._orig_args

    @Stage(UPLOADED_STAGE)
    def rollback_inform(self):
        # pylint: disable=no-self-use
        logme.warn('Unable to rollback PyPI upload, please delete the uploaded version manually.')
