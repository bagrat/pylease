from __future__ import print_function
from abc import ABCMeta, abstractmethod

from pylease.logger import LOGME as logme  # noqa
from pylease.ctxmgmt import Caution
from pylease.ex import PyleaseError
from pylease.filemgmt import update_files, VersionRollback
from pylease.releasemgmt import release
from pylease.util import SubclassIgnoreMark


class Command(object):
    # pylint: disable=no-self-use, too-many-instance-attributes
    # The whole logic of Pylease is centralized on the Command class,
    # thus it is reasonable to have more than seven instance attributes.

    __metaclass__ = ABCMeta

    _IGNORE_ME_VAR_NAME = 'ignore_me'
    ignore_me = False

    def __init__(self, lizy, name, description, rollback=None):
        super(Command, self).__init__()

        logme.debug("Initializing %s command with rollback %s", name, rollback)

        self.name = name
        self.description = description
        self.parser = lizy.add_subparser(self.name, help=self.description)
        self._lizy = lizy
        self.before_tasks = set()
        self.after_tasks = set()
        self.result = None
        self.rollback = rollback

        lizy.add_command(self.name, self)

    @abstractmethod
    def _process_command(self, lizy, args):
        pass  # pragma: no cover

    def __call__(self, args):
        with Caution() as caution:
            logme.debug("Executing before tasks.")
            for task in self.before_tasks:
                rollback = task(self._lizy, args)
                logme.debug("Before task returned rollback %s.", rollback)
                caution.add_rollback(rollback)

            logme.debug("Executing command %s with args %s and rollback %s.", self.name, args, self.rollback)
            result = self._process_command(self._lizy, args)
            logme.debug("Command %s finished, rollback is %s.", self.name, self.rollback)
            caution.add_rollback(self.rollback)

            self.result = result

            logme.debug("Executing after tasks.")
            for task in self.after_tasks:
                rollback = task(self._lizy, args)
                logme.debug("After task returned rollback %s.", rollback)
                caution.add_rollback(rollback)

        return caution.result

    @classmethod
    def init_all(cls, lizy):
        commands = cls.__subclasses__()

        for command in commands:
            command.init_all(lizy)
            if not getattr(command, cls._IGNORE_ME_VAR_NAME):
                command(lizy)

    def add_before_task(self, task):
        self.before_tasks.add(task)
        task.set_command(self)

    def add_after_task(self, task):
        self.after_tasks.add(task)
        task.set_command(self)


class NamedCommand(Command):
    # pylint: disable=W0223, too-few-public-methods
    # NamedCommand is also abstract
    # The number of public methods is reasonable for this kind of class

    _SUFFIX = "Command"
    ignore_me = SubclassIgnoreMark('NamedCommand')

    def __init__(self, lizy, description, rollback=None):
        my_name = self.__class__.__name__
        name = my_name[:-(len(self._SUFFIX))].lower()

        super(NamedCommand, self).__init__(lizy, name, description, rollback)


class StatusCommand(NamedCommand):
    # pylint: disable=too-few-public-methods
    # The number of public methods is reasonable for this kind of class

    OUTPUT_FMT = 'Project Name: {name}\nCurrent Version: {version}'

    KEY_VERSION = 'version'
    KEY_NAME = 'name'

    def __init__(self, lizy):
        super(StatusCommand, self).__init__(lizy, 'Retrieve current status of the project')

    def _process_command(self, lizy, args):
        print(self.OUTPUT_FMT.format(name=lizy.info_container.name, version=lizy.info_container.version))

        return {self.KEY_NAME: lizy.info_container.name, self.KEY_VERSION: lizy.info_container.version}


class MakeCommand(NamedCommand):
    # pylint: disable=too-few-public-methods
    # The number of public methods is reasonable for this kind of class

    KEY_OLD_VERSION = 'old_version'
    KEY_NEW_VERSION = 'new_version'
    KEY_LEVEL = 'level'

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
            error_msg = "Version specification not found!"
            logme.error(error_msg)
            raise PyleaseError(error_msg)

        level = args.level

        new_version = release(old_version, level)

        files = lizy.get_version_files()

        counts = update_files(old_version, new_version, files)

        count = 0
        for version_file in counts:
            count += counts[version_file]

        if count > 1:
            logme.warn("More than one version specification found.")
            logme.debug("Occurrences:")
            for filename in counts:
                msg = "\t{filename}: {count}".format(filename=filename, count=counts[filename])
                logme.debug(msg)

        self.rollback = VersionRollback(old_version, new_version, files).rollback
        return {self.KEY_OLD_VERSION: str(old_version), self.KEY_NEW_VERSION: str(new_version), self.KEY_LEVEL: str(level)}


class InitCommand(NamedCommand):
    # pylint: disable=too-few-public-methods
    # The number of public methods is reasonable for this kind of class
    def __init__(self, lizy):
        super(InitCommand, self).__init__(lizy, 'Initialize a new Python project', None)

    def _process_command(self, lizy, args):
        super(InitCommand, self)._process_command(lizy, args)
