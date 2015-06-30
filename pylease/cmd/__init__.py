from __future__ import print_function
from abc import ABCMeta, abstractmethod
import os
from pylease.cmd.rollback import Rollback, Stage

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
    """
    This class is one of the main point of Pylease.
    For adding new commands just inherit from this class and implement :func:`~pylease.cmd.Command._process_command` method.
    """

    __metaclass__ = ABCMeta

    _IGNORE_ME_VAR_NAME = 'ignore_me'
    ignore_me = False

    def __init__(self, lizy, name, description, rollback=None, requires_project=True):
        """
        This constructor should be called from child classes and at least be supplied with at least ``name`` and ``description``.

        Arguments:
            lizy (pylease.Pylease): The `lizy` object, which is initialized and passed by Pylease.
            name (str): The name of the command, which will appear in the `usage` output.
            description (str): Description of the command which will also appear in the help message.
            rollback (pylease.cmd.rollback.Rollback): The rollback object that will be executed in case of failure during or after the
                command. This parameter may be emitted if the command does not need a rollback, or may be set in the process of command
                execution using the :func:`~pylease.cmd.task.BeforeTask.enable_rollback` method, if it depends on some parameters during
                runtime.
            requires_project (bool): Boolean indicating whether the command requires to operate on an existing project. E.g. the ``init``
                command requires an empty directory.
        """
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
        self.requires_project = requires_project

        lizy.add_command(self.name, self)

    @abstractmethod
    def _process_command(self, lizy, args):
        """
        The method which should be implemented when inheriting the :class:`~pylease.cmd.Command`. All the command logic must go into this
        method.

        Arguments:
            lizy (pylease.Pylease): The :class:`~pylease.Pylease` singleton.
            args (argparse.Namespace): The arguments passed to the command line while invoking Pylease.
        """
        pass  # pragma: no cover

    def __call__(self, args):
        with Caution(verbose=args.verbose) as caution:
            if self.requires_project and self._lizy.info_container.is_empty:
                raise PyleaseError("'{}' command requires an existing project!".format(self.name))  # pragma: no cover

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
        """
        Adds a :class:`~pylease.cmd.task.BeforeTask` to the :class:`~pylease.cmd.Command`.

        Arguments:
            task (pylease.cmd.task.BeforeTask): The task to be added.
        """
        self.before_tasks.add(task)
        task.set_command(self)

    def add_after_task(self, task):
        """
        Adds a :class:`~pylease.cmd.task.AfterTask` to the :class:`~pylease.cmd.Command`.

        Arguments:
            task (pylease.cmd.task.AfterTask): The task to be added.
        """
        self.after_tasks.add(task)
        task.set_command(self)


class NamedCommand(Command):
    # pylint: disable=W0223, W1401, too-few-public-methods
    # NamedCommand is also abstract
    # The number of public methods is reasonable for this kind of class
    """
    Same as the :class:`~pylease.cmd.Command` class, however this class enables a little taste of convenience. You can define a class
    having name with a suffix "\ |pylease_named_command_suffix|\ " and it will automatically assign the prefix of the class name as the
    command name.
    """

    _SUFFIX = "Command"
    ignore_me = SubclassIgnoreMark('NamedCommand')

    def __init__(self, lizy, description, rollback=None, requires_project=True):
        """
        Same as :func:`~pylease.cmd.Command.__init__` of :class:`~pylease.cmd.Command` class, except that the ``name`` argument is passed
        automatically.
        """
        my_name = self.__class__.__name__
        name = my_name[:-(len(self._SUFFIX))].lower()

        super(NamedCommand, self).__init__(lizy, name, description, rollback, requires_project)


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
        logme.info('%s releasing %s to v%s', level.capitalize(), lizy.info_container.name, new_version)

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

    SETUP_PY_CONTENTS = """import {name}
from setuptools import setup

setup(name='{name}',
      version={name}.__version__)
"""
    SETUP_CFG_CONTENTS = """[pylease]
version-files = {name}/__init__.py
"""
    INIT_PY_CONTENTS = """__version__ = '{version}'
"""
    INITIAL_VERSION = '0.0'

    SETUP_PY_NAME = 'setup.py'
    SETUP_CFG_NAME = 'setup.cfg'
    INIT_PY_NAME_FMT = '{name}/__init__.py'

    def __init__(self, lizy):
        super(InitCommand, self).__init__(lizy, 'Initialize a new Python project', requires_project=False)

        self.parser.add_argument('name', action='store', type=str, help='name of the project to be initiated')

    def _process_command(self, lizy, args):
        super(InitCommand, self)._process_command(lizy, args)

        project_name = args.name
        setup_py_name = self.SETUP_PY_NAME
        setup_cfg_name = self.SETUP_CFG_NAME
        init_py_name = self.INIT_PY_NAME_FMT.format(name=project_name)

        setup_py_contents = self.SETUP_PY_CONTENTS.format(name=args.name)
        setup_cfg_contents = self.SETUP_CFG_CONTENTS.format(name=args.name)
        init_py_contents = self.INIT_PY_CONTENTS.format(version=self.INITIAL_VERSION)

        rollback = InitRollback(project_name)
        self.rollback = rollback

        nodes_in_cwd = [node for node in os.listdir('.') if not node.startswith('.')]
        if nodes_in_cwd:  # pragma: no cover
            logme.debug('Directory not empty.\nFollowing files are present:\n%s', nodes_in_cwd)
            raise PyleaseError('Directory not empty.\nSorry, but the directory must be empty to initialise a new project.')

        os.mkdir(project_name)
        rollback.enable_stage(InitRollback.DIRECTORY_STAGE)

        self._write_file(setup_py_name, setup_py_contents)
        rollback.enable_stage(rollback.SETUPPY_STAGE)

        self._write_file(setup_cfg_name, setup_cfg_contents)
        rollback.enable_stage(rollback.SETUPCFG_STAGE)

        self._write_file(init_py_name, init_py_contents)
        rollback.enable_stage(rollback.INITPY_STAGE)

    @classmethod
    def _write_file(cls, filename, contents):
        with open(os.path.join(os.getcwd(), filename), 'w') as the_file:
            the_file.write(contents)


class InitRollback(Rollback):  # pragma: no cover; Tested in the scope of Rollback class
    SETUPPY_STAGE = 'setuppy'
    SETUPCFG_STAGE = 'setupcfg'
    INITPY_STAGE = 'initpy'
    DIRECTORY_STAGE = 'directory'

    def __init__(self, project_name):
        super(InitRollback, self).__init__()

        self._name = project_name

    @Stage(SETUPPY_STAGE)
    def rollback_setuppy(self):
        logme.debug('Removing setup.py')
        os.remove(InitCommand.SETUP_PY_NAME)

    @Stage(SETUPCFG_STAGE)
    def rollback_setupcfg(self):
        logme.debug('Removing setup.cfg')
        os.remove(InitCommand.SETUP_CFG_NAME)

    @Stage(INITPY_STAGE)
    def rollback_initpy(self):
        logme.debug('Removing __init__.py')
        os.remove(InitCommand.INIT_PY_NAME_FMT.format(name=self._name))

    @Stage(DIRECTORY_STAGE)
    def rollback_directory(self):
        logme.debug('Removing %s', self._name)
        os.remove(self._name)
