__author__ = 'bagrat'


class PyleaseError(Exception):
    pass


class VersionSpecError(PyleaseError):
    pass


class ReleaseError(PyleaseError):
    pass


class VersionRetrievalError(PyleaseError):
    pass


class UploadError(PyleaseError):
    pass
