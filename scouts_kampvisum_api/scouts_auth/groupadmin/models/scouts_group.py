from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.groupadmin.settings import GroupadminSettings

from scouts_auth.inuits.models import AuditedBaseModel, Gender
from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScoutsGroupManager(models.Manager):
    def get_queryset(self):
        return ScoutsGroupQuerySet(self.model, using=self._db)

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
                "Unable to locate ScoutsGroup instance(s) with the provided params: (id: {}, group_admin_id: {})".format(
                    pk,
                    group_admin_id,
                )
            )
        return None

    def get_by_natural_key(self, group_admin_id):
        logger.trace(
            "GET BY NATURAL KEY %s: (group_admin_id: %s (%s))",
            "ScoutsGroup",
            group_admin_id,
            type(group_admin_id).__name__,
        )

        return self.get(group_admin_id=group_admin_id)


class ScoutsGroup(AuditedBaseModel):

    objects = ScoutsGroupManager()

    group_admin_id = RequiredCharField()
    parent_group_admin_id = OptionalCharField(null=True)
    number = OptionalCharField()
    name = OptionalCharField()
    group_type = OptionalCharField()
    default_sections_loaded = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["group_admin_id"], name="unique_group_admin_id_for_group"
            )
        ]

    @property
    def gender(self) -> Gender:
        identifier = self.number.upper().strip()[-1]
        if identifier == GroupadminSettings().get_group_gender_identifier_male():
            return Gender.MALE
        if identifier == GroupadminSettings.get_group_gender_identifier_female():
            return Gender.FEMALE
        return Gender.MIXED

    @property
    def full_name(self):
        return "{} {}".format(self.name, self.group_admin_id)

    @staticmethod
    def from_abstract_scouts_group(abstract_group: AbstractScoutsGroup):
        group = ScoutsGroup()

        group.group_admin_id = abstract_group.group_admin_id
        group.parent_group_admin_id = abstract_group.parent_group
        group.number = abstract_group.number
        group.name = abstract_group.name
        group.group_type = abstract_group.type

        return group

    def equals_abstract_scouts_group(self, abstract_group: AbstractScoutsGroup):
        return (
            self.group_admin_id == abstract_group.group_admin_id
            and self.parent_group_admin_id == abstract_group.parent_group
            and self.number == abstract_group.number
            and self.name == abstract_group.name
            and self.group_type == abstract_group.type
        )
