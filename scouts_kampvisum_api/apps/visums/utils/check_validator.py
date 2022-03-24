from typing import List

from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckValidator:
    @staticmethod
    def validate(validators: str, value: any) -> bool:
        validators: List[str] = validators.split(",")

        # logger.debug("VALIDATORS: %s", validators)

        for validator in validators:
            if len(validator.strip()) > 0:
                if not hasattr(CheckValidator, validator):
                    raise ValidationError(
                        "A validator was defined ({}), but the method is not defined".format(
                            validator
                        )
                    )
                # logger.debug(
                #     "Validating value %s (%s) with validator %s",
                #     value,
                #     type(value).__name__,
                #     validator,
                # )
                if not getattr(CheckValidator, validator)(value=value):
                    return False

        return True

    @staticmethod
    def is_number(value: any) -> bool:
        if isinstance(value, int) or isinstance(value, float):
            return True
        return False

    @staticmethod
    def is_positive_number(value: any) -> bool:
        return CheckValidator.is_number(value) and int(value) >= 0

    @staticmethod
    def validate_estimate(value):
        return CheckValidator.is_positive_number(value)
