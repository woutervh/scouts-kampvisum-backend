import logging

from django.db import models

from apps.visums.managers import CampTypeManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Translatable, Explainable


logger = logging.getLogger(__name__)


class CampType(Translatable, Explainable, AuditedBaseModel):

    objects = CampTypeManager()

    camp_type = RequiredCharField()
    is_base = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["camp_type"]
        constraints = [
            models.UniqueConstraint(fields=["camp_type"], name="unique_camp_type")
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED CampType")
        return (self.camp_type,)

    def __str__(self):
        return "OBJECT CampType: camp_type({}), is_base ({}), is_default ({}), label ({}), explanation ({})".format(
            self.camp_type, self.is_base, self.is_default, self.label, self.explanation
        )
