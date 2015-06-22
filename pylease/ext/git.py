from subprocess import call
import subprocess
from pylease.cmd.rollback import Rollback, Stage
from pylease.ex import PyleaseError
from pylease.cmd.task import AfterTask
from pylease.ext import Extension
from pylease.logger import LOGME as logme  # noqa


class GitExtension(Extension):
    """
    Git extension creates an annotated tag in the git repository named
    v<version>, where version is the current version being released. Also
    makes additional commit containing the updated version files.
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


class GitAfterTask(AfterTask):  # pragma: no cover - Unable to test this other than manually TODO: try to
    # pylint: disable=too-few-public-methods
    TAG_MESSAGE_FMT = 'Prepare release v{version}'

    def execute(self, lizy, args):
        if args.use_git:
            version = self._command_result[self._command.KEY_NEW_VERSION]
            tag_name = 'v{version}'.format(version=version)

            logme.info('Creating git tag %s', tag_name)

            self.enable_rollback(GitRollback(version))

            logme.debug("Staging %s files for commit", lizy.get_version_files())
            proc = subprocess.Popen(['git', 'add'] + lizy.get_version_files(), stderr=subprocess.PIPE)
            proc.wait()
            if proc.returncode:
                err = proc.stderr.read()
                raise PyleaseError(err)

            logme.debug("Committing files %s", lizy.get_version_files())
            proc = subprocess.Popen(['git', 'commit', '-m', self.TAG_MESSAGE_FMT.format(version=version)], stderr=subprocess.PIPE)
            proc.wait()
            if proc.returncode:
                err = proc.stderr.read()
                raise PyleaseError(err)
            self._rollback.enable_stage(GitRollback.COMMIT_STAGE)

            logme.debug("Adding git tag")
            proc = subprocess.Popen(['git', 'tag', '-a', tag_name], stderr=subprocess.PIPE)
            proc.wait()
            if proc.returncode:
                err = proc.stderr.read()
                raise PyleaseError(err)
            self._rollback.enable_stage(GitRollback.TAG_STAGE)


class GitRollback(Rollback):  # pragma: no cover - Unable to test this other than manually TODO: try to test
    COMMIT_STAGE = 'commit'
    TAG_STAGE = 'tag'

    def __init__(self, version):
        super(GitRollback, self).__init__()

        self._version = version

    @Stage(COMMIT_STAGE, 0)
    def rollback_commit(self):
        tag_message = GitAfterTask.TAG_MESSAGE_FMT.format(version=self._version)
        proc = subprocess.Popen('git log -n 1 --grep="{}"  --format="%H"'.format(tag_message), stdout=subprocess.PIPE, shell=True)
        proc.wait()
        release_commit = proc.stdout.read()

        proc = subprocess.Popen('git log -n 2 --format="%H" {}'.format(release_commit), stdout=subprocess.PIPE, shell=True)
        proc.wait()
        pre_release_commit = proc.stdout.read().split('\n')[1]

        proc = subprocess.Popen(['git', 'reset', pre_release_commit])
        proc.wait()

    @Stage(TAG_STAGE, 1)
    def rollback_tag(self):
        call(['git', 'tag', '-d', 'v{version}'.format(version=self._version)])
