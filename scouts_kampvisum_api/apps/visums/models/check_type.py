import logging

from django.db import models

from apps.visums.managers import CheckTypeManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.interfaces import Describable
from scouts_auth.inuits.models.fields import RequiredCharField


logger = logging.getLogger(__name__)


class CheckTypeEndpoint(models.TextChoices):
    """
    An enum that links known models to a routable endpoint string
    """

    SIMPLE_CHECK = "SimpleCheck", "simple"
    DATE_CHECK = "DateCheck", "date"
    DURATION_CHECK = "DurationCheck", "duration"
    LOCATION_CHECK = "LocationCheck", "location"
    LOCATION_CONTACT_CHECK = "LocationContactCheck", "location_contact"
    MEMBER_CHECK = "MemberCheck", "member"
    CONTACT_CHECK = "ContactCheck", "contact"
    FILE_UPLOAD_CHECK = "FileUploadCheck", "file"
    INPUT_CHECK = "InputCheck", "input"
    INFORMATION_CHECK = "InformationCheck", "info"

    @staticmethod
    def endpoint_from_type(check_type: str):
        for option in CheckTypeEndpoint.choices:
            if option[0] == check_type:
                return option[1]
        return None


class CheckType(Describable, AbstractBaseModel):

    objects = CheckTypeManager()

    check_type = RequiredCharField(max_length=32)

    class Meta:
        ordering = ["check_type"]
        constraints = [
            models.UniqueConstraint(fields=["check_type"], name="unique_check_type")
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED")
        return (self.check_type,)

    @property
    def endpoint_route(self):
        endpoint = CheckTypeEndpoint.endpoint_from_type(self.check_type)

        logger.debug("ENDPOINT: %s", endpoint)

        return endpoint

    def is_simple_check(self):
        return self.check_type == CheckTypeEndpoint.SIMPLE_CHECK

    def is_date_check(self):
        return self.check_type == CheckTypeEndpoint.DATE_CHECK

    def is_duration_check(self):
        return self.check_type == CheckTypeEndpoint.DURATION_CHECK

    def is_location_check(self):
        return self.check_type == CheckTypeEndpoint.LOCATION_CHECK

    def is_location_contact_check(self):
        return self.check_type == CheckTypeEndpoint.LOCATION_CONTACT_CHECK

    def is_member_check(self):
        return self.check_type == CheckTypeEndpoint.MEMBER_CHECK

    def is_contact_check(self):
        return self.check_type == CheckTypeEndpoint.CONTACT_CHECK

    def is_file_upload_check(self):
        return self.check_type == CheckTypeEndpoint.FILE_UPLOAD_CHECK

    def is_input_check(self):
        return self.check_type == CheckTypeEndpoint.INPUT_CHECK

    def is_information_check(self):
        return self.check_type == CheckTypeEndpoint.INFORMATION_CHECK

    def __str__(self):
        return "OBJECT CheckType: check_type({})".format(self.check_type)
