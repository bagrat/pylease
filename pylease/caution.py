from io import BytesIO
import sys

# The dirtiest hack in the world
import setuptools
from pylease.ex import PyleaseError, VersionRetrievalError
from pylease.releasemgmt import rollback

_setuptools_success_msg_prefix = 'Server response '


class BypassIO(BytesIO):
    def __init__(self, master_ios, initial_bytes=None):
        super(BypassIO, self).__init__(initial_bytes)

        self.master_ios = master_ios

    def write(self, bytes):
        for master_io in self.master_ios:
            master_io.write(bytes)

        return super(BypassIO, self).write(bytes)


class DirtyCaution(object):
    def __init__(self, current_version):
        super(DirtyCaution, self).__init__()

        self.current_version = current_version

    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self.master_io = BytesIO()

        sys.stdout = BypassIO(master_ios=(self.master_io, self._stdout))
        sys.stderr = BypassIO(master_ios=(self.master_io, self._stderr))

        return self.master_io

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._stdout
        sys.stderr = self._stderr

        lines = self.master_io.getvalue().splitlines()

        if not lines[len(lines) - 1]\
                .startswith(_setuptools_success_msg_prefix):
            rollback(self.current_version)

        return exc_type is None


class ReplacedSetup(object):
    def __init__(self):
        super(ReplacedSetup, self).__init__()

    def __enter__(self):
        self._old_setup = setuptools.setup
        setuptools.setup = self._setup_reporter

    def __exit__(self, exc_type, exc_val, exc_tb):
        setuptools.setup = self._old_setup

    @staticmethod
    def _setup_reporter(*args, **kwargs):
        if 'version' not in kwargs:
            raise PyleaseError('Something\'s wrong?')

        raise VersionRetrievalError(kwargs['version'])
