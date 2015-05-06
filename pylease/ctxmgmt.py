import setuptools
from pylease import logme


class Caution(object):
    """
    Context manager for handling rollback process in case of setup failure
    """
    def __init__(self):
        super(Caution, self).__init__()

        self._rollbacks = []
        self.result = 0

    def add_rollback(self, rollback):
        self._rollbacks.append(rollback)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logme.error("Some error occurred: rolling back...\n{}".format(exc_val.message))

            for rollback in self._rollbacks:
                rollback()

            self.result = 1

        return True


class ReplacedSetup(object):
    """
    Context manager for replacing setuptools setup method and then setting
    all back.
    """
    def __init__(self, callback):
        super(ReplacedSetup, self).__init__()

        self._callback = callback

    def __enter__(self):
        self._old_setup = setuptools.setup
        setuptools.setup = self._version_reporter

    def __exit__(self, exc_type, exc_val, exc_tb):
        setuptools.setup = self._old_setup

    def _version_reporter(self, **kwargs):
        """
        The replacement method for setup method.
        """
        self._callback(**kwargs)
