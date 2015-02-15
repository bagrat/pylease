"""
This is the dirtiest hack in the world I guess. But this is done for good,
 may be replaced by using legacy setuptools extension methods.
"""
import setuptools
from pylease import logme

from pylease.ex import VersionRetrievalError


class Caution(object):
    """
    Context manager for handling rollback process in case of setup failure
    """
    def __init__(self, rollback_object):
        super(Caution, self).__init__()

        self.rollback_object = rollback_object

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logme.error("some error occurred: rolling back...")
            self.rollback_object.rollback()


class ReplacedSetup(object):
    """
    Context manager for replacing setuptools setup method and then setting
    all back.
    """
    def __init__(self, callback):
        super(ReplacedSetup, self).__init__()

        self.callback = callback

    def __enter__(self):
        self._old_setup = setuptools.setup
        setuptools.setup = self._version_reporter

    def __exit__(self, exc_type, exc_val, exc_tb):
        setuptools.setup = self._old_setup

        if exc_type == VersionRetrievalError:
            return True

    def _version_reporter(self, **kwargs):
        """
        The replacement method for setup method.
        """
        self.callback(kwargs.get('version'))

        raise VersionRetrievalError
