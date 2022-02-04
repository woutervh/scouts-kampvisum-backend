import logging

from django.db import models
from django.core.exceptions import ValidationError

from apps.participants.models import InuitsParticipant
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
    
    # def has_value(self) -> bool:
    #     raise NotImplementedError("Subclasses should implement their own has_value method")
    
    def is_checked(self) -> bool:
        if self.should_be_checked():
            value = self.has_value()
            return value
        return True
        
    def should_be_checked(self) -> bool:
        check_type: CheckType = self.parent.check_type

        if check_type.is_simple_check() or check_type.is_date_check() or check_type.is_duration_check() or check_type.is_location_check() or check_type.is_camp_location_check() or check_type.is_participant_check():
            return True
        if check_type.is_file_upload_check() or check_type.is_comment_check():
            return False

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
    value = DefaultCharField(choices=CheckState.choices, default=CheckState.EMPTY)
    
    def has_value(self) -> bool:
        if CheckState.is_checked_or_irrelevant(self.value):
            return True
        return False
        


# ##############################################################################
# LinkedDateCheck
#
# A check that contains a date
# ##############################################################################
class LinkedDateCheck(LinkedCheck):
    value = DatetypeAwareDateField(null=True, blank=True)
    
    def has_value(self) -> bool:
        if self.value:
            return True
        return False


# ##############################################################################
# LinkedDurationCheck
#
# A check that contains a start and end date
# ##############################################################################
class LinkedDurationCheck(LinkedCheck):
    start_date = DatetypeAwareDateField(null=True, blank=True)
    end_date = DatetypeAwareDateField(null=True, blank=True)
    
    def has_value(self) -> bool:
        if self.start_date and self.end_date:
            return True
        return False


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
    
    def has_value(self) -> bool:
        if self.locations and self.locations.count() > 0:
            return True
        return False


# ##############################################################################
# LinkedParticipantCheck
#
# A check that selects members and non-members
# ##############################################################################
class LinkedParticipantCheck(LinkedCheck):
    value = models.ManyToManyField(InuitsParticipant)
    
    def has_value(self) -> bool:
        if len(self.value.all()) > 0:
            return True
        return False


# ##############################################################################
# LinkedFileUploadCheck
#
# A check that contains a file
# ##############################################################################
class LinkedFileUploadCheck(LinkedCheck):
    value = models.ManyToManyField(PersistedFile, related_name="checks")
    
    def has_value(self) -> bool:
        if self.value:
            return True
        return False


# ##############################################################################
# LinkedCommentCheck
#
# A check that contains comments
# ##############################################################################
class LinkedCommentCheck(LinkedCheck):
    value = OptionalCharField(max_length=300)
    
    def has_value(self) -> bool:
        if self.value:
            return True
        return False
