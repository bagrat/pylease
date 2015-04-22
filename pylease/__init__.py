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
    def __init__(self, parser, subparser, name, version):
        super(Pylease, self).__init__()

        self.parser = parser
        self.subparser = subparser
        self.version = version
        self.name = name
        self.commands = {}

    def add_command(self, name, command):
        self.commands[name] = command
