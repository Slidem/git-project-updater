class UpdaterError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class MultiplePropertiesDefined(UpdaterError):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
