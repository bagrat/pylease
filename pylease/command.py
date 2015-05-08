from __future__ import print_function
from abc import ABCMeta, abstractmethod

from pylease import LOGME as logme  # pep8:disable=N811
from pylease.ctxmgmt import Caution
from pylease.ex import PyleaseError
from pylease.filemgmt import update_files
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
            for task in self.before_tasks:
                rollback = task(self._lizy, args)
                caution.add_rollback(rollback)

            result = self._process_command(self._lizy, args)
            caution.add_rollback(self.rollback)

            self.result = result

            for task in self.after_tasks:
                rollback = task(self._lizy, args)
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


class BeforeTask(object):
    __metaclass__ = ABCMeta

    def __init__(self, rollback=None):
        super(BeforeTask, self).__init__()

        self._command = None
        self._rollback = rollback

    def set_command(self, command):
        self._command = command

    def __call__(self, lizy, args):
        try:
            self.execute(lizy, args)
            return self._rollback
        except Exception as ex:
            setattr(ex, 'rollback', self._rollback)
            raise ex

    @abstractmethod
    def execute(self, lizy, args):
        pass  # pragma: no cover


class AfterTask(BeforeTask):

    # pylint: disable=W0223
    # AfterTask is also abstract

    __metaclass__ = ABCMeta

    @property
    def _command_result(self):
        return self._command.result  # pragma: no cover


class NamedCommand(Command):

    # pylint: disable=W0223
    # NamedCommand is also abstract

    _SUFFIX = "Command"
    ignore_me = SubclassIgnoreMark('NamedCommand')

    def __init__(self, lizy, description, rollback=None):
        my_name = self.__class__.__name__
        name = my_name[:-(len(self._SUFFIX))].lower()

        super(NamedCommand, self).__init__(lizy, name, description, rollback)


class StatusCommand(NamedCommand):
    OUTPUT_FMT = 'Project Name: {name}\nCurrent Version: {version}'

    KEY_VERSION = 'version'
    KEY_NAME = 'name'

    def __init__(self, lizy):
        super(StatusCommand, self).__init__(lizy, 'Retrieve current status of the project')

    def _process_command(self, lizy, args):
        print(self.OUTPUT_FMT.format(name=lizy.info_container.name, version=lizy.info_container.version))

        return {self.KEY_NAME: lizy.info_container.name, self.KEY_VERSION: lizy.info_container.version}


class MakeCommand(NamedCommand):
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

        return {self.KEY_OLD_VERSION: str(old_version), self.KEY_NEW_VERSION: str(new_version), self.KEY_LEVEL: str(level)}
