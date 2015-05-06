from abc import ABCMeta, abstractmethod
from pylease import logme
from pylease.filemgmt import update_files
from pylease.releasemgmt import release
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
        self.before_tasks = set()
        self.after_tasks = set()

        lizy.add_command(self.name, self)

    @abstractmethod
    def _process_command(self, lizy, args):
        pass  # pragma: no cover

    def __call__(self, args):
        for task in self.before_tasks:
            task(self._lizy, args)

        result = self._process_command(self._lizy, args)

        if result is None or result == 0:
            for task in self.after_tasks:
                task(self._lizy, args)

        return result

    @classmethod
    def init_all(cls, lizy):
        commands = cls.__subclasses__()

        for command in commands:
            command.init_all(lizy)
            if not getattr(command, cls._IGNORE_ME_VAR_NAME):
                command(lizy)

    def add_before_task(self, task):
        self.before_tasks.add(task)

    def add_after_task(self, task):
        self.after_tasks.add(task)


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


class MakeCommand(NamedCommand):
    def __init__(self, lizy):
        super(MakeCommand, self).__init__(lizy, 'Make a release')

        release_group = self.parser.add_argument_group(title='release arguments',
                                                       description='Specify one of those arguments to make the '
                                                       'corresponding level release')

        level_group = release_group.add_mutually_exclusive_group(required=True)
        level_group.add_argument('--major', dest='level', action='store_const', const='major', help='Make a major release')
        level_group.add_argument('--minor', dest='level', action='store_const', const='minor', help='Make a minor release')
        level_group.add_argument('--patch', dest='level', action='store_const', const='patch', help='Make a patch release')
        level_group.add_argument('--dev', dest='level', action='store_const', const='dev', help='Make a dev release')

    def _process_command(self, lizy, args):
        old_version = lizy.info_container.version

        if old_version is None:
            logme.error("Version specification not found!")
            return 1

        level = args.level

        new_version = release(old_version, level)

        counts = update_files(old_version, new_version)

        count = 0
        for version_file in counts:
            count += counts[version_file]

        if count > 1:
            logme.warn("More than one version specification found.")
            logme.debug("Occurrences:")
            for filename in counts:
                logme.debug("\t{filename}: {count}".format(filename=filename, count=counts[filename]))
