from django.db import models

from apps.visums.models.enums import CheckTypeEnum
from apps.visums.managers import CheckTypeManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.mixins import Describable
from scouts_auth.inuits.models.fields import RequiredCharField

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckType(Describable, AbstractBaseModel):

    objects = CheckTypeManager()

    check_type = RequiredCharField(max_length=32)

    class Meta:
        ordering = ["check_type"]
        constraints = [
            models.UniqueConstraint(fields=["check_type"], name="unique_check_type")
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED CheckType")
        return (self.check_type,)

    @property
    def endpoint_route(self):
        endpoint = CheckTypeEnum.endpoint_from_type(self.check_type)

        # logger.debug("ENDPOINT: %s", endpoint)

        return endpoint

    def is_simple_check(self):
        return self.check_type == CheckTypeEnum.SIMPLE_CHECK

    def is_date_check(self):
        return self.check_type == CheckTypeEnum.DATE_CHECK

    def is_duration_check(self):
        return self.check_type == CheckTypeEnum.DURATION_CHECK

    def is_location_check(self):
        return self.check_type == CheckTypeEnum.LOCATION_CHECK

    def is_camp_location_check(self):
        return self.check_type == CheckTypeEnum.CAMP_LOCATION_CHECK

    def is_member_check(self):
        return self.check_type == CheckTypeEnum.MEMBER_CHECK

    def is_participant_check(self):
        return (
            self.check_type == CheckTypeEnum.PARTICIPANT_CHECK
            or self.is_participant_member_check()
            or self.is_participant_cook_check()
            or self.is_participant_leader_check()
            or self.is_participant_responsible_check()
            or self.is_participant_adult_check()
        )

    def is_participant_member_check(self):
        return self.check_type == CheckTypeEnum.PARTICIPANT_MEMBER_CHECK

    def is_participant_cook_check(self):
        return self.check_type == CheckTypeEnum.PARTICIPANT_COOK_CHECK

    def is_participant_leader_check(self):
        return self.check_type == CheckTypeEnum.PARTICIPANT_LEADER_CHECK

    def is_participant_responsible_check(self):
        return self.check_type == CheckTypeEnum.PARTICIPANT_RESPONSIBLE_CHECK

    def is_participant_adult_check(self):
        return self.check_type == CheckTypeEnum.PARTICIPANT_ADULT_CHECK

    def is_file_upload_check(self):
        return self.check_type == CheckTypeEnum.FILE_UPLOAD_CHECK

    def is_comment_check(self):
        return self.check_type == CheckTypeEnum.COMMENT_CHECK

    def is_number_check(self):
        return self.check_type == CheckTypeEnum.NUMBER_CHECK

    def __str__(self):
        return "OBJECT CheckType: check_type({})".format(self.check_type)
