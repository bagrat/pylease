import ConfigParser
import logging
import os

__author__ = 'bagrat'
__version__ = '0.2'

_LOGGING_FMT = "%(levelname)s: %(message)s"

LOGME = logging.getLogger(__name__)
LOGME.setLevel(logging.ERROR)

HANDLER = logging.StreamHandler()
HANDLER.setLevel(logging.ERROR)
HANDLER.setFormatter(logging.Formatter(fmt=_LOGGING_FMT))

LOGME.addHandler(HANDLER)


class Pylease(object):
    def __init__(self, parser, cmd_subparsers, info_container):
        super(Pylease, self).__init__()

        self.parser = parser
        self.cmd_subparsers = cmd_subparsers
        self.info_container = info_container
        self.commands = {}

        config = {}
        config_parser = ConfigParser.SafeConfigParser()
        try:
            if os.path.exists('setup.cfg'):
                config_parser.read('setup.cfg')
                items = config_parser.items('pylease')
                for item in items:
                    config[item[0]] = item[1]
        except ConfigParser.NoSectionError:
            LOGME.warn('No pylease section found in setup.cfg')

        self.confg = config

    def add_command(self, name, command):
        self.commands[name] = command

    def execute_command(self, name, args):
        return self.commands[name](args)

    def add_subparser(self, *args, **kwargs):
        return self.cmd_subparsers.add_parser(*args, **kwargs)
