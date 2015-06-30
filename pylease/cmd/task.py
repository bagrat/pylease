from abc import ABCMeta, abstractmethod
from pylease.ctxmgmt import Caution
from pylease.logger import LOGME as logme  # noqa


class BeforeTask(object):
    """

    """
    # pylint: disable=too-few-public-methods
    # The number of public methods is reasonable for this kind of class

    __metaclass__ = ABCMeta

    def __init__(self, rollback=None):
        super(BeforeTask, self).__init__()

        logme.debug("Initializing %s with rollback '%s'", self.__class__.__name__, rollback)
        self._command = None
        self._rollback = rollback
        self._needs_rollback = False

    def enable_rollback(self, rollback=None):
        """
        Enables a rollback for the task. The provided rollback gets executed in case of failure in the execution stack.

        Attributes:
            rollback (pylease.cmd.rollback.Rollback): The rollback instance for the task.
        """
        if rollback:
            if self._rollback:
                logme.debug('Overwriting existing rollback for task "%s"', self.__class__.__name__)
            self._rollback = rollback
        self._needs_rollback = True

    def set_command(self, command):
        self._command = command

    def __call__(self, lizy, args):
        try:
            logme.debug("Executing task %s", self.__class__.__name__)
            self.execute(lizy, args)

            if self._needs_rollback:
                logme.debug("Done executing task %s, rollback is %s", self.__class__.__name__, self._rollback)
                return self._rollback
        except BaseException as ex:
            if self._needs_rollback:
                logme.debug("%s error occurred, setting rollback '%s' to exception", ex.__class__.__name__, self._rollback)
                setattr(ex, Caution.EXCEPTION_ROLLBACK_ATTR_NAME, self._rollback)
            raise ex

    @abstractmethod
    def execute(self, lizy, args):
        """
        The place where the extension logic goes on.

        Arguments:
            lizy (pylease.Pylease): The :class:`~pylease.Pylease` singleton that provides all the needed information about the project.
            args (argparse.Namespace): The arguments supplied to the command line.
        """
        pass  # pragma: no cover


class AfterTask(BeforeTask):
    # pylint: disable=too-few-public-methods, W0223
    # AfterTask is also abstract
    # The number of public methods is reasonable for this kind of class
    __metaclass__ = ABCMeta

    @property
    def _command_result(self):
        """
        A dictionary containing information by the completion of the command execution.
        """
        return self._command.result  # pragma: no cover
