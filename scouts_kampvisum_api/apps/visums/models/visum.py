from django.db import models

from apps.camps.models import CampYear, CampType
from apps.groups.models import ScoutsSection

from apps.visums.models import CampVisumEngagement
from apps.visums.models.enums import CampVisumState, CheckState
from apps.visums.managers import CampVisumManager

from scouts_auth.groupadmin.models.mixins import GroupAdminIdMixin, GroupNameMixin

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import (
    RequiredCharField,
    OptionalCharField,
    DefaultCharField,
    OptionalDateField,
    OptionalDateTimeField,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisum(GroupAdminIdMixin, GroupNameMixin, AuditedBaseModel):

    objects = CampVisumManager()

    year = models.ForeignKey(CampYear, on_delete=models.CASCADE)
    name = RequiredCharField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    sections = models.ManyToManyField(ScoutsSection)
    camp_types = models.ManyToManyField(CampType)

    camp_registration_mail_sent_before_deadline = models.BooleanField(
        default=False)
    camp_registration_mail_sent_after_deadline = models.BooleanField(
        default=False)
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
    check_state = DefaultCharField(
        choices=CheckState.choices,
        default=CheckState.UNCHECKED,
        max_length=32
    )
    # DC's can add notes to a linked category that are only viewable and editable by other DC's
    notes = OptionalCharField(max_length=300)

    class Meta:
        ordering = ["sections__age_group", "name"]
        indexes = [
            models.Index(fields=['group'], name='group_idx'),
            models.Index(fields=['group', 'year'], name='group_year_idx')
        ]
        permissions = [
            ("view_campvisum_locations", "User can view all camp locations"),
            ("view_campvisum_member_data",
             "User is allowed to view gdpr-sensitive data of members"),
            ("view_campvisum_notes", "User is a DC and can view approval notes"),
            ("change_campvisum_notes", "User is a DC and can edit approval notes"),
        ]

    def is_signable(self):
        return (
            self.state != CampVisumState.DATA_REQUIRED
            and self.state != CampVisumState.NOT_SIGNABLE
        )

    def __str__(self):
        return f"{self.id}"

    def to_simple_str(self):
        return f"{self.id}{' : ' + self.name if self.name else ''}"
    
    @property
    def location(self):
        from apps.visums.models.linked_category import LinkedCategory
        from apps.visums.models.linked_sub_category import LinkedSubCategory
        from apps.visums.models.linked_check import LinkedLocationCheck
        from apps.locations.models.camp_location import CampLocation
        from apps.locations.serializers.camp_location_minimal_serializer import CampLocationMinimalSerializer
        
        location = None
        logistics = LinkedCategory.objects.filter(
                    category_set__id=self.category_set.id, parent__name="logistics"
                )
        for linked_category in logistics:
            linked_sub_categories_logistics_locations = (
                LinkedSubCategory.objects.filter(
                    category=linked_category.id,
                    parent__name="logistics_locations",
                )
            )
            for (
                linked_sub_category
            ) in linked_sub_categories_logistics_locations:
                linked_location_checks = LinkedLocationCheck.objects.filter(
                    sub_category=linked_sub_category.id,
                    parent__name="logistics_locations_location",
                )
                for linked_location_check in linked_location_checks:
                    for (
                        linked_location
                    ) in linked_location_check.locations.all():
                        for camp_location in CampLocation.objects.filter(
                            location_id=linked_location.id
                        ):
                            location = CampLocationMinimalSerializer(
                                camp_location, many=False
                            ).data
                            location["visum_id"] = self.id
                            location["name"] = linked_location.name
                            location["start_date"] = linked_location.start_date
                            location["end_date"] = linked_location.end_date
        return location
