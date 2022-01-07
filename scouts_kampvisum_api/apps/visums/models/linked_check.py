from django.db import models

from apps.visums.models import LinkedSubCategory, Check

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCheck(AbstractBaseModel):

    parent = models.ForeignKey(Check, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="checks"
    )


# ##############################################################################
# LinkedSimpleCheck
#
# A check that can be checked, unchecked or set as not applicable
# ##############################################################################
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models.fields import DefaultCharField


class LinkedSimpleCheck(LinkedCheck):
    value = DefaultCharField(choices=CheckState.choices, default=CheckState.UNCHECKED)


# ##############################################################################
# LinkedDateCheck
#
# A check that contains a date
# ##############################################################################
from scouts_auth.inuits.models.fields import DatetypeAwareDateField


class LinkedDateCheck(LinkedCheck):
    value = DatetypeAwareDateField()


# ##############################################################################
# LinkedLocationCheck
#
# A check that contains a geo-coordinate
# ##############################################################################


class LinkedLocationCheck(LinkedCheck):
    pass


# ##############################################################################
# LinkedContactCheck
#
# A check that contains contact information
# ##############################################################################
from scouts_auth.inuits.models.fields import RequiredCharField


class LinkedContactCheck(LinkedCheck):
    value = RequiredCharField(max_length=64)


# ##############################################################################
# LinkedFileUploadCheck
#
# A check that contains a file
# ##############################################################################
from scouts_auth.inuits.models import PersistedFile


class LinkedFileUploadCheck(LinkedCheck):
    # value = models.OneToOneField(
    #     PersistedFile, on_delete=models.CASCADE, related_name="check"
    # )
    pass


# ##############################################################################
# LinkedInputCheck
#
# A check that contains text
# ##############################################################################
class LinkedInputCheck(LinkedCheck):
    value = RequiredCharField(max_length=300)


# ##############################################################################
# LinkedInformationCheck
#
# A check that contains extra information as text
# ##############################################################################
class LinkedInformationCheck(LinkedInputCheck):
    pass
