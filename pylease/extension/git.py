from subprocess import call
from pylease.extension import Extension


class GitExtension(Extension):
    _default_release_branch = 'master'

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

    def _make_tag(self, version):
        call(['git', 'add', 'setup.py'])
        call(['git', 'commit', '-m', 'Prepare release v{version}'.format(
            version=version)])
        call(['git', 'tag', '-a', 'v{version}'.format(version=version)])
