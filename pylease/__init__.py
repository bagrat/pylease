import ConfigParser
from pylease.logger import LOGME as logme
import os

__version__ = '0.2'


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
            logme.warn('No pylease section found in setup.cfg')

        self.config = config

        self._load_extensions()

    def add_command(self, name, command):
        self.commands[name] = command

    def execute_command(self, name, args):
        return self.commands[name](args)

    def add_subparser(self, *args, **kwargs):
        return self.cmd_subparsers.add_parser(*args, **kwargs)

    def _get_config_list_value(self, key):
        values = None
        if key in self.config:
            values_str_list = self.config[key].replace(' ', '')
            values = values_str_list.split(',')

        return values

    def get_version_files(self):
        return self._get_config_list_value('version-files')

    def _load_extensions(self):
        extension_packages = self._get_config_list_value('use-plugins') or []

        for package in extension_packages:
            __import__(package)
