from django.db import models

from apps.camps.managers import CampTypeManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, UniqueBooleanField
from scouts_auth.inuits.models.interfaces import Indexable, Explainable, Translatable

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampType(Indexable, Explainable, Translatable, AuditedBaseModel):

    objects = CampTypeManager()

    camp_type = RequiredCharField()
    is_base = models.BooleanField(default=False)
    is_default = UniqueBooleanField(default=False)

    class Meta:
        ordering = ["index", "camp_type"]
        constraints = [
            models.UniqueConstraint(fields=["camp_type"], name="unique_camp_type")
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED CampType")
        return (self.camp_type,)

    def __str__(self):
        return "OBJECT CampType: id ({}), camp_type({}), is_base ({}), is_default ({}), index ({}), label ({}), explanation ({})".format(
            self.id,
            self.camp_type,
            self.is_base,
            self.is_default,
            self.index,
            self.label,
            self.explanation,
        )

    def to_readable_str(self):
        return "OBJECT CampType: {}".format(self.camp_type)
