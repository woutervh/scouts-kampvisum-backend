from rest_framework.exceptions import APIException
from requests.exceptions import HTTPError


class ScoutsAuthException(APIException):
    def __init__(self, message, http_exception: HTTPError = None):
        if http_exception:
            super().__init__(message % (http_exception, http_exception.response.text))
        else:
            super().__init__(message)


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
