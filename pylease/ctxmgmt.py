import setuptools
import sys
from pylease.logger import LOGME as logme


class Caution(object):
    """
    Context manager for handling rollback process in case of pylease failure
    """
    # pylint: too-few-public-methods
    # The number of public methods is reasonable for this kind of class

    EXCEPTION_ROLLBACK_ATTR_NAME = 'rollback'

    def __init__(self):
        super(Caution, self).__init__()

        self._rollbacks = set()
        self.result = 0

    def add_rollback(self, rollback):
        if rollback:
            self._rollbacks.add(rollback)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            msg = "Some error occurred: rolling back...\n{}".format(exc_val.message)
            logme.error(msg)
            logme.debug("Error occurred with type {}".format(exc_type.__name__))

            logme.debug("Checking {} exception for rollback".format(exc_type.__name__))
            if hasattr(exc_val, self.EXCEPTION_ROLLBACK_ATTR_NAME):
                rollback = getattr(exc_val, self.EXCEPTION_ROLLBACK_ATTR_NAME)
                logme.debug("Found rollback '{}', executing...".format(rollback))
                rollback()

            for rollback in self._rollbacks:
                rollback()

            self.result = 1

        return True


class ReplacedSetup(object):
    """
    Context manager for replacing setuptools setup method and then setting
    all back.
    """
    # pylint: too-few-public-methods
    # The number of public methods is reasonable for this kind of class
    def __init__(self, callback):
        super(ReplacedSetup, self).__init__()

        self._callback = callback
        self._old_setup = None

    def __enter__(self):
        self._old_setup = setuptools.setup
        setuptools.setup = self._version_reporter

    def __exit__(self, exc_type, exc_val, exc_tb):
        setuptools.setup = self._old_setup
        if 'setup' in sys.modules:
            del sys.modules['setup']

    def _version_reporter(self, **kwargs):
        """
        The replacement method for setup method.
        """
        self._callback(**kwargs)
