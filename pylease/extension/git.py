from pylease.extension import Extension


_default_release_branch = 'master'
_default_development_branch = 'dev'


class GitExtension(Extension):
    def __init__(self, arg_parser):
        super(GitExtension, self).__init__(arg_parser)

    def execute(self):
        super(GitExtension, self).execute()

