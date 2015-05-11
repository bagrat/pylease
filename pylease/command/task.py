from abc import ABCMeta, abstractmethod
from pylease.ctxmgmt import Caution
from pylease.logger import LOGME as logme  # noqa


class BeforeTask(object):
    # pylint: disable=too-few-public-methods
    # The number of public methods is reasonable for this kind of class

    __metaclass__ = ABCMeta

    def __init__(self, rollback=None):
        super(BeforeTask, self).__init__()

        logme.debug("Initializing {} with rollback '{}'".format(self.__class__.__name__, rollback))
        self._command = None
        self._rollback = rollback
        self._needs_rollback = False

    def enable_rollback(self, rollback=None):
        if rollback:
            if self._rollback:
                logme.debug('Overwriting existing rollback for task "{}"'.format(self.__class__.__name__))
            self._rollback = rollback
        self._needs_rollback = True

    def set_command(self, command):
        self._command = command

    def __call__(self, lizy, args):
        try:
            logme.debug("Executing task {}".format(self.__class__.__name__))
            self.execute(lizy, args)

            if self._needs_rollback:
                logme.debug("Done executing task {}, rollback is {}".format(self.__class__.__name__, self._rollback))
                return self._rollback
        except BaseException as ex:
            if self._needs_rollback:
                logme.debug("{} error occurred, setting rollback '{}' to exception".format(ex.__class__.__name__, self._rollback))
                setattr(ex, Caution.EXCEPTION_ROLLBACK_ATTR_NAME, self._rollback)
            raise ex

    @abstractmethod
    def execute(self, lizy, args):
        pass  # pragma: no cover


class AfterTask(BeforeTask):
    # pylint: disable=too-few-public-methods, W0223
    # AfterTask is also abstract
    # The number of public methods is reasonable for this kind of class

    __metaclass__ = ABCMeta

    @property
    def _command_result(self):
        return self._command.result  # pragma: no cover
