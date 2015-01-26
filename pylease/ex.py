__author__ = 'bagrat'


class PyleaseError(Exception):
    pass


class VersionSpecError(PyleaseError):
    pass


class ReleaseError(PyleaseError):
    pass


class VersionRetrievalError(PyleaseError):
    def __init__(self, version, *args, **kwargs):
        super(VersionRetrievalError, self).__init__(*args, **kwargs)
        self.version = version


class UploadError(PyleaseError):
    pass