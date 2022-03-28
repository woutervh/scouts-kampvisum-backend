from django.db import models
from dry_rest_permissions.generics import authenticated_users

from apps.camps.models import Camp, CampType

from apps.visums.models import CampVisumApproval
from apps.visums.managers import CampVisumManager

from scouts_auth.groupadmin.models import ScoutsGroup

from scouts_auth.inuits.models import AuditedBaseModel


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
    approval = models.OneToOneField(
        CampVisumApproval,
        on_delete=models.CASCADE,
        related_name="visum",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["camp__sections__age_group"]
        permissions = [
            ("create_campvisum", "User can create a camp"),
        ]

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        # logger.debug("DATA: %s", request.data)
        return True

    @authenticated_users
    def has_object_write_permission(self, request):
        if self.group in request.user.persisted_scouts_groups:
            return True

        return False

    def __str__(self):
        return "{}".format(self.id)

    def to_simple_str(self):
        return "{} ({})".format(self.camp.name, self.id)
