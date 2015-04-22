from abc import ABCMeta, abstractmethod
from pylease.util import SubclassIgnoreMark


class Command(object):
    __metaclass__ = ABCMeta

    _IGNORE_ME_VAR_NAME = 'ignore_me'
    ignore_me = False

    def __init__(self, lizy):
        super(Command, self).__init__()

        lizy.add_command(self.name, self)

        self._lizy = lizy

    @abstractmethod
    def _process_command(self, lizy, args):
        pass  # pragma: no cover

    @abstractmethod
    def _get_name(self):
        pass  # pragma: no cover

    @property
    def name(self):
        return self._get_name()

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

    def __init__(self, lizy):
        my_name = self.__class__.__name__
        self._name = my_name[:-(len(self._SUFFIX))].lower()

        super(NamedCommand, self).__init__(lizy)

    def _get_name(self):
        return self._name


# class StatusCommand(Command):
#     def __init__(self, lizy):
#         super(StatusCommand, self).__init__(lizy)
#
#         status_parser = lizy.subparser.add_parser('status', help='Retrieve current status of the project')
#
#     def _name(self):
#         return "status"
#
#     def _process_command(self, lizy, args):
#         print(lizy.name + " " + lizy.version)
