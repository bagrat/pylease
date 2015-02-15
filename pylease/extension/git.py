from subprocess import call
from pylease.extension import Extension


class GitExtension(Extension):
    """
    Git extension creates an annotated tag in the git repository named
    v<version>, where version is the current version being released. Also
    makes additional commit containing the updated setup.py.
    """

    def __init__(self, arg_parser):
        super(GitExtension, self).__init__(arg_parser)

        git_group = arg_parser.add_argument_group(title='git arguments')

        git_group.add_argument('--git-tag',
                               action='store_true',
                               dest='use_git',
                               default=False,
                               help='Create a version tag on git')

    def execute(self, args, version):
        super(GitExtension, self).execute(args, version)

        if args.use_git:
            self._make_tag(version)

    @classmethod
    def _make_tag(cls, version):
        call(['git', 'add', 'setup.py'])
        call(['git', 'commit', '-m', 'Prepare release v{version}'.format(
            version=version)])
        call(['git', 'tag', '-a', 'v{version}'.format(version=version)])
