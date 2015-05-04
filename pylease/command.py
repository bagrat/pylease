from abc import ABCMeta, abstractmethod
from pylease.util import SubclassIgnoreMark


class Command(object):
    __metaclass__ = ABCMeta

    _IGNORE_ME_VAR_NAME = 'ignore_me'
    ignore_me = False

    def __init__(self, lizy, name, description):
        super(Command, self).__init__()

        self.name = name
        self.description = description
        self.parser = lizy.add_subparser(self.name, help=self.description)
        self._lizy = lizy

        lizy.add_command(self.name, self)

    @abstractmethod
    def _process_command(self, lizy, args):
        pass  # pragma: no cover

    def __call__(self, args):
        self._process_command(self._lizy, args)

    @classmethod
    def init_all(cls, lizy):
        commands = cls.__subclasses__()

        for command in commands:
            command.init_all(lizy)
            if not getattr(command, cls._IGNORE_ME_VAR_NAME):
                command(lizy)


class NamedCommand(Command):
    _SUFFIX = "Command"
    ignore_me = SubclassIgnoreMark('NamedCommand')

    def __init__(self, lizy, description):
        my_name = self.__class__.__name__
        name = my_name[:-(len(self._SUFFIX))].lower()

        super(NamedCommand, self).__init__(lizy, name, description)


class StatusCommand(NamedCommand):
    OUTPUT_FMT = 'Project Name: {name}\nCurrent Version: {version}'

    def __init__(self, lizy):
        super(StatusCommand, self).__init__(lizy, 'Retrieve current status of the project')

    def _process_command(self, lizy, args):
        print(self.OUTPUT_FMT.format(name=lizy.info_container.name, version=lizy.info_container.version))
