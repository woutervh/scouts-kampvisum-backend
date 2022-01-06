import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler

from scouts_auth.inuits.mail import EmailServiceException


logger = logging.getLogger(__name__)


def drf_exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception"""
    logger.error("EXC: %s", exc)
    if isinstance(exc, DjangoValidationError):
        try:
            detail = exc.message_dict
        except Exception:
            detail = exc.messages
        exc = DRFValidationError(detail=detail)
    elif isinstance(exc, EmailServiceException):
        exc = EmailServiceException(exc)

    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    return response
