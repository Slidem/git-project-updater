class UpdaterError(Exception):
    def __init__(self, message):
        super().__init__(message)


class MultiplePropertiesDefined(UpdaterError):
    def __init__(self, message):
        super().__init__(message)


class VersionChangerError(UpdaterError):
    def __init__(self, message):
        super().__init__(message)
