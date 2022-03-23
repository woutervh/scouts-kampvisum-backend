from django.db import models

from apps.camps.models import CampType

from apps.visums.managers import CheckManager
from apps.visums.models import SubCategory, CheckType

from scouts_auth.inuits.models import ArchiveableAbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField
from scouts_auth.inuits.models.interfaces import (
    Changeable,
    Explainable,
    Indexable,
    Linkable,
    Translatable,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Check(
    Changeable,
    Explainable,
    Indexable,
    Linkable,
    Translatable,
    ArchiveableAbstractBaseModel,
):

    objects = CheckManager()

    name = RequiredCharField(max_length=64)
    is_multiple = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_required_for_validation = models.BooleanField(default=True)
    sub_category = models.ForeignKey(
        SubCategory, related_name="checks", on_delete=models.CASCADE
    )
    check_type = models.ForeignKey(CheckType, on_delete=models.CASCADE)
    change_handlers = OptionalCharField()
    validators = OptionalCharField()
    camp_types = models.ManyToManyField(CampType)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "sub_category")

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED Check")
        return (self.name, self.sub_category)

    def __str__(self):
        return "OBJECT Check: name({}), sub_category({}), check_type({}), is_multiple ({}), camp_types ({})".format(
            self.name,
            str(self.sub_category),
            str(self.check_type),
            self.is_multiple,
            ", ".join(camp_type.camp_type for camp_type in self.camp_types.all())
            if self.camp_types
            else "[]",
        )

    def to_simple_str(self) -> str:
        return "{} ({})".format(self.name, self.id)
