class EmailServiceException(Exception):
    def __init__(self, message):
        return super().__init__(message)
