from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from django.core.exceptions import ValidationError as DjangoValidationError


class InvalidWorkflowTransitionException(Exception):
    def __init__(self,
                 from_status: str,
                 to_status: str,
                 extra: str = "Can't transition between statuses"):
        message = "Invalid workflow transition from status %s to status %s" % (
            from_status,
            to_status,
        )
        if extra:
            message += ": " + extra
        return super().__init__(message)


class InvalidWorkflowTransitionAPIException(APIException):
    status_code = 400
    default_detail = 'Invalid workflow transition'
    default_code = 'bad_request'

    def __init__(self, exception: InvalidWorkflowTransitionException):
        detail = str(exception)
        return super().__init__(detail)


def exception_handler(exc, context):
    """
    Handle Django ValidationError as an accepted exception.
    """

    if isinstance(exc, DjangoValidationError):
        try:
            detail = exc.message_dict
        except Exception:
            detail = exc.messages
        exc = DRFValidationError(detail=detail)
    elif isinstance(exc, InvalidWorkflowTransitionException):
        exc = InvalidWorkflowTransitionAPIException(exc)

    return drf_exception_handler(exc, context)

