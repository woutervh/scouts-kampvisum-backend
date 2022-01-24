import logging

from django.db import models
from django.core.exceptions import ValidationError

from apps.people.models import InuitsMember, InuitsParticipant
from apps.visums.models import (
    LinkedSubCategory,
    Check,
    CheckType,
)
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel, PersistedFile
from scouts_auth.inuits.models.fields import (
    DefaultCharField,
    OptionalCharField,
    OptionalIntegerField,
    DatetypeAwareDateField,
)


logger = logging.getLogger(__name__)


class LinkedCheck(AbstractBaseModel):

    parent = models.ForeignKey(Check, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="checks"
    )

    class Meta:
        ordering = ["parent__index"]

    @staticmethod
    def get_concrete_check_type(check: Check):
        check_type: CheckType = check.check_type

        if check_type.is_simple_check():
            return LinkedSimpleCheck()
        elif check_type.is_date_check():
            return LinkedDateCheck()
        elif check_type.is_duration_check():
            return LinkedDurationCheck()
        elif check_type.is_location_check():
            return LinkedLocationCheck()
        elif check_type.is_camp_location_check():
            return LinkedLocationCheck(is_camp_location=True)
        elif check_type.is_member_check():
            return LinkedMemberCheck()
        elif check_type.is_participant_check():
            return LinkedParticipantCheck()
        elif check_type.is_file_upload_check():
            return LinkedFileUploadCheck()
        elif check_type.is_comment_check():
            return LinkedCommentCheck()
        else:
            raise ValidationError(
                "Check type {} is not recognized".format(check_type.check_type)
            )


# ##############################################################################
# LinkedSimpleCheck
#
# A check that can be checked, unchecked or set as not applicable
# ##############################################################################
class LinkedSimpleCheck(LinkedCheck):
    value = DefaultCharField(choices=CheckState.choices, default=CheckState.UNCHECKED)


# ##############################################################################
# LinkedDateCheck
#
# A check that contains a date
# ##############################################################################
class LinkedDateCheck(LinkedCheck):
    value = DatetypeAwareDateField(null=True, blank=True)


# ##############################################################################
# LinkedDurationCheck
#
# A check that contains a start and end date
# ##############################################################################
class LinkedDurationCheck(LinkedCheck):
    start_date = DatetypeAwareDateField(null=True, blank=True)
    end_date = DatetypeAwareDateField(null=True, blank=True)


# ##############################################################################
# LinkedLocationCheck
#
# A check that contains a geo-coordinate and contact details
# ##############################################################################
class LinkedLocationCheck(LinkedCheck):
    name = OptionalCharField(max_length=64)
    contact_name = OptionalCharField(max_length=128)
    contact_phone = OptionalCharField(max_length=64)
    contact_email = OptionalCharField(max_length=128)
    # locations linked through CampLocation object, related_name is 'locations'
    is_camp_location = models.BooleanField(default=False)
    center_latitude = models.FloatField(null=True, blank=True)
    center_longitude = models.FloatField(null=True, blank=True)
    zoom = OptionalIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ##############################################################################
# LinkedCampLocationCheck
#
# A check that contains a geo-coordinate and some required contact details
# ##############################################################################
# class LinkedCampLocationCheck(LinkedLocationCheck):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


# ##############################################################################
# LinkedMemberCheck
#
# A check that selects members
# ##############################################################################
class LinkedMemberCheck(LinkedCheck):
    value = models.ManyToManyField(InuitsMember)


# ##############################################################################
# LinkedParticipantCheck
#
# A check that selects members and non-members
# ##############################################################################
class LinkedParticipantCheck(LinkedCheck):
    value = models.ManyToManyField(InuitsParticipant)


# ##############################################################################
# LinkedFileUploadCheck
#
# A check that contains a file
# ##############################################################################
class LinkedFileUploadCheck(LinkedCheck):
    value = models.ManyToManyField(PersistedFile)


# ##############################################################################
# LinkedCommentCheck
#
# A check that contains comments
# ##############################################################################
class LinkedCommentCheck(LinkedCheck):
    value = OptionalCharField(max_length=300)
