
class PyleaseError(Exception):
    pass


class VersionSpecError(PyleaseError):
    pass


class ReleaseError(PyleaseError):
    pass


class UploadError(PyleaseError):
    pass
