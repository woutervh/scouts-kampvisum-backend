from typing import List

from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckValidator:
    @staticmethod
    def validate(validators: str, value: any, *args, **kwargs) -> bool:
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
                if not getattr(CheckValidator, validator)(value=value, *args, **kwargs):
                    return False

        return True

    @staticmethod
    def is_number(value: any, *args, **kwargs) -> bool:
        if isinstance(value, int) or isinstance(value, float):
            return True
        return False

    @staticmethod
    def is_positive_number(value: any, *args, **kwargs) -> bool:
        return CheckValidator.is_number(value) and int(value) >= 0

    @staticmethod
    def validate_estimate(value: any, *args, **kwargs):
        return CheckValidator.is_positive_number(value)
    
    @staticmethod
    def validate_responsible_unique(value, *args, **kwargs):
        from apps.visums.models import LinkedParticipantCheck

        linked_participant_check = LinkedParticipantCheck.objects.safe_get(visum=value.sub_category.category.category_set.visum, linked_to=value.parent.linked_to, raise_error=True)

        if linked_participant_check.participants.count() > 0 and linked_participant_check.first().participant.group_admin_id == kwargs.get("group_admin_id"):
            raise ValidationError("Duplicate camp responsibles !")

        return True
