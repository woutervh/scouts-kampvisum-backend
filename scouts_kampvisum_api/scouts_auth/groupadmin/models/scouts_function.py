from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.models.enums import AbstractScoutsFunctionCode
from scouts_auth.groupadmin.settings import GroupadminSettings

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import (
    RequiredCharField,
    OptionalCharField,
    OptionalDateTimeField,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_function_for_group(self, group_admin_id: str):
        return self.filter(scouts_groups__group_admin_id=group_admin_id).count() > 0


class ScoutsFunctionManager(models.Manager):
    def get_queryset(self):
        return ScoutsFunctionQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        group_admin_id = kwargs.get("group_admin_id", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if group_admin_id:
            try:
                return self.get_queryset().get(group_admin_id=group_admin_id)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsFunction instance(s) with the provided params: (id: {}, group_admin_id: {})".format(
                    pk, group_admin_id
                )
            )
        return None

    def get_by_natural_key(self, group_admin_id):
        logger.trace(
            "GET BY NATURAL KEY %s: (group_admin_id: %s (%s))",
            "ScoutsFunction",
            group_admin_id,
            type(group_admin_id).__name__,
        )

        return self.get(group_admin_id=group_admin_id)


class ScoutsFunction(AuditedBaseModel):

    objects = ScoutsFunctionManager()

    group_admin_id = RequiredCharField()
    code = OptionalCharField()
    type = OptionalCharField()
    description = OptionalCharField()
    name = OptionalCharField()
    scouts_groups = models.ManyToManyField(ScoutsGroup)
    begin = OptionalDateTimeField()
    end = OptionalDateTimeField()

    class Meta:
        ordering = ["group_admin_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["group_admin_id"], name="unique_group_admin_id"
            )
        ]

    def _has_function_for_group(self, scouts_group: ScoutsGroup = None) -> bool:
        return ScoutsFunction.objects.all().has_function_for_group(
            group_admin_id=scouts_group.group_admin_id
        )

    def _has_function_for_parent_group(self, scouts_group: ScoutsGroup = None) -> bool:
        return (
            ScoutsFunction.objects.all().has_function_for_group(
                group_admin_id=scouts_group.parent_group_admin_id
            )
            if scouts_group.parent_group_admin_id
            else False
        )

    def is_leader(self, scouts_group: ScoutsGroup = None) -> bool:
        return (
            (
                self.name.lower()
                == GroupadminSettings.get_section_leader_identifier().lower()
            )
            if not scouts_group
            or self._has_function_for_group(scouts_group=scouts_group)
            else False
        )

    def is_section_leader(self, scouts_group: ScoutsGroup = None) -> bool:
        return self.is_leader(scouts_group=scouts_group)

    def is_group_leader(self, scouts_group: ScoutsGroup = None) -> bool:
        return (
            (AbstractScoutsFunctionCode(code=self.code).is_group_leader())
            if not scouts_group
            or self._has_function_for_group(scouts_group=scouts_group)
            else False
        )

    def is_district_commissioner(self, scouts_group: ScoutsGroup = None) -> bool:
        return (
            AbstractScoutsFunctionCode(code=self.code).is_district_commissioner()
            if not scouts_group
            or self._has_function_for_group(scouts_group=scouts_group)
            or self._has_function_for_parent_group(scouts_group=scouts_group)
            else False
        )
