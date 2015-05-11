
class PyleaseError(Exception):
    def __init__(self, message='', *args, **kwargs):
        super(PyleaseError, self).__init__(*args, **kwargs)

        self.message = message


class VersionSpecError(PyleaseError):
    pass


class ReleaseError(PyleaseError):
    pass


class UploadError(PyleaseError):
    pass
