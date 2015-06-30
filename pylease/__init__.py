import ConfigParser
from pylease.logger import LOGME as logme  # noqa
import os

import pylease.cmd
import pylease.ext

__version__ = '0.2'


class Pylease(object):
    """
    The main class of Pylease, which contains all the needed resources for extensions. This class is initialised once and by Pylease,
    which is the so called ``lizy`` object. It is passed to :class:`~pylease.cmd.Command` and :class:`~pylease.ext.Extension` instances.

    Attributes:
        info_container (pylease.InfoContainer): Contains information about current status of the project. Minimal information is
            ``name`` and ``version``.
        commands (dict): A dictionary of Pylease commands, including commands defined in extensions if any. The values of the dictionary
            are instances of :class:`~pylease.cmd.Command` class.
        parser (argparse.ArgumentParser): The root parser of Pylease. Use this object to add command line arguments to Pylease on the
            same level as ``--version`` and ``--help``.
        config (dict): A dictionary representing the configuration parsed from ``setup.cfg`` defined under ``[pylease]`` section. If a
            configuration value in the configuration file is defined as ``key1 = valA, valB, valC`` then the value of the ``key1`` key of
            this attribute will be an instance of :class:`~list` and be equal to ``['valA', 'valB, 'valC']``.
    """
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

    def get_plugins(self):
        return self._get_config_list_value('use-plugins') or []

    def _load_extensions(self):
        extension_packages = self.get_plugins()

        for package in extension_packages:
            __import__(package)


class InfoContainer(object):
    # pylint: disable=too-few-public-methods
    """
    A simple container that maps a provided dictionary to its attributes. This provides the current status of the project,
    and the minimal built-in information attributes are the following:

    Attributes:
        name (str): The name of the project.
        version (str): The current versin of the project
        is_empty (bool): The status of current working directory, i.e. indicates whether it is empty or not.
    """
    def __init__(self):
        super(InfoContainer, self).__init__()

        self.name = None
        self.version = None
        self.is_empty = False

    def set_info(self, **kwargs):
        """
        Used to extend the information about the project.

        Example:
            Below are two options on how to use/extend the ``InfoContainer``::

                info = InfoContainer()

                # Option 1
                info.set_info(info1='value2', info2='value2')

                # Option 2
                more_info = {'info3': 'value3'}
                info.set_info(**more_info)

                # Then you can access your info as instance attributes
                print(info.info2)  # will print 'value2'

        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
