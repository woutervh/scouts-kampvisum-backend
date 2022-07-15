from django.db import models

from apps.camps.models import Camp, CampType

from apps.visums.models import CampVisumEngagement
from apps.visums.models.enums import CampVisumState
from apps.visums.managers import CampVisumManager

from scouts_auth.groupadmin.models import ScoutsGroup

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    DefaultCharField,
    OptionalDateTimeField,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisum(AuditedBaseModel):

    objects = CampVisumManager()

    group = models.ForeignKey(
        ScoutsGroup, on_delete=models.CASCADE, related_name="visums"
    )
    camp = models.OneToOneField(Camp, on_delete=models.CASCADE, related_name="visum")
    camp_types = models.ManyToManyField(CampType)

    camp_registration_mail_sent_before_deadline = models.BooleanField(default=False)
    camp_registration_mail_sent_after_deadline = models.BooleanField(default=False)
    camp_registration_mail_last_sent = OptionalDateTimeField()

    engagement = models.OneToOneField(
        CampVisumEngagement,
        on_delete=models.CASCADE,
        related_name="visum",
        null=True,
        blank=True,
    )

    state = DefaultCharField(
        choices=CampVisumState.choices,
        default=CampVisumState.DATA_REQUIRED,
        max_length=32,
    )
    # DC's can add notes to a linked category that are only viewable and editable by other DC's
    notes = OptionalCharField(max_length=300)

    class Meta:
        # ordering = ["camp__sections__age_group"]
        permissions = [
            ("view_camp_locations", "User can view all camp locations"),
            ("view_visum", "User can view a camp visum"),
            ("edit_visum", "User can create and edit a camp visum"),
            ("delete_visum", "User can delete a camp visum"),
            ("list_visum", "User can list visums for his/her group"),
            ("view_visum_notes", "User is a DC and can view approval notes"),
            ("edit_visum_notes", "User is a DC and can edit approval notes"),
        ]

    def is_signable(self):
        return (
            self.state != CampVisumState.DATA_REQUIRED
            and self.state != CampVisumState.NOT_SIGNABLE
        )

    def __str__(self):
        return "{}".format(self.id)

    def to_simple_str(self):
        return "{} ({})".format(self.camp.name, self.id)
