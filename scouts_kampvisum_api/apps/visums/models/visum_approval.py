from django.db import models

from scouts_auth.groupadmin.models import ScoutsUser

from scouts_auth.inuits.models import AbstractBaseModel


class CampVisumApproval(AbstractBaseModel):

    approved = models.BooleanField(default=False)

    leaders = models.ForeignKey(
        ScoutsUser,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_leaders",
        null=True,
        blank=True,
    )
    group_leaders = models.ForeignKey(
        ScoutsUser,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_group_leaders",
        null=True,
        blank=True,
    )
    district_commissioner = models.ForeignKey(
        ScoutsUser,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_district_commissioner",
        null=True,
        blank=True,
    )

    def can_sign(self) -> bool:
        return self.approved

    def leaders_can_sign(self) -> bool:
        return self.can_sign()

    def group_leaders_can_sign(self) -> bool:
        return self.leaders_can_sign() and self.leaders and self.leaders.count() > 0

    def district_commissioner_can_sign(self) -> bool:
        return self.group_leaders_can_sign() and self.group_leaders and self.group_leaders.count() > 0
