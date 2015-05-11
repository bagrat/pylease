from subprocess import call
import subprocess
from pylease.ex import PyleaseError
from pylease.command.task import AfterTask
from pylease.extension import Extension
from pylease.logger import LOGME as logme  # noqa


class GitExtension(Extension):
    """
    Git extension creates an annotated tag in the git repository named
    v<version>, where version is the current version being released. Also
    makes additional commit containing the updated setup.py.
    """
    # pylint: disable=too-few-public-methods
    # The number of public methods is reasonable for this kind of class
    def load(self):
        make_command = self._lizy.commands['make']
        parser = make_command.parser

        git_group = parser.add_argument_group(title='git arguments')

        git_group.add_argument('--git-tag',
                               action='store_true',
                               dest='use_git',
                               default=False,
                               help='Create a version tag on git')

        make_command.add_after_task(GitAfterTask())


class GitAfterTask(AfterTask):  # pragma: no cover - Unable to test this other than manually TODO: try to test
    def execute(self, lizy, args):
        if args.use_git:
            version = self._command_result[self._command.KEY_NEW_VERSION]
            tag_name = 'v{version}'.format(version=version)

            logme.info('Creating git tag {}'.format(tag_name))

            self.enable_rollback(GitRollback(version).rollback)

            logme.debug("Staging {} files for commit".format(lizy.get_version_files()))
            proc = subprocess.Popen(['git', 'add'] + lizy.get_version_files(), stderr=subprocess.PIPE)
            proc.wait()
            if proc.returncode:
                err = proc.stderr.read()
                print(err)
                raise PyleaseError(err)

            logme.debug("Committing files {}".format(lizy.get_version_files()))
            proc = subprocess.Popen(['git', 'commit', '-m', 'Prepare release v{version}'.format(version=version)], stderr=subprocess.PIPE)
            proc.wait()
            if proc.returncode:
                err = proc.stderr.read()
                raise PyleaseError(err)
            self._rollback.commit_done = True

            logme.debug("Adding git tag")
            proc = subprocess.Popen(['git', 'tag', '-a', tag_name], stderr=subprocess.PIPE)
            proc.wait()
            if proc.returncode:
                err = proc.stderr.read()
                raise PyleaseError(err)
            self._rollback.tag_done = True

            raise Exception()


class GitRollback(object):  # pragma: no cover - Unable to test this other than manually TODO: try to test
    def __init__(self, version):
        super(GitRollback, self).__init__()

        self._version = version
        self.commit_done = False
        self.tag_done = False

    def rollback(self):
        if self.commit_done:
            pass

        if self.tag_done:
            call(['git', 'tag', '-d', 'v{version}'.format(version=self._version)])
