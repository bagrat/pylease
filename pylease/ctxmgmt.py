"""
This is the dirtiest hack in the world I guess. But this is done for good,
 may be replaced by using legacy setuptools extension methods.
"""
from io import BytesIO
import sys
import setuptools

from pylease.ex import PyleaseError, VersionRetrievalError
from pylease.releasemgmt import rollback

_setuptools_success_msg_prefix = 'Server response '


class BypassIO(BytesIO):
    """
    Bypassing IO for multiplexing data stream.
    """

    def __init__(self, master_ios, initial_bytes=None):
        """
        Proxies BytesIO __init__ and requires a list of other IO objects
         that need to capture the data written to this instance.

        :param master_ios: The list of capturing IOs
        :param initial_bytes: see ByteIO.write
        """
        super(BypassIO, self).__init__(initial_bytes)

        self.master_ios = master_ios

    def write(self, bytes):
        """
        Overrides BytesIO write method by calling it, and in addition
         multiplexes the data to all IOs provided in the constructor as
         master_ios

        :param bytes: The data to be written to the IO
        """
        for master_io in self.master_ios:
            master_io.write(bytes)

        return super(BypassIO, self).write(bytes)


class DirtyCaution(object):
    """
    The hack for checking setup status. This context manager listens to
    stdout and stderr to read the last log message of setup to detect final
    status.
    """
    # TODO: more research for checking for setup success

    def __init__(self, current_version):
        super(DirtyCaution, self).__init__()

        self.current_version = current_version

    def __enter__(self):
        """
        Enters the 'with' context by setting a listener IO for stdout and
        stderr.
        """
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self.master_io = BytesIO()

        sys.stdout = BypassIO(master_ios=(self.master_io, self._stdout))
        sys.stderr = BypassIO(master_ios=(self.master_io, self._stderr))

        return self.master_io

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the 'with' context by detaching the stdout and stderr
        listener. Besides, checks for setup status and rolls back package
        version to current_version in case of failure.
        """
        sys.stdout = self._stdout
        sys.stderr = self._stderr

        lines = self.master_io.getvalue().splitlines()

        if lines and not lines[len(lines) - 1]\
                .startswith(_setuptools_success_msg_prefix):
            rollback(self.current_version)

            if not exc_type:
                sys.exit(1)

        if exc_type:
            print(exc_val.message)
            sys.exit(1)


class ReplacedSetup(object):
    """
    Context manager for replacing setuptools setup method and then setting
    all back.
    """
    def __init__(self):
        super(ReplacedSetup, self).__init__()

    def __enter__(self):
        self._old_setup = setuptools.setup
        setuptools.setup = self._setup_reporter

    def __exit__(self, exc_type, exc_val, exc_tb):
        setuptools.setup = self._old_setup

    @staticmethod
    def _setup_reporter(*args, **kwargs):
        """
        The replacement method for setup method.
        """
        if 'version' not in kwargs:
            raise PyleaseError('Something\'s wrong?')

        raise VersionRetrievalError(kwargs['version'])
