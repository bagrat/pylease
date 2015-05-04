import logging

__author__ = 'bagrat'
__version__ = '0.2'

_LOGGING_FMT = "%(levelname)s: %(message)s"

logme = logging.getLogger(__name__)
logme.setLevel(logging.ERROR)

handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
handler.setFormatter(logging.Formatter(fmt=_LOGGING_FMT))

logme.addHandler(handler)


class Pylease(object):
    def __init__(self, parser, cmd_subparsers, info_container):
        super(Pylease, self).__init__()

        self.parser = parser
        self.cmd_subparsers = cmd_subparsers
        self.info_container = info_container
        self.commands = {}

    def add_command(self, name, command):
        self.commands[name] = command

    def execute_command(self, name, args):
        self.commands[name](args)

    def add_subparser(self, *args, **kwargs):
        return self.cmd_subparsers.add_parser(*args, **kwargs)
