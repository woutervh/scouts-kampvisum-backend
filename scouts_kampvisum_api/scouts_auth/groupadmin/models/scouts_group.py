from django.db import models

from scouts_auth.groupadmin.models import AbstractScoutsGroup

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField

from django.db import models
from django.core.exceptions import ValidationError


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
                "Unable to locate DefaultDeadline instance(s) with the provided params: (id: {}, group_admin_id: {})".format(
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
    
    group_admin_id = OptionalCharField()
    number = OptionalCharField()
    name = OptionalCharField()
    group_type = OptionalCharField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["group_admin_id"], name="unique_group_admin_id_for_group")
        ]
    
    
    @staticmethod
    def from_abstract_scouts_group(abstract_group: AbstractScoutsGroup):
        group = ScoutsGroup()
        
        group.group_admin_id = abstract_group.group_admin_id
        group.number = abstract_group.number
        group.name = abstract_group.name
        group.group_type = abstract_group.type
        
        return group