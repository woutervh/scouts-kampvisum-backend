from django.db import models

from apps.visums.models import LinkedSubCategory, VisumCheck
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel, PersistedFile
from scouts_auth.inuits.models.fields import (
    DefaultCharField,
    OptionalCharField,
    DatetypeAwareDateField,
)


class LinkedCheck(AbstractBaseModel):

    parent = models.ForeignKey(VisumCheck, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="checks"
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
# A check that contains a geo-coordinate
# ##############################################################################
class LinkedLocationCheck(LinkedCheck):
    # @TODO
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedLocationContactCheck
#
# A check that contains a geo-coordinate and contact details
# ##############################################################################
class LinkedLocationContactCheck(LinkedCheck):
    # @TODO
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedMemberCheck
#
# A check that selects members and non-members
# ##############################################################################
class LinkedMemberCheck(LinkedCheck):
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedContactCheck
#
# A check that contains contact information
# ##############################################################################
class LinkedContactCheck(LinkedCheck):
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedFileUploadCheck
#
# A check that contains a file
# ##############################################################################
class LinkedFileUploadCheck(LinkedCheck):
    value = models.OneToOneField(
        PersistedFile, on_delete=models.CASCADE, null=True, blank=True
    )


# ##############################################################################
# LinkedInputCheck
#
# A check that contains text
# ##############################################################################
class LinkedInputCheck(LinkedCheck):
    value = OptionalCharField(max_length=300)


# ##############################################################################
# LinkedInformationCheck
#
# A check that contains extra information as text
# ##############################################################################
class LinkedInformationCheck(LinkedInputCheck):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
