class BaseError(Exception):
    message: str = None

    def __init__(self, message):
        self.message = message


class InvalidURL(BaseError):
    pass
