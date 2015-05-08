from subprocess import call
from pylease.command import AfterTask
from pylease.extension import Extension


class GitExtension(Extension):
    """
    Git extension creates an annotated tag in the git repository named
    v<version>, where version is the current version being released. Also
    makes additional commit containing the updated setup.py.
    """

    def load(self):
        make_command = self._lizy.commands['make']
        parser = make_command.parser

        git_group = parser.add_argument_group(title='git arguments')

        git_group.add_argument('--git-tag',
                               action='store_true',
                               dest='use_git',
                               default=False,
                               help='Create a version tag on git')

        make_command.add_after_task(GitAfterTask(None))


class GitAfterTask(AfterTask):  # pragma: no cover - Unable to test this other than manually TODO: try to test
    def execute(self, lizy, args):
        if args.use_git:
            version = self._command_result[self._command.KEY_NEW_VERSION]
            call(['git', 'add', 'setup.py'])
            call(['git', 'commit', '-m', 'Prepare release v{version}'.format(
                version=version)])
            call(['git', 'tag', '-a', 'v{version}'.format(version=version)])
