from rest_framework.exceptions import APIException
from requests.exceptions import HTTPError


class ScoutsAuthException(APIException):

    cause: Exception = None

    def __init__(self, message, http_exception: HTTPError = None, cause: Exception = None):
        if http_exception:
            if isinstance(http_exception, HTTPError):
                super().__init__(message % (http_exception, http_exception.response.text))
            else:
                super().__init__(message)
        else:
            super().__init__(message)

        self.cause = cause if cause else None

    def has_cause(self) -> bool:
        return self.cause is not None


class TokenRequestException(ScoutsAuthException):
    def __init__(self, http_exception: HTTPError):
        super().__init__(
            "SCOUTS_AUTH: OIDC auth token request failed with error: %s with message: %s",
            http_exception,
        )


class TokenRefreshException(ScoutsAuthException):
    def __init__(self, http_exception: HTTPError):
        super().__init__(
            "SCOUTS_AUTH: OIDC token refresh failed with error: %s with message: %s",
            http_exception,
        )


class InvalidArgumentException(APIException):
    def __init__(self, message):
        super().__init__(message)
